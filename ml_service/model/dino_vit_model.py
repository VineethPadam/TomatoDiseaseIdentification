"""
LeafVision-DINO — ViT-S/16 with AgERA5 Multimodal Fusion Architecture
====================================================================
Implements a state-of-the-art Vision Transformer (ViT-Small/16) backbone
pretrained with self-supervised DINO (Caron et al.) for leaf pathology representation,
coupled with an AgERA5 v2.0 Agrometeorological feature fusion head.

Key Architecture Specifications:
- Patch Size: 16x16 pixels
- Image Resolution: 224x224 (196 spatial tokens + 1 [CLS] token = 197 tokens)
- Embedding Dimension: 384
- Transformer Depth: 12 Encoder Blocks
- Attention Heads: 6
- Multimodal Fusion: Gated Multimodal Unit (GMU) fusing ViT-S/16 visual tokens
  with 6 AgERA5 weather indicators (Temp, RH, Precip, Solar, Wind, VPD)
- Classification Target: 10 PlantVillage Tomato Disease Classes
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict, Any, Optional

from ml_service.data.plantvillage_classes import PLANTVILLAGE_TOMATO_CLASSES


class PatchEmbed(nn.Module):
    """
    2D Image to Patch Embedding via 16x16 Conv2d projection
    Image (B, 3, 224, 224) -> Patches (B, 196, 384)
    """
    def __init__(self, img_size: int = 224, patch_size: int = 16, in_chans: int = 3, embed_dim: int = 384):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.grid_size = (img_size // patch_size, img_size // patch_size)
        self.num_patches = self.grid_size[0] * self.grid_size[1]  # 14 * 14 = 196

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, C, H, W = x.shape
        # Conv2d -> (B, embed_dim, H/16, W/16) -> flatten to (B, embed_dim, 196) -> transpose (B, 196, embed_dim)
        x = self.proj(x).flatten(2).transpose(1, 2)
        x = self.norm(x)
        return x


class MultiHeadSelfAttention(nn.Module):
    """
    Multi-Head Self-Attention (MHSA) module as used in DINO ViT-S/16.
    Computes scaled dot-product attention across patch tokens and CLS token.
    """
    def __init__(self, dim: int = 384, num_heads: int = 6, qkv_bias: bool = True, attn_drop: float = 0.0, proj_drop: float = 0.0):
        super().__init__()
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim ** -0.5

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x: torch.Tensor, return_attn: bool = False) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, C // self.num_heads).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]  # each: (B, num_heads, N, head_dim)

        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn_weights = attn if return_attn else None
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x, attn_weights


class MLPBlock(nn.Module):
    """
    Transformer Feed-Forward MLP with GELU activation
    """
    def __init__(self, in_features: int, hidden_features: int, drop: float = 0.0):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_features, in_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class TransformerBlock(nn.Module):
    """
    Single ViT Encoder Block: LayerNorm -> MHSA -> LayerNorm -> MLP
    """
    def __init__(self, dim: int = 384, num_heads: int = 6, mlp_ratio: float = 4.0, qkv_bias: bool = True, drop: float = 0.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = MultiHeadSelfAttention(dim, num_heads=num_heads, qkv_bias=qkv_bias, attn_drop=drop, proj_drop=drop)
        self.norm2 = nn.LayerNorm(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = MLPBlock(in_features=dim, hidden_features=mlp_hidden_dim, drop=drop)

    def forward(self, x: torch.Tensor, return_attn: bool = False) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        h, attn = self.attn(self.norm1(x), return_attn=return_attn)
        x = x + h
        x = x + self.mlp(self.norm2(x))
        return x, attn


class AgERA5WeatherEncoder(nn.Module):
    """
    Encodes the 6 AgERA5 agrometeorological indicators
    (Temp, Humidity, Precip, Solar, Wind, VPD) into a dense embedding.
    """
    def __init__(self, in_dim: int = 6, out_dim: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 32),
            nn.LayerNorm(32),
            nn.GELU(),
            nn.Linear(32, out_dim),
            nn.LayerNorm(out_dim),
            nn.GELU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class LeafVisionDINOViTS16(nn.Module):
    """
    Complete Multimodal LeafVision-DINO ViT-S/16 Model.
    Fuses vision tokens with AgERA5 meteorological indicators for PlantVillage disease detection.
    """
    def __init__(
        self,
        img_size: int = 224,
        patch_size: int = 16,
        in_chans: int = 3,
        num_classes: int = 10,
        embed_dim: int = 384,
        depth: int = 6,       # Standard ViT-S has 12, depth=6 or 12 for efficient inference
        num_heads: int = 6,
        weather_in_dim: int = 6,
        weather_embed_dim: int = 64,
        drop_rate: float = 0.1
    ):
        super().__init__()
        self.num_classes = num_classes
        self.embed_dim = embed_dim

        # 1. Patch Embedding
        self.patch_embed = PatchEmbed(img_size=img_size, patch_size=patch_size, in_chans=in_chans, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches

        # 2. [CLS] token and Learnable Positional Embeddings
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        self.pos_drop = nn.Dropout(p=drop_rate)

        # 3. Transformer Encoder Blocks (DINO architecture)
        self.blocks = nn.ModuleList([
            TransformerBlock(dim=embed_dim, num_heads=num_heads, drop=drop_rate)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)

        # 4. AgERA5 Weather Indicator Encoder
        self.weather_encoder = AgERA5WeatherEncoder(in_dim=weather_in_dim, out_dim=weather_embed_dim)

        # 5. Multimodal Cross-Fusion Gate (GMU)
        self.fusion_fc = nn.Linear(embed_dim + weather_embed_dim, embed_dim)
        self.fusion_gate = nn.Sequential(
            nn.Linear(embed_dim + weather_embed_dim, embed_dim),
            nn.Sigmoid()
        )
        self.fusion_norm = nn.LayerNorm(embed_dim)

        # 6. Final Disease Classification Head
        self.head = nn.Sequential(
            nn.Linear(embed_dim, 128),
            nn.GELU(),
            nn.Dropout(p=drop_rate),
            nn.Linear(128, num_classes)
        )

        self._init_weights()

    def _init_weights(self):
        # Truncated normal initialization for position embeddings and CLS token
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        self.apply(self._init_module_weights)

    def _init_module_weights(self, m):
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)
        elif isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out')
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)

    def extract_visual_features(self, x: torch.Tensor) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Runs patch embedding and ViT encoder to extract spatial tokens and attention map
        """
        B = x.shape[0]
        x = self.patch_embed(x)  # (B, 196, 384)

        cls_tokens = self.cls_token.expand(B, -1, -1)  # (B, 1, 384)
        x = torch.cat((cls_tokens, x), dim=1)           # (B, 197, 384)
        x = self.pos_drop(x + self.pos_embed)

        last_attn = None
        for i, blk in enumerate(self.blocks):
            # Capture attention from the final block for visualization
            is_last = (i == len(self.blocks) - 1)
            x, attn = blk(x, return_attn=is_last)
            if is_last:
                last_attn = attn

        x = self.norm(x)
        cls_feat = x[:, 0]  # CLS token representation (B, 384)
        return cls_feat, last_attn

    def forward(self, img: torch.Tensor, weather: Optional[torch.Tensor] = None) -> Dict[str, Any]:
        """
        Forward pass with optional AgERA5 weather fusion.
        Args:
            img: (B, 3, 224, 224) normalized tomato leaf image tensor
            weather: (B, 6) normalized AgERA5 indicators tensor or None
        Returns:
            Dict containing logits, probabilities, visual features, and attention saliency
        """
        B = img.shape[0]
        cls_feat, last_attn = self.extract_visual_features(img)

        # Weather conditioning
        if weather is not None:
            w_feat = self.weather_encoder(weather)  # (B, 64)
            concat = torch.cat([cls_feat, w_feat], dim=-1)  # (B, 384 + 64 = 448)
            fused_cand = self.fusion_fc(concat)
            gate = self.fusion_gate(concat)
            fused = gate * cls_feat + (1.0 - gate) * fused_cand
            fused = self.fusion_norm(fused)
        else:
            fused = cls_feat

        logits = self.head(fused)
        probs = F.softmax(logits, dim=-1)

        # Compute CLS attention to 196 spatial patches
        saliency_map = None
        if last_attn is not None:
            # Average across heads: last_attn is (B, num_heads, 197, 197)
            cls_to_patches = last_attn[:, :, 0, 1:].mean(dim=1)  # (B, 196)
            saliency_map = cls_to_patches.view(B, 14, 14)

        return {
            "logits": logits,
            "probabilities": probs,
            "fused_features": fused,
            "saliency_map": saliency_map
        }
