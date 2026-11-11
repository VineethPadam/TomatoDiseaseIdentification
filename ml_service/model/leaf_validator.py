"""
Leaf & Foliage Validity Verification Engine (HSV & Morphological Analysis)
========================================================================
Robustly validates tomato leaves (green, chlorotic yellow, necrotic brown,
water-soaked, spotted) and decisively rejects:
1. Tomato fruits (ripe red, orange, and unripe green round tomatoes)
2. Human portraits, faces, skin
3. Non-plant images (vehicles, rooms, screenshots, animals, abstract objects)
"""

import numpy as np
from PIL import Image, ImageFilter
from typing import Dict, Any


def validate_leaf_image(pil_img: Image.Image) -> Dict[str, Any]:
    """
    Validates that the uploaded image depicts authentic tomato foliage (leaves),
    and strictly rejects tomato fruits, human faces, and non-plant objects.
    """
    img_rgb = pil_img.resize((160, 160)).convert("RGB")
    img_hsv = pil_img.resize((160, 160)).convert("HSV")
    
    arr_rgb = np.array(img_rgb, dtype=np.float32)
    arr_hsv = np.array(img_hsv, dtype=np.float32)
    
    r = arr_rgb[:, :, 0]
    g = arr_rgb[:, :, 1]
    b = arr_rgb[:, :, 2]
    
    # H: 0-360 degrees, S: 0-1, V: 0-1
    h = arr_hsv[:, :, 0] / 255.0 * 360.0
    s = arr_hsv[:, :, 1] / 255.0
    v = arr_hsv[:, :, 2] / 255.0
    
    total_pixels = 160 * 160

    # =====================================================================
    # 1. TOMATO FRUIT REJECTION (Red, Orange, and Smooth Green Fruits)
    # =====================================================================
    # A. Red / Scarlet Tomato Fruit (Ripe tomatoes, sliced tomatoes)
    red_fruit_mask = (
        ((h <= 26) | (h >= 335)) &
        (s >= 0.35) &
        (v >= 0.20) &
        (r > g + 25) &
        (r > b + 25)
    )
    red_fruit_ratio = float(np.sum(red_fruit_mask)) / total_pixels

    # B. Orange / Tangerine Tomato Fruit
    orange_fruit_mask = (
        (h >= 12) & (h <= 30) &
        (s >= 0.65) &
        (v >= 0.40) &
        (r > g + 15) &
        (g > b + 30)
    )
    orange_fruit_ratio = float(np.sum(orange_fruit_mask)) / total_pixels

    if red_fruit_ratio > 0.06 or orange_fruit_ratio > 0.08:
        return {
            "is_leaf": False,
            "leaf_score": 0.02,
            "rejection_reason": (
                "Tomato fruit detected instead of leaf foliage. "
                "The diagnostic model is trained exclusively on tomato leaves (foliage) "
                "to diagnose plant diseases. Please upload a photo of a tomato leaf."
            )
        }

    # =====================================================================
    # 2. HUMAN FACE / SKIN DETECTION
    # =====================================================================
    # Human skin: Hue 10° - 30°, S 0.18 - 0.58, V >= 0.40, High Blue (B >= 90)
    skin_mask = (
        (h >= 10) & (h <= 30) &
        (s >= 0.18) & (s <= 0.58) &
        (v >= 0.40) &
        (b >= 90) &
        (r > g + 10)
    )
    skin_ratio = float(np.sum(skin_mask)) / total_pixels

    # =====================================================================
    # 3. PLANT FOLIAGE (Green, Chlorotic Yellow, Necrotic Brown)
    # =====================================================================
    # Green leaf tissue
    green_mask = (h >= 65) & (h <= 165) & (s >= 0.12) & (v >= 0.15)
    
    # Yellow chlorotic leaf tissue (TYLCV, chlorosis, Leaf Mold)
    yellow_mask = (h >= 34) & (h <= 65) & (s >= 0.20) & (v >= 0.20) & (b < 125)
    
    # Brown necrotic leaf spots (Alternaria, Septoria, Blights on leaf tissue)
    brown_mask = (h >= 18) & (h < 34) & (s >= 0.45) & (v <= 0.65) & (b < 90)

    foliage_mask = green_mask | yellow_mask | brown_mask
    foliage_ratio = float(np.sum(foliage_mask)) / total_pixels

    # =====================================================================
    # 4. GREEN UNRIPE TOMATO FRUIT REJECTION (Spherical + Smooth Texture)
    # =====================================================================
    # A green tomato fruit is a solid circle with high fill ratio and very smooth surface
    if foliage_ratio > 0.15:
        rows = np.any(green_mask, axis=1)
        cols = np.any(green_mask, axis=0)
        if np.any(rows) and np.any(cols):
            rmin, rmax = np.where(rows)[0][[0, -1]]
            cmin, cmax = np.where(cols)[0][[0, -1]]
            h_box = rmax - rmin + 1
            w_box = cmax - cmin + 1
            if h_box > 30 and w_box > 30:
                aspect = min(h_box, w_box) / max(h_box, w_box)
                fill_ratio = np.sum(green_mask[rmin:rmax+1, cmin:cmax+1]) / (h_box * w_box)
                
                # Check internal leaf venation / texture
                edges = np.array(img_rgb.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
                int_edge = float(np.mean(edges[rmin+4:rmax-4, cmin+4:cmax-4]))
                
                # Green round fruit has circular aspect (>0.82), solid circular fill (>0.70), lacks leaf veins (edge < 10), and has no necrotic/chlorotic lesions
                has_lesions = (np.sum(brown_mask) > 40) or (np.sum(yellow_mask) > 60)
                if aspect > 0.82 and fill_ratio > 0.70 and int_edge < 9.5 and not has_lesions:
                    return {
                        "is_leaf": False,
                        "leaf_score": 0.05,
                        "rejection_reason": (
                            "Green tomato fruit detected. "
                            "Please upload an image of a tomato leaf (foliage) rather than tomato fruits."
                        )
                    }

    # =====================================================================
    # 5. REJECTION RULES FOR HUMAN / MONOCHROMATIC / NON-PLANT
    # =====================================================================
    if skin_ratio > 0.20 and foliage_ratio < 0.15:
        return {
            "is_leaf": False,
            "leaf_score": 0.03,
            "rejection_reason": "Human face or person detected in the photo. Please upload a clear photo of a tomato leaf."
        }

    # Check non-organic blue / sky / metallic objects
    blue_dominant = (b > r + 25) & (b > g + 25)
    blue_ratio = float(np.sum(blue_dominant)) / total_pixels
    if blue_ratio > 0.35 and foliage_ratio < 0.10:
        return {
            "is_leaf": False,
            "leaf_score": 0.04,
            "rejection_reason": "Non-plant image detected (artificial background or object). No leaf foliage detected."
        }

    # Minimum foliage requirement
    if foliage_ratio < 0.06:
        return {
            "is_leaf": False,
            "leaf_score": round(foliage_ratio * 4, 2),
            "rejection_reason": "No tomato leaf or plant foliage detected. Please upload a clear, focused photo of a tomato leaf."
        }

    leaf_score = min(0.99, max(0.70, foliage_ratio * 1.5))
    return {
        "is_leaf": True,
        "leaf_score": round(leaf_score, 2),
        "rejection_reason": None
    }
