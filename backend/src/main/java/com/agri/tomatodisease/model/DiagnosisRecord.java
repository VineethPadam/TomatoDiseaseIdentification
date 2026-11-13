package com.agri.tomatodisease.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "diagnosis_records")
public class DiagnosisRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "image_name", nullable = false)
    private String imageName;

    @Column(name = "image_path", length = 500)
    private String imagePath;

    @Column(name = "predicted_disease", nullable = false, length = 150)
    private String predictedDisease;

    @Column(name = "disease_key", nullable = false, length = 100)
    private String diseaseKey;

    @Column(name = "scientific_name", length = 150)
    private String scientificName;

    @Column(name = "category", length = 50)
    private String category;

    @Column(name = "confidence_score", nullable = false)
    private Double confidenceScore;

    // AgERA5 Indicators
    private Double temperature;
    private Double humidity;
    private Double precipitation;
    private Double solarRadiation;
    private Double windSpeed;
    private Double vpd;

    @Column(name = "microclimate_risk_level", length = 100)
    private String microclimateRiskLevel;

    // Spring AI Report Breakdown
    @Column(name = "report_summary", columnDefinition = "TEXT")
    private String reportSummary;

    @Column(name = "symptoms_report", columnDefinition = "TEXT")
    private String symptomsReport;

    @Column(name = "reasons_report", columnDefinition = "TEXT")
    private String reasonsReport;

    @Column(name = "organic_recommendations", columnDefinition = "TEXT")
    private String organicRecommendations;

    @Column(name = "chemical_recommendations", columnDefinition = "TEXT")
    private String chemicalRecommendations;

    @Column(name = "prevention_recommendations", columnDefinition = "TEXT")
    private String preventionRecommendations;

    @Lob
    @Column(name = "full_spring_ai_report", columnDefinition = "LONGTEXT")
    private String fullSpringAiReport;

    @Lob
    @Column(name = "heatmap_image", columnDefinition = "LONGTEXT")
    private String heatmapImage;

    @Lob
    @Column(name = "analytics_chart_image", columnDefinition = "LONGTEXT")
    private String analyticsChartImage;

    @Column(name = "foliar_infection_pct")
    private Double foliarInfectionPct;

    @Column(name = "pathology_focus_label", length = 200)
    private String pathologyFocusLabel;

    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    public DiagnosisRecord() {}

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

    public String getMicroclimateRiskLevel() { return microclimateRiskLevel; }
    public void setMicroclimateRiskLevel(String microclimateRiskLevel) { this.microclimateRiskLevel = microclimateRiskLevel; }

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
