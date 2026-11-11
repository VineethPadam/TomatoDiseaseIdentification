/**
 * AgroVision AI — Copernicus AgERA5 v2.0 Microclimate Controller
 * Always visible, interactive meteorological controls.
 */

const AgERA5 = {
    presets: {
        monsoon_high_humidity: {
            temperature: 22.0,
            humidity: 92.0,
            precipitation: 18.5,
            solar_radiation: 11.0,
            wind_speed: 3.2
        },
        warm_humid_summer: {
            temperature: 27.0,
            humidity: 84.0,
            precipitation: 8.0,
            solar_radiation: 16.5,
            wind_speed: 2.1
        },
        hot_arid_drought: {
            temperature: 34.0,
            humidity: 36.0,
            precipitation: 0.0,
            solar_radiation: 26.0,
            wind_speed: 4.5
        },
        optimal_greenhouse: {
            temperature: 24.0,
            humidity: 65.0,
            precipitation: 2.0,
            solar_radiation: 20.0,
            wind_speed: 1.5
        }
    },

    calculateVpd(tempC, rhPercent) {
        // Tetens equation for saturation vapour pressure in kPa
        const es = 0.61078 * Math.exp((17.27 * tempC) / (tempC + 237.3));
        const ea = es * (rhPercent / 100.0);
        const vpd = Math.max(0.01, es - ea);
        return parseFloat(vpd.toFixed(2));
    },

    init() {
        const tempSlider = document.getElementById("tempInput");
        const humSlider = document.getElementById("humidityInput");
        const presetPills = document.querySelectorAll(".preset-pill");
        const tickBtns = document.querySelectorAll(".tick-btn");

        const updateWeatherDisplay = () => {
            const t = parseFloat(tempSlider.value);
            const rh = parseFloat(humSlider.value);

            document.getElementById("tempDisplay").textContent = `${t.toFixed(1)} °C`;
            document.getElementById("humidityDisplay").textContent = `${rh.toFixed(0)} %`;

            const vpd = this.calculateVpd(t, rh);
            document.getElementById("vpdDisplay").textContent = `${vpd.toFixed(2)} kPa`;

            const bar = document.getElementById("vpdBar");
            const note = document.getElementById("vpdNote");

            if (vpd < 0.4) {
                bar.style.width = "20%";
                note.textContent = "High Leaf Wetness & Fog: Critical Late Blight / Bacterial Spore Outbreak Risk";
                note.style.color = "#ef4444";
            } else if (vpd < 0.8) {
                bar.style.width = "40%";
                note.textContent = "Humid Atmospheric Boundary: Fungal Mycelial Germination Zone";
                note.style.color = "#f59e0b";
            } else if (vpd <= 1.4) {
                bar.style.width = "65%";
                note.textContent = "Optimal Transpiration Zone: Healthy Plant Moisture Balance";
                note.style.color = "#10b981";
            } else {
                bar.style.width = "95%";
                note.textContent = "Severe Evaporative Stress: High Spider Mite & Whitefly Pest Risk";
                note.style.color = "#ef4444";
            }
        };

        tempSlider.addEventListener("input", () => {
            presetPills.forEach(p => p.classList.remove("active"));
            updateWeatherDisplay();
        });

        humSlider.addEventListener("input", () => {
            presetPills.forEach(p => p.classList.remove("active"));
            updateWeatherDisplay();
        });

        // Preset buttons
        presetPills.forEach(pill => {
            pill.addEventListener("click", () => {
                presetPills.forEach(p => p.classList.remove("active"));
                pill.classList.add("active");

                const pKey = pill.getAttribute("data-preset");
                if (this.presets[pKey]) {
                    const preset = this.presets[pKey];
                    tempSlider.value = preset.temperature;
                    humSlider.value = preset.humidity;
                    updateWeatherDisplay();
                }
            });
        });

        // Quick tick buttons
        tickBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                const val = parseFloat(btn.getAttribute("data-val"));
                const parentCard = btn.closest(".control-card");
                if (parentCard.contains(tempSlider)) {
                    tempSlider.value = val;
                } else if (parentCard.contains(humSlider)) {
                    humSlider.value = val;
                }
                presetPills.forEach(p => p.classList.remove("active"));
                updateWeatherDisplay();
            });
        });

        updateWeatherDisplay();
    },

    applyPreset(presetKey) {
        const targetPill = document.querySelector(`.preset-pill[data-preset="${presetKey}"]`);
        if (targetPill) {
            targetPill.click();
        }
    },

    getCurrentValues() {
        const temp = parseFloat(document.getElementById("tempInput").value);
        const hum = parseFloat(document.getElementById("humidityInput").value);
        const vpd = this.calculateVpd(temp, hum);
        return {
            temperature: temp,
            humidity: hum,
            precipitation: 12.0,
            solarRadiation: 16.0,
            windSpeed: 2.5,
            vpd: vpd
        };
    }
};

window.addEventListener("DOMContentLoaded", () => {
    AgERA5.init();
});
