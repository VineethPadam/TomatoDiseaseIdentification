"""
Leaf & Foliage Validity Verification Engine (HSV & Morphological Analysis)
========================================================================
Robustly validates tomato leaves (green chlorophyll, chlorotic yellow,
necrotic lesions) and strictly rejects:
1. Tomato fruits (ripe red, orange, and smooth unripe green fruits)
2. Human portraits, faces, skin, selfies
3. Non-plant artificial objects (vehicles, sky, blue clothing, screens)
4. Paper documents, certificates, receipts, text xeroxes
5. Uniform monochromatic backgrounds, furniture, walls, fabrics

Also extracts tight bounding-box coordinates around the leaf region
so that only the leaf is cropped and evaluated by the neural network.
"""

import numpy as np
from PIL import Image, ImageFilter
from typing import Dict, Any, Optional, Tuple


def validate_leaf_image(pil_img: Image.Image) -> Dict[str, Any]:
    """
    Validates that the uploaded image depicts authentic tomato foliage (leaves),
    and strictly rejects tomato fruits, human faces, and non-plant objects.
    When valid, computes the tight bounding box around the authentic leaf region.
    """
    orig_w, orig_h = pil_img.size
    proc_dim = 256
    scale = proc_dim / float(max(orig_w, orig_h))
    proc_w = int(round(orig_w * scale))
    proc_h = int(round(orig_h * scale))
    proc_img = pil_img.resize((proc_w, proc_h), Image.Resampling.BILINEAR).convert("RGB")
    
    arr_rgb = np.array(proc_img, dtype=np.float32)
    hsv = np.array(proc_img.convert("HSV"), dtype=np.float32)
    
    r = arr_rgb[:, :, 0]
    g = arr_rgb[:, :, 1]
    b = arr_rgb[:, :, 2]
    
    # H: 0-360 degrees, S: 0-1, V: 0-1
    h = hsv[:, :, 0] / 255.0 * 360.0
    s = hsv[:, :, 1] / 255.0
    v = hsv[:, :, 2] / 255.0
    total_pixels = proc_w * proc_h

    # =====================================================================
    # 1. NON-PLANT REJECTIONS (Fruit, Human, Artificial, Documents)
    # =====================================================================
    # A. Red or orange tomato fruit
    red_fruit = ((h <= 25) | (h >= 335)) & (s >= 0.35) & (v >= 0.20) & (r > g + 25) & (r > b + 25)
    orange_fruit = (h >= 12) & (h <= 30) & (s >= 0.60) & (v >= 0.40) & (r > g + 15) & (g > b + 30)
    if (np.sum(red_fruit) / total_pixels > 0.07) or (np.sum(orange_fruit) / total_pixels > 0.08):
        return {
            "is_leaf": False,
            "leaf_score": 0.02,
            "rejection_reason": "Tomato fruit or non-foliar produce detected. Please upload a photo of a tomato leaf.",
            "bbox": None
        }

    # B. Human face / skin
    skin = (h >= 10) & (h <= 32) & (s >= 0.18) & (s <= 0.60) & (v >= 0.35) & (b >= 75) & (r > g + 10) & (g > b)
    if np.sum(skin) / total_pixels > 0.30:
        return {
            "is_leaf": False,
            "leaf_score": 0.02,
            "rejection_reason": "Human face or skin detected. Please upload a clear photo of a tomato leaf.",
            "bbox": None
        }

    # C. Blue / sky / artificial objects
    blue_obj = (b > r + 20) & (b > g + 15) & (s > 0.20)
    if np.sum(blue_obj) / total_pixels > 0.30:
        return {
            "is_leaf": False,
            "leaf_score": 0.03,
            "rejection_reason": "Non-plant object or artificial background detected. Please upload a photo of a tomato leaf.",
            "bbox": None
        }

    # D. Paper documents, certificates, white screenshots
    white_paper = (v > 0.80) & (s < 0.12) & (np.abs(r - g) < 20) & (np.abs(g - b) < 20)
    if np.sum(white_paper) / total_pixels > 0.65:
        green_on_paper = (h >= 52) & (h <= 175) & (s >= 0.15) & (g > b + 4)
        if np.sum(green_on_paper) / total_pixels < 0.035:
            return {
                "is_leaf": False,
                "leaf_score": 0.01,
                "rejection_reason": "Document, text sheet, or non-plant paper detected. Please upload a photo of a tomato leaf.",
                "bbox": None
            }

    # =====================================================================
    # 2. PLANT FOLIAGE IDENTIFICATION & SPATIAL ENVELOPE
    # =====================================================================
    # Backgrounds to disregard
    is_pure_black = (r < 28) & (g < 28) & (b < 28)
    is_bg = is_pure_black | white_paper | blue_obj | skin

    # Green chlorophyll
    green_tissue = (h >= 52) & (h <= 175) & (s >= 0.12) & (v >= 0.10) & (g >= r - 12) & (g > b + 2) & (~is_bg)
    # Chlorotic yellow
    yellow_tissue = (h >= 28) & (h < 52) & (s >= 0.18) & (v >= 0.16) & (r > b + 10) & (g > b + 4) & (~is_bg)
    foliage_seeds = green_tissue | yellow_tissue
    seed_ratio = np.sum(foliage_seeds) / total_pixels

    if seed_ratio < 0.035:
        return {
            "is_leaf": False,
            "leaf_score": 0.04,
            "rejection_reason": "No tomato leaf or plant foliage detected. Please upload a clear photo of a tomato leaf.",
            "bbox": None
        }

    # Morphological envelope around foliage
    seed_pil = Image.fromarray((foliage_seeds * 255).astype(np.uint8))
    k = max(9, int(proc_dim * 0.05) | 1)
    closed = seed_pil.filter(ImageFilter.MaxFilter(size=k)).filter(ImageFilter.MinFilter(size=k))
    leaf_envelope = np.array(closed) > 0

    # Necrotic lesion tissue within leaf envelope
    necrotic_tissue = (
        leaf_envelope &
        (h >= 14) & (h < 35) & (s >= 0.18) & (v >= 0.08) & (v <= 0.65) &
        (r > b + 4) & (g >= b - 15) & (~is_bg)
    )

    leaf_mask = (foliage_seeds | necrotic_tissue) & (~is_bg)
    leaf_ratio = np.sum(leaf_mask) / total_pixels

    if leaf_ratio < 0.045:
        return {
            "is_leaf": False,
            "leaf_score": 0.05,
            "rejection_reason": "Foliage area is too small or faint. Please upload a closer, clearer photo of the tomato leaf.",
            "bbox": None
        }

    # =====================================================================
    # 3. BOUNDING BOX EXTRACTION & SURFACE TEXTURE CHECK
    # =====================================================================
    rows = np.any(leaf_mask, axis=1)
    cols = np.any(leaf_mask, axis=0)
    if not np.any(rows) or not np.any(cols):
        return {
            "is_leaf": False,
            "leaf_score": 0.05,
            "rejection_reason": "No coherent leaf structure found. Please upload a clear photo of a tomato leaf.",
            "bbox": None
        }

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Scale bbox to original image coordinates
    ymin = int(round(rmin / scale))
    ymax = int(round(rmax / scale))
    xmin = int(round(cmin / scale))
    xmax = int(round(cmax / scale))

    # Add 6% padding around the leaf
    pad_y = int((ymax - ymin) * 0.06) + 2
    pad_x = int((xmax - xmin) * 0.06) + 2

    ymin = max(0, ymin - pad_y)
    ymax = min(orig_h, ymax + pad_y)
    xmin = max(0, xmin - pad_x)
    xmax = min(orig_w, xmax + pad_x)

    # Edge density check of leaf area
    edges = np.array(proc_img.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    leaf_edges = edges[leaf_mask]
    if len(leaf_edges) > 100:
        edge_density = float(np.mean(leaf_edges))
        color_std = float(np.std(arr_rgb[leaf_mask]))
        if edge_density < 2.8 and color_std < 10.0:
            return {
                "is_leaf": False,
                "leaf_score": 0.05,
                "rejection_reason": "Surface texture is artificial or uniform (not a natural plant leaf). Please upload an authentic photo.",
                "bbox": None
            }

    leaf_score = min(0.99, max(0.72, leaf_ratio * 1.6))
    return {
        "is_leaf": True,
        "leaf_score": round(leaf_score, 2),
        "rejection_reason": None,
        "bbox": (ymin, xmin, ymax, xmax)
    }
