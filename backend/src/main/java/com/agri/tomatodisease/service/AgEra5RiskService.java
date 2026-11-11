package com.agri.tomatodisease.service;

import com.agri.tomatodisease.model.WeatherIndicators;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class AgEra5RiskService {

    public double calculateVpd(double tempC, double rhPercent) {
        // Tetens equation for saturation vapour pressure in kPa
        double es = 0.61078 * Math.exp((17.27 * tempC) / (tempC + 237.3));
        double ea = es * (rhPercent / 100.0);
        return Math.max(0.05, Math.round((es - ea) * 100.0) / 100.0);
    }

    public WeatherIndicators ensureWeatherDefaults(WeatherIndicators w) {
        if (w == null) {
            w = new WeatherIndicators();
        }
        if (w.getTemperature() == null) w.setTemperature(24.5);
        if (w.getHumidity() == null) w.setHumidity(70.0);
        if (w.getPrecipitation() == null) w.setPrecipitation(2.5);
        if (w.getSolarRadiation() == null) w.setSolarRadiation(18.0);
        if (w.getWindSpeed() == null) w.setWindSpeed(2.5);
        if (w.getVpd() == null) {
            w.setVpd(calculateVpd(w.getTemperature(), w.getHumidity()));
        }
        return w;
    }

    public RiskEvaluation evaluateRisk(String diseaseKey, WeatherIndicators weather) {
        WeatherIndicators w = ensureWeatherDefaults(weather);
        double temp = w.getTemperature();
        double rh = w.getHumidity();
        double precip = w.getPrecipitation();
        double vpd = w.getVpd();

        double score = 30.0;
        List<String> factors = new ArrayList<>();

        if ("Tomato___Late_blight".equals(diseaseKey)) {
            if (temp >= 14.0 && temp <= 22.0) {
                score += 35.0;
                factors.add(String.format("Temperature of %.1f°C is ideal for Phytophthora infestans zoospore release (optimal 15-22°C).", temp));
            }
            if (rh >= 88.0) {
                score += 35.0;
                factors.add(String.format("High relative humidity (%.1f%%) promotes continuous free moisture on tomato leaflets.", rh));
            }
            if (precip > 5.0 || vpd < 0.4) {
                score += 15.0;
                factors.add(String.format("Low VPD (%.2f kPa) and precipitation (%.1f mm) prevent foliage drying.", vpd, precip));
            }
        } else if ("Tomato___Early_blight".equals(diseaseKey)) {
            if (temp >= 22.0 && temp <= 30.0) {
                score += 35.0;
                factors.add(String.format("Warm temperature (%.1f°C) accelerates Alternaria solani mycelial expansion.", temp));
            }
            if (rh >= 75.0) {
                score += 30.0;
                factors.add(String.format("Elevated humidity (%.1f%%) fulfills conidial dew requirements.", rh));
            }
            if (precip > 3.0) {
                score += 15.0;
                factors.add(String.format("Precipitation of %.1f mm drives soil-to-canopy spore splashing.", precip));
            }
        } else if ("Tomato___Bacterial_spot".equals(diseaseKey)) {
            if (temp >= 24.0 && temp <= 32.0) {
                score += 30.0;
                factors.add(String.format("Warm temperature (%.1f°C) accelerates Xanthomonas multiplication.", temp));
            }
            if (rh >= 80.0) {
                score += 25.0;
                factors.add(String.format("High ambient humidity (%.1f%%) keeps stomatal apertures open.", rh));
            }
            if (precip > 6.0) {
                score += 35.0;
                factors.add(String.format("Driving rain splash (%.1f mm) propels bacteria across foliage.", precip));
            }
        } else if ("Tomato___Spider_mites_Two_spotted_spider_mite".equals(diseaseKey)) {
            if (temp >= 28.0) {
                score += 40.0;
                factors.add(String.format("Elevated heat (%.1f°C) compresses spider mite lifecycle to under 5 days.", temp));
            }
            if (rh <= 50.0) {
                score += 35.0;
                factors.add(String.format("Low relative humidity (%.1f%%) suppresses natural fungal biocontrols.", rh));
            }
            if (vpd >= 1.8) {
                score += 20.0;
                factors.add(String.format("Atmospheric VPD demand (%.2f kPa) stresses crop transpiration.", vpd));
            }
        } else if ("Tomato___Tomato_Yellow_Leaf_Curl_Virus".equals(diseaseKey)) {
            if (temp >= 26.0) {
                score += 35.0;
                factors.add(String.format("Warm conditions (%.1f°C) stimulate whitefly (Bemisia tabaci) mobility and feeding.", temp));
            }
            if (precip < 2.0) {
                score += 25.0;
                factors.add("Absence of heavy rain allows airborne whitefly vectors to disperse without impediment.");
            }
        } else if ("Tomato___healthy".equals(diseaseKey)) {
            if (temp >= 20.0 && temp <= 26.0 && rh >= 55.0 && rh <= 75.0 && vpd >= 0.8 && vpd <= 1.4) {
                score = 92.0;
                factors.add(String.format("AgERA5 indicators (Temp: %.1f°C, RH: %.1f%%, VPD: %.2f kPa) fall directly inside the tomato vegetative comfort zone.", temp, rh, vpd));
            } else {
                score = 70.0;
                factors.add("Environmental parameters present minor physiological stress but remain within manageable bounds.");
            }
        } else {
            if (rh >= 80.0) {
                score += 30.0;
                factors.add(String.format("Humidity at %.1f%% presents elevated fungal spore germination risk.", rh));
            }
            if (temp >= 20.0 && temp <= 28.0) {
                score += 25.0;
                factors.add(String.format("Moderate temperature of %.1f°C supports phytopathogen growth.", temp));
            }
        }

        score = Math.min(99.0, Math.max(10.0, score));

        String level;
        if (score >= 75.0) {
            level = "High Risk / Outbreak Conditions";
        } else if (score >= 50.0) {
            level = "Moderate Alert";
        } else {
            level = "Low Microclimatic Stress";
        }

        if (factors.isEmpty()) {
            factors.add("Meteorological indicators are within typical baseline agricultural ranges.");
        }

        return new RiskEvaluation(level, score, factors);
    }

    public static class RiskEvaluation {
        private final String level;
        private final double score;
        private final List<String> factors;

        public RiskEvaluation(String level, double score, List<String> factors) {
            this.level = level;
            this.score = score;
            this.factors = factors;
        }

        public String getLevel() { return level; }
        public double getScore() { return score; }
        public List<String> getFactors() { return factors; }
    }
}
