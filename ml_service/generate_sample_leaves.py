"""
Generates benchmark sample tomato leaf images representing different PlantVillage classes
========================================================================================
Creates realistic synthetic test images with distinct visual patterns:
- Healthy: Lush green leaflet with subtle veining
- Early Blight: Dark concentric bullseye rings and yellow halo
- Late Blight: Irregular water-soaked greasy gray-brown lesions with pale edges
- Bacterial Spot: Small dark brown angular water-soaked speckles
- Yellow Leaf Curl: Curled cupped margins, striking yellow chlorosis
- Septoria Leaf Spot: Small circular white/gray spots with dark borders
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def draw_leaf_base(width=400, height=400, base_color=(45, 140, 50)):
    """Draws a realistic tomato leaf silhouette on a clean agronomic background"""
    img = Image.new("RGB", (width, height), (242, 246, 242))
    draw = ImageDraw.Draw(img)

    # Main leaf leaflet points (serrated tomato leaflet)
    cx, cy = width // 2, height // 2
    points = []
    num_pts = 60
    for i in range(num_pts):
        angle = (i / num_pts) * 2 * math.pi
        # Base oval + leaflet elongation
        rx = 110 * math.sin(angle / 2)
        ry = 160 * math.cos(angle)
        # Add realistic leaflet serrations
        serration = 10 * math.sin(angle * 12)
        x = cx + (rx + serration) * math.cos(angle - math.pi/2) * 0.9
        y = cy + (ry + serration) * math.sin(angle - math.pi/2) * 1.05
        points.append((x, y))

    # Fill leaflet
    draw.polygon(points, fill=base_color, outline=(base_color[0]-15, base_color[1]-20, base_color[2]-15))

    # Draw central vein and lateral veins
    draw.line([(cx, cy - 140), (cx, cy + 150)], fill=(base_color[0]+25, base_color[1]+30, base_color[2]+15), width=4)
    for vy in range(cy - 100, cy + 120, 30):
        # Left vein
        draw.line([(cx, vy), (cx - 75, vy - 25)], fill=(base_color[0]+15, base_color[1]+20, base_color[2]+10), width=2)
        # Right vein
        draw.line([(cx, vy), (cx + 75, vy - 25)], fill=(base_color[0]+15, base_color[1]+20, base_color[2]+10), width=2)

    return img


def generate_healthy():
    img = draw_leaf_base(base_color=(46, 155, 58))
    # Soft leaf texture
    return img.filter(ImageFilter.SMOOTH_MORE)


def generate_early_blight():
    img = draw_leaf_base(base_color=(60, 135, 45))
    draw = ImageDraw.Draw(img)
    # Draw concentric bullseye rings in lower/middle leaflet
    spots = [(170, 230, 35), (235, 180, 28), (190, 140, 22)]
    for sx, sy, r in spots:
        # Yellow chlorotic halo
        draw.ellipse([sx - r - 12, sy - r - 12, sx + r + 12, sy + r + 12], fill=(195, 185, 40))
        # Concentric dark rings
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(55, 35, 20))
        draw.ellipse([sx - r*0.7, sy - r*0.7, sx + r*0.7, sy + r*0.7], fill=(85, 55, 30))
        draw.ellipse([sx - r*0.4, sy - r*0.4, sx + r*0.4, sy + r*0.4], fill=(40, 25, 15))
        draw.ellipse([sx - r*0.15, sy - r*0.15, sx + r*0.15, sy + r*0.15], fill=(70, 45, 25))
    return img.filter(ImageFilter.SMOOTH)


def generate_late_blight():
    img = draw_leaf_base(base_color=(65, 115, 55))
    draw = ImageDraw.Draw(img)
    # Large water-soaked irregular dark lesions and edge collapse
    draw.polygon([(110, 150), (160, 130), (180, 190), (140, 240), (100, 210)], fill=(45, 40, 32))
    draw.polygon([(220, 200), (280, 220), (270, 290), (200, 270)], fill=(50, 45, 35))
    draw.ellipse([180, 100, 240, 160], fill=(60, 55, 40))
    # White downy mildew margin simulation
    draw.arc([110, 150, 180, 240], start=45, end=210, fill=(215, 220, 215), width=3)
    draw.arc([220, 200, 270, 290], start=120, end=300, fill=(215, 220, 215), width=3)
    return img.filter(ImageFilter.SMOOTH)


def generate_bacterial_spot():
    img = draw_leaf_base(base_color=(55, 140, 50))
    draw = ImageDraw.Draw(img)
    np.random.seed(42)
    # Many small angular dark spots with tiny yellow rims
    for _ in range(45):
        bx = int(np.random.uniform(130, 270))
        by = int(np.random.uniform(110, 290))
        rad = int(np.random.uniform(3, 7))
        draw.ellipse([bx - rad - 2, by - rad - 2, bx + rad + 2, by + rad + 2], fill=(185, 180, 45))
        draw.ellipse([bx - rad, by - rad, bx + rad, by + rad], fill=(28, 22, 18))
    return img.filter(ImageFilter.SMOOTH)


def generate_yellow_leaf_curl():
    # Pervasive interveinal chlorosis and margin curling
    img = draw_leaf_base(base_color=(195, 195, 45))
    draw = ImageDraw.Draw(img)
    # Veins stay slightly greener
    cx, cy = 200, 200
    draw.line([(cx, cy - 140), (cx, cy + 150)], fill=(70, 130, 50), width=5)
    for vy in range(cy - 100, cy + 120, 30):
        draw.line([(cx, vy), (cx - 75, vy - 25)], fill=(75, 135, 55), width=3)
        draw.line([(cx, vy), (cx + 75, vy - 25)], fill=(75, 135, 55), width=3)
    return img.filter(ImageFilter.SMOOTH_MORE)


def generate_septoria_spot():
    img = draw_leaf_base(base_color=(50, 135, 48))
    draw = ImageDraw.Draw(img)
    np.random.seed(101)
    # Circular spots with dark border and gray-white center
    for _ in range(35):
        sx = int(np.random.uniform(135, 265))
        sy = int(np.random.uniform(120, 280))
        r = int(np.random.uniform(4, 9))
        draw.ellipse([sx - r - 2, sy - r - 2, sx + r + 2, sy + r + 2], fill=(180, 175, 50))  # yellow halo
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(45, 30, 20))                    # dark margin
        draw.ellipse([sx - r*0.6, sy - r*0.6, sx + r*0.6, sy + r*0.6], fill=(195, 195, 190)) # gray center
        # Tiny black pycnidium speck in center
        draw.point((sx, sy), fill=(15, 15, 15))
    return img.filter(ImageFilter.SMOOTH)


def create_all_samples():
    sample_funcs = {
        "healthy_leaf.jpg": generate_healthy,
        "early_blight_leaf.jpg": generate_early_blight,
        "late_blight_leaf.jpg": generate_late_blight,
        "bacterial_spot_leaf.jpg": generate_bacterial_spot,
        "yellow_leaf_curl_leaf.jpg": generate_yellow_leaf_curl,
        "septoria_spot_leaf.jpg": generate_septoria_spot
    }

    out_dirs = [
        "c:/Users/kovvu/OneDrive/Desktop/Tomato_disease_identification_project_folder/project/TomatoDiseaseIdentification/ml_service/samples",
        "c:/Users/kovvu/OneDrive/Desktop/Tomato_disease_identification_project_folder/project/TomatoDiseaseIdentification/backend/src/main/resources/static/assets/sample_leaves"
    ]

    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    for filename, func in sample_funcs.items():
        img = func()
        for d in out_dirs:
            path = os.path.join(d, filename)
            img.save(path, "JPEG", quality=95)
            print(f"Saved: {path}")


if __name__ == "__main__":
    create_all_samples()
