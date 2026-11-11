package com.agri.tomatodisease.model;

public class WeatherIndicators {

    private Double temperature;      // 2m Temperature in °C
    private Double humidity;         // 2m Relative Humidity in %
    private Double precipitation;    // Daily precipitation in mm
    private Double solarRadiation;   // Solar radiation flux in MJ/m²
    private Double windSpeed;        // 10m wind speed in m/s
    private Double vpd;              // Vapour Pressure Deficit in kPa

    public WeatherIndicators() {}

    public WeatherIndicators(Double temperature, Double humidity, Double precipitation,
                             Double solarRadiation, Double windSpeed, Double vpd) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.precipitation = precipitation;
        this.solarRadiation = solarRadiation;
        this.windSpeed = windSpeed;
        this.vpd = vpd;
    }

    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }

    public Double getHumidity() { return humidity; }
    public void setHumidity(Double humidity) { this.humidity = humidity; }

    public Double getPrecipitation() { return precipitation; }
    public void setPrecipitation(Double precipitation) { this.precipitation = precipitation; }

    public Double getSolarRadiation() { return solarRadiation; }
    public void setSolarRadiation(Double solarRadiation) { this.solarRadiation = solarRadiation; }

    public Double getWindSpeed() { return windSpeed; }
    public void setWindSpeed(Double windSpeed) { this.windSpeed = windSpeed; }

    public Double getVpd() { return vpd; }
    public void setVpd(Double vpd) { this.vpd = vpd; }
}
