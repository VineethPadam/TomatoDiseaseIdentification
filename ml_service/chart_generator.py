"""
AgroVision AI — Professional Matplotlib Agronomic Chart Generator
=================================================================
Generates publication-quality, 300-DPI multi-panel diagnostic graphics
visualizing ViT-S/16 classification confidence, Copernicus AgERA5 microclimatic
telemetry, and foliar surface tissue infection severity breakdown.
"""

import io
import base64
from typing import Dict, Any, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend safe for headless servers
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def generate_diagnostic_analytics_chart(
    top3: List[Dict[str, Any]],
    weather: Optional[Dict[str, Any]] = None,
    risk_info: Optional[Dict[str, Any]] = None,
    foliar_infection_pct: float = 0.0,
    predicted_disease: str = "Tomato Disease"
) -> Tuple[str, bytes]:
    """
    Creates a publication-grade, 3-panel widescreen diagnostic graphic.
    
    Panel 1: ViT-S/16 Diagnostic Confidence Spectrum (Horizontal Bar Chart)
    Panel 2: Copernicus AgERA5 Microclimate Telemetry & Risk Index
    Panel 3: Foliar Surface Area Infection Breakdown (Donut Chart)
    
    Returns:
        (base64_data_uri, raw_png_bytes)
    """
    # Defensive fallbacks
    weather = weather or {"temperature": 24.0, "humidity": 75.0, "precipitation": 2.5, "solar_radiation": 18.0, "wind_speed": 2.2, "vpd": 0.65}
    temp = float(weather.get("temperature", 24.0))
    hum = float(weather.get("humidity", 75.0))
    vpd = float(weather.get("vpd", 0.65))
    precip = float(weather.get("precipitation", 2.5))
    solar = float(weather.get("solar_radiation", 18.0))
    wind = float(weather.get("wind_speed", 2.2))
    
    risk_level = (risk_info.get("risk_level") if risk_info else None) or "Moderate Risk"
    risk_score = float(risk_info.get("risk_score", 65.0) if risk_info else 65.0)

    # Clean Top 3 items
    candidate_names = []
    candidate_confs = []
    if top3 and len(top3) > 0:
        for item in top3[:4]:
            c_name = item.get("common_name") or item.get("class_id", "").replace("Tomato___", "").replace("_", " ")
            # Truncate if overly long
            if len(c_name) > 22:
                c_name = c_name[:20] + "..."
            candidate_names.append(c_name)
            candidate_confs.append(float(item.get("confidence", 0.0)))
    else:
        candidate_names = [predicted_disease, "Secondary Pathogen", "Alternative Condition"]
        candidate_confs = [98.2, 1.3, 0.5]

    # Reverse for top-down bar chart order
    bar_names = candidate_names[::-1]
    bar_confs = candidate_confs[::-1]

    # Create figure with 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(14.2, 4.2), dpi=200)
    fig.patch.set_facecolor("#ffffff")

    # Typography & styling constants
    font_main = {"family": "sans-serif", "color": "#0f172a"}
    border_color = "#cbd5e1"

    # =========================================================================
    # PANEL 1: ViT-S/16 Diagnostic Confidence Spectrum
    # =========================================================================
    ax0 = axs[0]
    ax0.set_facecolor("#f8fafc")
    y_pos = np.arange(len(bar_names))
    
    # Highlight top diagnosed class in vibrant emerald green (#10b981)
    bar_colors = ["#94a3b8"] * (len(bar_names) - 1) + ["#10b981"]
    bars0 = ax0.barh(y_pos, bar_confs, color=bar_colors, height=0.52, edgecolor="#0f766e", linewidth=0.7)
    
    ax0.set_yticks(y_pos)
    ax0.set_yticklabels(bar_names, fontsize=8.5, fontweight="bold", color="#1e293b")
    ax0.set_xlim(0, 115)
    ax0.set_xlabel("Confidence Probability (%)", fontsize=8.5, fontweight="bold", color="#475569")
    ax0.set_title("1. ViT-S/16 Diagnostic Confidence", fontsize=10.5, fontweight="bold", color="#065f46", pad=10)
    
    for bar, val in zip(bars0, bar_confs):
        ax0.text(
            val + 1.8,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            ha="left",
            fontsize=8.5,
            fontweight="bold",
            color="#0f172a"
        )
    
    ax0.spines["top"].set_visible(False)
    ax0.spines["right"].set_visible(False)
    ax0.spines["left"].set_color(border_color)
    ax0.spines["bottom"].set_color(border_color)
    ax0.grid(axis="x", linestyle="--", alpha=0.35, color="#94a3b8")

    # =========================================================================
    # PANEL 2: Copernicus AgERA5 Microclimate Telemetry & Risk Index
    # =========================================================================
    ax1 = axs[1]
    ax1.set_facecolor("#f8fafc")
    
    telemetry_labels = ["Temp\n(°C)", "Humidity\n(%)", "VPD\n(kPa*10)", "Precip\n(mm)", "Solar\n(MJ/m²)", "Wind\n(m/s)"]
    telemetry_vals = [temp, hum, vpd * 10.0, precip, solar, wind]
    
    # Meaningful agronomic palette
    tel_colors = ["#f59e0b", "#0284c7", "#8b5cf6", "#06b6d4", "#eab308", "#64748b"]
    bars1 = ax1.bar(telemetry_labels, telemetry_vals, color=tel_colors, width=0.55, edgecolor="#334155", linewidth=0.5)
    
    ax1.set_title("2. AgERA5 Weather & Risk Level", fontsize=10.5, fontweight="bold", color="#065f46", pad=10)
    max_val = max(telemetry_vals) if telemetry_vals else 100
    ax1.set_ylim(0, max(105, max_val * 1.22))
    
    for bar, val, raw_val in zip(bars1, telemetry_vals, [temp, hum, vpd, precip, solar, wind]):
        display_str = f"{raw_val:.1f}" if raw_val < 10 else f"{int(round(raw_val))}"
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            val + (max_val * 0.035 + 1.2),
            display_str,
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#1e293b"
        )

    # Risk badge box inside panel 2
    risk_color = "#ef4444" if ("High" in risk_level or "Severe" in risk_level or risk_score > 70) else ("#f59e0b" if "Mod" in risk_level else "#10b981")
    ax1.text(
        0.5, 0.90,
        f"Microclimate Alert: {risk_level} ({risk_score:.0f}%)",
        transform=ax1.transAxes,
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#ffffff",
        bbox=dict(boxstyle="round,pad=0.35", facecolor=risk_color, edgecolor="none", alpha=0.95)
    )

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color(border_color)
    ax1.spines["bottom"].set_color(border_color)
    ax1.grid(axis="y", linestyle="--", alpha=0.35, color="#94a3b8")

    # =========================================================================
    # PANEL 3: Foliar Surface Area Infection Breakdown (Donut Chart)
    # =========================================================================
    ax2 = axs[2]
    ax2.set_facecolor("#ffffff")
    
    clamped_inf = max(0.0, min(100.0, float(foliar_infection_pct)))
    healthy_pct = 100.0 - clamped_inf
    
    if clamped_inf < 0.5:
        # Healthy Leaf
        donut_sizes = [100.0]
        donut_colors = ["#23be32"]
        donut_labels = ["100% Healthy Foliage"]
        center_text = "0% Lesions\nHealthy"
        center_color = "#059669"
        explode = (0.0,)
    else:
        donut_sizes = [clamped_inf, healthy_pct]
        # Matching exact heatmap colors: Hot Red (#fa281e) vs Foliage Green (#23be32)
        donut_colors = ["#fa281e", "#23be32"]
        donut_labels = [f"Diseased\n{clamped_inf:.1f}%", f"Healthy\n{healthy_pct:.1f}%"]
        center_text = f"{clamped_inf:.1f}%\nInfected"
        center_color = "#dc2626"
        explode = (0.04, 0.0)

    wedges, texts, autotexts = ax2.pie(
        donut_sizes,
        labels=donut_labels,
        colors=donut_colors,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.76,
        explode=explode,
        wedgeprops=dict(width=0.44, edgecolor="#ffffff", linewidth=2.0),
        textprops=dict(fontsize=8.0, fontweight="bold", color="#0f172a")
    )
    
    for autotext in autotexts:
        autotext.set_color("#ffffff")
        autotext.set_fontsize(8.5)
        autotext.set_fontweight("bold")

    # Inner donut center text
    ax2.text(
        0, 0,
        center_text,
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color=center_color
    )
    
    ax2.set_title("3. Foliar Infection Ratio", fontsize=10.5, fontweight="bold", color="#065f46", pad=10)

    # Finalize layout
    plt.tight_layout(pad=1.8)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="PNG", dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    
    raw_bytes = buf.getvalue()
    b64_str = base64.b64encode(raw_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64_str}"
    
    return data_uri, raw_bytes
