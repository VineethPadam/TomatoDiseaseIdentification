package com.agri.tomatodisease.model;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

public class DiagnosisResponse {

    private Long id;
    private String imageName;
    private String imagePath;
    private String predictedDisease;
    private String diseaseKey;
    private String scientificName;
    private String category;
    private Double confidenceScore;

    private WeatherIndicators weather;
    private String microclimateRiskLevel;
    private Double microclimateRiskScore;
    private List<String> microclimateFactors;

    private List<Map<String, Object>> top3Predictions;

    // Spring AI Generated Report
    private String reportSummary;
    private String symptomsReport;
    private String reasonsReport;
    private String organicRecommendations;
    private String chemicalRecommendations;
    private String preventionRecommendations;
    private String fullSpringAiReport;
    private String heatmapImage;
    private String pathologyFocusLabel;
    private String analyticsChartImage;
    private Double foliarInfectionPct;

    private LocalDateTime createdAt;

    public DiagnosisResponse() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getImageName() { return imageName; }
    public void setImageName(String imageName) { this.imageName = imageName; }

    public String getImagePath() { return imagePath; }
    public void setImagePath(String imagePath) { this.imagePath = imagePath; }

    public String getPredictedDisease() { return predictedDisease; }
    public void setPredictedDisease(String predictedDisease) { this.predictedDisease = predictedDisease; }

    public String getDiseaseKey() { return diseaseKey; }
    public void setDiseaseKey(String diseaseKey) { this.diseaseKey = diseaseKey; }

    public String getScientificName() { return scientificName; }
    public void setScientificName(String scientificName) { this.scientificName = scientificName; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public Double getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(Double confidenceScore) { this.confidenceScore = confidenceScore; }

    public WeatherIndicators getWeather() { return weather; }
    public void setWeather(WeatherIndicators weather) { this.weather = weather; }

    public String getMicroclimateRiskLevel() { return microclimateRiskLevel; }
    public void setMicroclimateRiskLevel(String microclimateRiskLevel) { this.microclimateRiskLevel = microclimateRiskLevel; }

    public Double getMicroclimateRiskScore() { return microclimateRiskScore; }
    public void setMicroclimateRiskScore(Double microclimateRiskScore) { this.microclimateRiskScore = microclimateRiskScore; }

    public List<String> getMicroclimateFactors() { return microclimateFactors; }
    public void setMicroclimateFactors(List<String> microclimateFactors) { this.microclimateFactors = microclimateFactors; }

    public List<Map<String, Object>> getTop3Predictions() { return top3Predictions; }
    public void setTop3Predictions(List<Map<String, Object>> top3Predictions) { this.top3Predictions = top3Predictions; }

    public String getReportSummary() { return reportSummary; }
    public void setReportSummary(String reportSummary) { this.reportSummary = reportSummary; }

    public String getSymptomsReport() { return symptomsReport; }
    public void setSymptomsReport(String symptomsReport) { this.symptomsReport = symptomsReport; }

    public String getReasonsReport() { return reasonsReport; }
    public void setReasonsReport(String reasonsReport) { this.reasonsReport = reasonsReport; }

    public String getOrganicRecommendations() { return organicRecommendations; }
    public void setOrganicRecommendations(String organicRecommendations) { this.organicRecommendations = organicRecommendations; }

    public String getChemicalRecommendations() { return chemicalRecommendations; }
    public void setChemicalRecommendations(String chemicalRecommendations) { this.chemicalRecommendations = chemicalRecommendations; }

    public String getPreventionRecommendations() { return preventionRecommendations; }
    public void setPreventionRecommendations(String preventionRecommendations) { this.preventionRecommendations = preventionRecommendations; }

    public String getFullSpringAiReport() { return fullSpringAiReport; }
    public void setFullSpringAiReport(String fullSpringAiReport) { this.fullSpringAiReport = fullSpringAiReport; }

    public String getHeatmapImage() { return heatmapImage; }
    public void setHeatmapImage(String heatmapImage) { this.heatmapImage = heatmapImage; }

    public String getPathologyFocusLabel() { return pathologyFocusLabel; }
    public void setPathologyFocusLabel(String pathologyFocusLabel) { this.pathologyFocusLabel = pathologyFocusLabel; }

    public String getAnalyticsChartImage() { return analyticsChartImage; }
    public void setAnalyticsChartImage(String analyticsChartImage) { this.analyticsChartImage = analyticsChartImage; }

    public Double getFoliarInfectionPct() { return foliarInfectionPct; }
    public void setFoliarInfectionPct(Double foliarInfectionPct) { this.foliarInfectionPct = foliarInfectionPct; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
