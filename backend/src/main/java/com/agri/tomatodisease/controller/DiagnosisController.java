package com.agri.tomatodisease.controller;

import com.agri.tomatodisease.model.DiagnosisRecord;
import com.agri.tomatodisease.model.DiagnosisResponse;
import com.agri.tomatodisease.model.DiseaseEntity;
import com.agri.tomatodisease.model.WeatherIndicators;
import com.agri.tomatodisease.repository.DiagnosisRecordRepository;
import com.agri.tomatodisease.service.AgEra5RiskService;
import com.agri.tomatodisease.service.DiseaseCatalogService;
import com.agri.tomatodisease.service.MlInferenceService;
import com.agri.tomatodisease.service.SpringAiReportService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.*;

@RestController
@RequestMapping("/api/diagnosis")
public class DiagnosisController {

    @Value("${upload.dir:./uploads}")
    private String uploadDir;

    private final MlInferenceService mlService;
    private final DiseaseCatalogService catalogService;
    private final AgEra5RiskService riskService;
    private final SpringAiReportService springAiService;
    private final DiagnosisRecordRepository recordRepository;

    public DiagnosisController(
            MlInferenceService mlService,
            DiseaseCatalogService catalogService,
            AgEra5RiskService riskService,
            SpringAiReportService springAiService,
            DiagnosisRecordRepository recordRepository
    ) {
        this.mlService = mlService;
        this.catalogService = catalogService;
        this.riskService = riskService;
        this.springAiService = springAiService;
        this.recordRepository = recordRepository;
    }

    @PostMapping("/predict")
    public ResponseEntity<?> diagnoseLeaf(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "temperature", required = false) Double temperature,
            @RequestParam(value = "humidity", required = false) Double humidity,
            @RequestParam(value = "precipitation", required = false) Double precipitation,
            @RequestParam(value = "solarRadiation", required = false) Double solarRadiation,
            @RequestParam(value = "windSpeed", required = false) Double windSpeed,
            @RequestParam(value = "vpd", required = false) Double vpd
    ) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Please upload a valid tomato leaf image."));
        }

        try {
            // 1. Save uploaded leaf image file
            String originalFilename = file.getOriginalFilename();
            String storedFilename = System.currentTimeMillis() + "_" + (originalFilename != null ? originalFilename.replaceAll("\\s+", "_") : "leaf.jpg");
            File destination = new File(uploadDir, storedFilename);
            if (!destination.getParentFile().exists()) {
                destination.getParentFile().mkdirs();
            }
            try (FileOutputStream fos = new FileOutputStream(destination)) {
                fos.write(file.getBytes());
            }

            // 2. Prepare AgERA5 Weather Indicators
            WeatherIndicators weather = new WeatherIndicators(temperature, humidity, precipitation, solarRadiation, windSpeed, vpd);
            weather = riskService.ensureWeatherDefaults(weather);

            // 3. Invoke LeafVision-DINO ViT-S/16 Inference
            Map<String, Object> mlResult = mlService.predictDisease(file.getBytes(), originalFilename, weather);
            
            // Check for Leaf Validity (Rejects human faces, selfies, animals, non-leaf objects)
            Object isValidObj = mlResult.get("is_valid_leaf");
            if (isValidObj != null && Boolean.FALSE.equals(isValidObj)) {
                String errorMsg = (String) mlResult.getOrDefault("error_message", 
                        "Invalid image: No plant foliage or tomato leaf detected. The uploaded photo appears to be a person or non-plant object. Please upload a clear photo of a tomato leaf.");
                return ResponseEntity.badRequest().body(Map.of(
                        "is_valid_leaf", false,
                        "error", errorMsg
                ));
            }

            String predictedKey = (String) mlResult.getOrDefault("predicted_class", "Tomato___healthy");
            String commonName = (String) mlResult.getOrDefault("common_name", "Tomato Leaf Diagnosis");
            String scientificName = (String) mlResult.getOrDefault("scientific_name", "Solanum lycopersicum");
            String category = (String) mlResult.getOrDefault("category", "General");
            Double confidence = Double.valueOf(String.valueOf(mlResult.getOrDefault("confidence", 98.4)));
            String heatmapImage = (String) mlResult.get("heatmap_image");
            String pathologyFocusLabel = (String) mlResult.getOrDefault("pathology_focus_label", "Active Pathological Lesion Focus");
            String analyticsChartImage = (String) mlResult.get("analytics_chart_image");

            @SuppressWarnings("unchecked")
            List<Map<String, Object>> top3 = (List<Map<String, Object>>) mlResult.get("top3");

            // 4. Retrieve Disease Catalog Knowledge
            Optional<DiseaseEntity> diseaseOpt = catalogService.getDiseaseByKey(predictedKey);
            DiseaseEntity diseaseEntity = diseaseOpt.orElse(null);
            if (diseaseEntity != null) {
                scientificName = diseaseEntity.getScientificName();
                category = diseaseEntity.getCategory();
                commonName = diseaseEntity.getCommonName();
            }

            // 5. Evaluate AgERA5 Microclimatic Risk
            AgEra5RiskService.RiskEvaluation riskEval = riskService.evaluateRisk(predictedKey, weather);

            // 6. Generate Comprehensive Spring AI Report
            SpringAiReportService.ReportResult aiReport = springAiService.generateComprehensiveReport(
                    commonName,
                    predictedKey,
                    confidence,
                    diseaseEntity,
                    weather,
                    riskEval
            );

            // 7. Persist Diagnosis Record to MySQL
            DiagnosisRecord record = new DiagnosisRecord();
            record.setImageName(storedFilename);
            record.setImagePath("/" + storedFilename);
            record.setPredictedDisease(commonName);
            record.setDiseaseKey(predictedKey);
            record.setScientificName(scientificName);
            record.setCategory(category);
            record.setConfidenceScore(confidence);
            record.setTemperature(weather.getTemperature());
            record.setHumidity(weather.getHumidity());
            record.setPrecipitation(weather.getPrecipitation());
            record.setSolarRadiation(weather.getSolarRadiation());
            record.setWindSpeed(weather.getWindSpeed());
            record.setVpd(weather.getVpd());
            record.setMicroclimateRiskLevel(riskEval.getLevel());
            record.setReportSummary(aiReport.getSummary());
            record.setSymptomsReport(aiReport.getSymptoms());
            record.setReasonsReport(aiReport.getReasons());
            record.setOrganicRecommendations(aiReport.getOrganics());
            record.setChemicalRecommendations(aiReport.getChemicals());
            record.setPreventionRecommendations(aiReport.getPreventions());
            record.setFullSpringAiReport(aiReport.getFullReport());
            record.setHeatmapImage(heatmapImage);
            record.setPathologyFocusLabel(pathologyFocusLabel);
            record.setAnalyticsChartImage(analyticsChartImage);
            record.setCreatedAt(LocalDateTime.now());

            DiagnosisRecord saved = recordRepository.save(record);

            // 8. Assemble Full Diagnosis Response
            DiagnosisResponse response = new DiagnosisResponse();
            response.setId(saved.getId());
            response.setImageName(saved.getImageName());
            response.setImagePath(saved.getImagePath());
            response.setHeatmapImage(saved.getHeatmapImage());
            response.setPathologyFocusLabel(saved.getPathologyFocusLabel());
            response.setAnalyticsChartImage(saved.getAnalyticsChartImage());
            response.setPredictedDisease(saved.getPredictedDisease());
            response.setDiseaseKey(saved.getDiseaseKey());
            response.setScientificName(saved.getScientificName());
            response.setCategory(saved.getCategory());
            response.setConfidenceScore(saved.getConfidenceScore());
            response.setWeather(weather);
            response.setMicroclimateRiskLevel(riskEval.getLevel());
            response.setMicroclimateRiskScore(riskEval.getScore());
            response.setMicroclimateFactors(riskEval.getFactors());
            response.setTop3Predictions(top3);
            response.setReportSummary(aiReport.getSummary());
            response.setSymptomsReport(aiReport.getSymptoms());
            response.setReasonsReport(aiReport.getReasons());
            response.setOrganicRecommendations(aiReport.getOrganics());
            response.setChemicalRecommendations(aiReport.getChemicals());
            response.setPreventionRecommendations(aiReport.getPreventions());
            response.setFullSpringAiReport(aiReport.getFullReport());
            response.setCreatedAt(saved.getCreatedAt());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body(Map.of("error", "Diagnosis failed: " + e.getMessage()));
        }
    }

    @GetMapping("/history")
    public ResponseEntity<List<DiagnosisRecord>> getHistory() {
        return ResponseEntity.ok(recordRepository.findAllByOrderByCreatedAtDesc());
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getDiagnosisById(@PathVariable Long id) {
        return recordRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteDiagnosis(@PathVariable Long id) {
        if (recordRepository.existsById(id)) {
            recordRepository.deleteById(id);
            return ResponseEntity.ok(Map.of("message", "Record deleted successfully."));
        }
        return ResponseEntity.notFound().build();
    }

    @GetMapping("/{id}/report")
    public ResponseEntity<String> getPrintableReport(@PathVariable Long id) {
        return recordRepository.findById(id)
                .map(r -> ResponseEntity.ok()
                        .header("Content-Type", "text/plain; charset=utf-8")
                        .body(r.getFullSpringAiReport()))
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/{id}/download-pdf")
    public ResponseEntity<?> downloadPhytosanitaryPdf(@PathVariable Long id) {
        Optional<DiagnosisRecord> recordOpt = recordRepository.findById(id);
        if (recordOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        DiagnosisRecord record = recordOpt.get();

        byte[] originalImageBytes = null;
        try {
            if (record.getImageName() != null) {
                File imgFile = new File(uploadDir, record.getImageName());
                if (imgFile.exists()) {
                    originalImageBytes = Files.readAllBytes(imgFile.toPath());
                }
            }
        } catch (Exception e) {
            System.err.println("Notice: Could not read original leaf image from disk: " + e.getMessage());
        }

        byte[] pdfBytes = mlService.generatePdf(record, originalImageBytes);
        if (pdfBytes == null || pdfBytes.length == 0) {
            return ResponseEntity.internalServerError().body(Map.of("error", "Failed to compile official phytosanitary PDF."));
        }

        String cleanName = record.getPredictedDisease() != null ? record.getPredictedDisease().replaceAll("[^a-zA-Z0-9_-]", "_") : "Report";
        String filename = "AgroVision_Phytosanitary_Report_" + record.getId() + "_" + cleanName + ".pdf";

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
                .contentType(MediaType.APPLICATION_PDF)
                .contentLength(pdfBytes.length)
                .body(pdfBytes);
    }
}
