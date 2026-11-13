"""
AgERA5 v2.0 Agrometeorological Indicators & Phytopathological Risk Analysis
=============================================================================
Provides standardization, normalization, feature vectors, and epidemiological
disease risk modeling based on the Copernicus AgERA5 dataset specifications:
- 2m Air Temperature (°C)
- 2m Relative Humidity (%)
- Daily Precipitation Flux (mm)
- Solar Radiation Flux (MJ/m²)
- 10m Wind Speed (m/s)
- Vapour Pressure Deficit (VPD in kPa)
"""

import math
from typing import Dict, Any, Tuple

# AgERA5 Normalization baselines (mean, std) for neural network inputs
AGERA5_NORM_STATS = {
    "temperature": {"mean": 24.5, "std": 6.8},         # Range ~ 10 - 40 °C
    "humidity": {"mean": 70.0, "std": 18.5},           # Range ~ 20 - 100 %
    "precipitation": {"mean": 4.5, "std": 8.0},        # Range ~ 0 - 50 mm/day
    "solar_radiation": {"mean": 18.0, "std": 6.5},      # Range ~ 5 - 30 MJ/m²
    "wind_speed": {"mean": 2.8, "std": 1.6},           # Range ~ 0.5 - 10 m/s
    "vpd": {"mean": 1.1, "std": 0.65}                  # Range ~ 0.1 - 3.5 kPa
}

# Pre-configured AgERA5 Scenarios for educational demonstrations and simulation
AGERA5_PRESET_SCENARIOS = {
    "monsoon_high_humidity": {
        "name": "Monsoon / Rainy Season (High Blight & Bacterial Spot Risk)",
        "description": "Prolonged leaf wetness, high humidity (>90%), moderate temperature, ideal for Late Blight and Bacterial Spot.",
        "temperature": 20.5,
        "humidity": 92.0,
        "precipitation": 18.5,
        "solar_radiation": 11.0,
        "wind_speed": 3.2,
        "vpd": 0.28
    },
    "warm_humid_summer": {
        "name": "Warm & Humid Summer (Early Blight & Leaf Mold Risk)",
        "description": "Warm temperatures (27°C) with frequent showers and morning dews, triggering Alternaria and Cladosporium sporulation.",
        "temperature": 27.2,
        "humidity": 84.0,
        "precipitation": 8.0,
        "solar_radiation": 16.5,
        "wind_speed": 2.1,
        "vpd": 0.65
    },
    "hot_arid_drought": {
        "name": "Hot & Arid Drought (Spider Mite & TYLCV Whitefly Vector Risk)",
        "description": "High temperature (34°C), very low relative humidity (35%), dry atmosphere causing high transpiration stress and pest outbreaks.",
        "temperature": 34.0,
        "humidity": 36.0,
        "precipitation": 0.0,
        "solar_radiation": 26.0,
        "wind_speed": 4.5,
        "vpd": 2.85
    },
    "optimal_greenhouse": {
        "name": "Optimal Agronomic Microclimate (Vegetative Vigour / Healthy)",
        "description": "Balanced temperature (23°C), moderate humidity (62%), regulated drip moisture with healthy transpiration.",
        "temperature": 23.0,
        "humidity": 62.0,
        "precipitation": 2.0,
        "solar_radiation": 20.0,
        "wind_speed": 1.5,
        "vpd": 1.05
    },
    "cool_foggy_morning": {
        "name": "Cool Damp Foggy Autumn (Late Blight Critical Alert)",
        "description": "Cool morning (16°C), persistent relative humidity (95%), stagnant air, ideal germination threshold for Phytophthora infestans.",
        "temperature": 16.5,
        "humidity": 96.0,
        "precipitation": 4.5,
        "solar_radiation": 9.5,
        "wind_speed": 1.0,
        "vpd": 0.15
    }
}


def calculate_vpd(temp_c: float, relative_humidity: float) -> float:
    """
    Computes Vapour Pressure Deficit (VPD in kPa) using the Tetens equation
    from AgERA5 temperature and relative humidity.
    """
    # Saturated vapour pressure es in kPa
    es = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    # Actual vapour pressure ea
    ea = es * (relative_humidity / 100.0)
    vpd = max(0.01, es - ea)
    return round(vpd, 3)


def normalize_agera5_vector(indicators: Dict[str, float]) -> list:
    """
    Normalizes a dictionary of AgERA5 indicators into a 6-element standardized vector
    ready for neural network tensor input: [temp, rh, precip, solar, wind, vpd].
    """
    t = (indicators.get("temperature", 24.5) - AGERA5_NORM_STATS["temperature"]["mean"]) / AGERA5_NORM_STATS["temperature"]["std"]
    rh = (indicators.get("humidity", 70.0) - AGERA5_NORM_STATS["humidity"]["mean"]) / AGERA5_NORM_STATS["humidity"]["std"]
    pr = (indicators.get("precipitation", 4.5) - AGERA5_NORM_STATS["precipitation"]["mean"]) / AGERA5_NORM_STATS["precipitation"]["std"]
    sr = (indicators.get("solar_radiation", 18.0) - AGERA5_NORM_STATS["solar_radiation"]["mean"]) / AGERA5_NORM_STATS["solar_radiation"]["std"]
    w = (indicators.get("wind_speed", 2.8) - AGERA5_NORM_STATS["wind_speed"]["mean"]) / AGERA5_NORM_STATS["wind_speed"]["std"]
    vpd_val = indicators.get("vpd", None)
    if vpd_val is None:
        vpd_val = calculate_vpd(indicators.get("temperature", 24.5), indicators.get("humidity", 70.0))
    v = (vpd_val - AGERA5_NORM_STATS["vpd"]["mean"]) / AGERA5_NORM_STATS["vpd"]["std"]

    return [t, rh, pr, sr, w, v]


def assess_epidemiological_risk(
    disease_class: str,
    weather: Dict[str, float],
    foliar_pct: float = 0.0
) -> Dict[str, Any]:
    """
    Evaluates microclimatic and physical foliar risk for the given disease under current AgERA5 indicators.
    Integrates physical leaf foliar lesion severity (60%) with ambient microclimatic disease pressure (40%).
    Returns:
      - risk_level: "Low Risk / Optimal Health", "Low Microclimatic Stress", "Moderate Alert / Active Spread", "High Risk / Critical Outbreak"
      - risk_score: float (10.0 to 99.0)
      - risk_reasons: list of explanatory leaf pathological and microclimatic triggers
    """
    temp = weather.get("temperature", 24.0)
    rh = weather.get("humidity", 70.0)
    precip = weather.get("precipitation", 2.0)
    vpd = weather.get("vpd", calculate_vpd(temp, rh))

    score = 25.0
    reasons = []

    if disease_class == "Tomato___Late_blight":
        # Phytophthora infestans thrives in cool (15-22°C), extremely damp (>88% RH) weather
        if 14.0 <= temp <= 22.0:
            score += 35.0
            reasons.append(f"Temperature of {temp:.1f}°C is directly inside the optimal 14-22°C germination zone for Phytophthora infestans.")
        elif temp > 26.0:
            score -= 15.0
            reasons.append(f"Warm temperature ({temp:.1f}°C) restricts Late Blight sporangia viability.")

        if rh >= 90.0:
            score += 40.0
            reasons.append(f"Critical ambient humidity ({rh:.1f}%) creates near-saturated boundary air, causing persistent free moisture on leaflets.")
        elif rh >= 80.0:
            score += 20.0
            reasons.append(f"High relative humidity ({rh:.1f}%) promotes fungal mycelial expansion.")

        if precip > 5.0 or vpd < 0.35:
            score += 15.0
            reasons.append(f"Precipitation ({precip:.1f}mm) and low VPD ({vpd:.2f} kPa) prevent leaf surfaces from drying out.")

    elif disease_class == "Tomato___Early_blight":
        # Alternaria solani thrives in warm (24-30°C) with cycling wet/dew and dry periods
        if 23.0 <= temp <= 30.0:
            score += 35.0
            reasons.append(f"Warm temperature of {temp:.1f}°C accelerates Alternaria solani spore germination and lesion enlargement.")
        if rh >= 75.0:
            score += 30.0
            reasons.append(f"Elevated humidity ({rh:.1f}%) supplies the dew requirement for conidial penetration.")
        if precip > 3.0:
            score += 15.0
            reasons.append(f"Rainfall ({precip:.1f}mm) contributes to soil-to-leaf spore splashing.")

    elif disease_class == "Tomato___Bacterial_spot":
        # Xanthomonas likes warm (25-30°C) + rain splash
        if 24.0 <= temp <= 32.0:
            score += 30.0
            reasons.append(f"Warm ambient temperature ({temp:.1f}°C) stimulates Xanthomonas bacterial multiplication.")
        if rh >= 80.0:
            score += 25.0
            reasons.append(f"High humidity ({rh:.1f}%) maintains stomatal openness, facilitating bacterial ingress.")
        if precip > 8.0:
            score += 35.0
            reasons.append(f"Heavy rainfall ({precip:.1f}mm) actively splashes bacterial cells across the plant canopy.")

    elif disease_class == "Tomato___Leaf_Mold":
        # Passalora fulva likes warm (20-25°C) and RH > 85%
        if 20.0 <= temp <= 26.0:
            score += 30.0
            reasons.append(f"Moderate temperature ({temp:.1f}°C) matches Cladosporium / Passalora thermal optimum.")
        if rh >= 85.0:
            score += 45.0
            reasons.append(f"Very high relative humidity ({rh:.1f}%) is the primary catalyst for velvet mold sporulation on lower leaf surfaces.")

    elif disease_class == "Tomato___Septoria_leaf_spot":
        # Septoria likes 20-26°C and prolonged wetness
        if 20.0 <= temp <= 27.0:
            score += 30.0
            reasons.append(f"Temperature ({temp:.1f}°C) strongly favors Septoria pycnidial germination.")
        if rh >= 80.0:
            score += 30.0
            reasons.append(f"Humidity of {rh:.1f}% maintains leaf wetness required for spore thread emergence.")
        if precip > 4.0:
            score += 25.0
            reasons.append(f"Rain splash ({precip:.1f}mm) spreads pycnidiospores upward from bottom leaves.")

    elif disease_class == "Tomato___Spider_mites_Two_spotted_spider_mite":
        # Tetranychus urticae explodes in hot, dry weather
        if temp >= 28.0:
            score += 40.0
            reasons.append(f"High temperature ({temp:.1f}°C) shortens spider mite egg-to-adult generation cycle to under 6 days.")
        if rh <= 50.0:
            score += 35.0
            reasons.append(f"Dry air ({rh:.1f}% RH) eliminates fungal pathogens that naturally regulate mite populations.")
        if vpd >= 1.8:
            score += 20.0
            reasons.append(f"High atmospheric evaporative demand (VPD: {vpd:.2f} kPa) dehydrates natural biocontrol predators.")

    elif disease_class == "Tomato___Tomato_Yellow_Leaf_Curl_Virus":
        # Vector Bemisia tabaci loves warm/hot dry weather
        if temp >= 26.0:
            score += 35.0
            reasons.append(f"Warm temperature ({temp:.1f}°C) dramatically increases whitefly (Bemisia tabaci) feeding and reproduction.")
        if precip < 2.0:
            score += 25.0
            reasons.append("Absence of heavy rain allows airborne whitefly populations to fly freely and transmit TYLCV.")

    elif disease_class == "Tomato___healthy":
        # Plant is healthy: zero pathogen outbreak risk
        score = 10.0
        if 20.0 <= temp <= 26.0 and 55.0 <= rh <= 75.0 and 0.8 <= vpd <= 1.4:
            reasons.append(f"Optimal vegetative climate: Temp ({temp:.1f}°C), RH ({rh:.1f}%), and VPD ({vpd:.2f} kPa) support vigorous, disease-free tomato foliage.")
        else:
            reasons.append("Foliage is healthy. Ambient microclimate requires routine agronomic monitoring but presents minimal pathogen risk.")
        level = "Low Risk / Optimal Health"
        return {
            "disease": disease_class,
            "risk_score": round(score, 1),
            "risk_level": level,
            "vpd_kpa": round(vpd, 2),
            "microclimate_factors": reasons
        }

    # Realistic Plant-Grounding: Blend physical foliar infection severity (60%) with microclimate score (40%)
    foliar_val = max(0.0, float(foliar_pct))
    if foliar_val >= 50.0:
        foliar_severity = 75.0 + min(25.0, (foliar_val - 50.0) * 0.5)
        severity_desc = f"Critical foliar infection: {foliar_val:.1f}% of leaf tissue is destroyed by active pathological lesions."
    elif foliar_val >= 20.0:
        foliar_severity = 50.0 + (foliar_val - 20.0) * 0.83
        severity_desc = f"Substantial foliar spread: {foliar_val:.1f}% of leaf area exhibits pathological damage."
    elif foliar_val > 0.0:
        foliar_severity = 30.0 + foliar_val * 1.0
        severity_desc = f"Early localized foliar damage: {foliar_val:.1f}% symptomatic leaf area detected."
    else:
        foliar_severity = score

    if foliar_val > 0.0:
        final_score = 0.60 * foliar_severity + 0.40 * score
        reasons.insert(0, severity_desc)
    else:
        final_score = score

    # Clamp score between 10.0 and 99.0
    final_score = min(99.0, max(10.0, final_score))

    if final_score >= 70.0:
        level = "High Risk / Critical Outbreak"
    elif final_score >= 45.0:
        level = "Moderate Alert / Active Spread"
    else:
        level = "Low Microclimatic Stress"

    if not reasons:
        reasons.append("Current AgERA5 meteorological indicators are within standard baseline tolerances.")

    return {
        "disease": disease_class,
        "risk_score": round(final_score, 1),
        "risk_level": level,
        "vpd_kpa": round(vpd, 2),
        "foliar_infection_pct": round(foliar_val, 1),
        "microclimate_factors": reasons
    }
