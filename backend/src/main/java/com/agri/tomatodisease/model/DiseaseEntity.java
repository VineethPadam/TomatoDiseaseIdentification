package com.agri.tomatodisease.model;

import jakarta.persistence.*;

@Entity
@Table(name = "disease_catalog")
public class DiseaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "disease_key", nullable = false, unique = true, length = 100)
    private String diseaseKey;

    @Column(name = "common_name", nullable = false, length = 150)
    private String commonName;

    @Column(name = "scientific_name", nullable = false, length = 150)
    private String scientificName;

    @Column(name = "category", nullable = false, length = 50)
    private String category;

    @Column(name = "symptoms_json", columnDefinition = "TEXT")
    private String symptomsJson;

    @Column(name = "reasons_json", columnDefinition = "TEXT")
    private String reasonsJson;

    @Column(name = "agera5_triggers_json", columnDefinition = "TEXT")
    private String agera5TriggersJson;

    @Column(name = "organic_treatment_json", columnDefinition = "TEXT")
    private String organicTreatmentJson;

    @Column(name = "chemical_treatment_json", columnDefinition = "TEXT")
    private String chemicalTreatmentJson;

    @Column(name = "prevention_json", columnDefinition = "TEXT")
    private String preventionJson;

    public DiseaseEntity() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getDiseaseKey() { return diseaseKey; }
    public void setDiseaseKey(String diseaseKey) { this.diseaseKey = diseaseKey; }

    public String getCommonName() { return commonName; }
    public void setCommonName(String commonName) { this.commonName = commonName; }

    public String getScientificName() { return scientificName; }
    public void setScientificName(String scientificName) { this.scientificName = scientificName; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getSymptomsJson() { return symptomsJson; }
    public void setSymptomsJson(String symptomsJson) { this.symptomsJson = symptomsJson; }

    public String getReasonsJson() { return reasonsJson; }
    public void setReasonsJson(String reasonsJson) { this.reasonsJson = reasonsJson; }

    public String getAgera5TriggersJson() { return agera5TriggersJson; }
    public void setAgera5TriggersJson(String agera5TriggersJson) { this.agera5TriggersJson = agera5TriggersJson; }

    public String getOrganicTreatmentJson() { return organicTreatmentJson; }
    public void setOrganicTreatmentJson(String organicTreatmentJson) { this.organicTreatmentJson = organicTreatmentJson; }

    public String getChemicalTreatmentJson() { return chemicalTreatmentJson; }
    public void setChemicalTreatmentJson(String chemicalTreatmentJson) { this.chemicalTreatmentJson = chemicalTreatmentJson; }

    public String getPreventionJson() { return preventionJson; }
    public void setPreventionJson(String preventionJson) { this.preventionJson = preventionJson; }
}
