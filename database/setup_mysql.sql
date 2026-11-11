-- ====================================================================
-- Tomato Leaf Disease Identification System - MySQL Database Setup
-- Project: LeafVision-DINO (ViT-S/16) + AgERA5 + Spring AI + MySQL
-- ====================================================================

CREATE DATABASE IF NOT EXISTS tomato_leaf_disease
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE tomato_leaf_disease;

-- 1. Table for Disease Knowledge Base (PlantVillage Catalog)
CREATE TABLE IF NOT EXISTS disease_catalog (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    disease_key VARCHAR(100) NOT NULL UNIQUE,
    common_name VARCHAR(150) NOT NULL,
    scientific_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    symptoms_json TEXT NOT NULL,
    reasons_json TEXT NOT NULL,
    agera5_triggers_json TEXT NOT NULL,
    organic_treatment_json TEXT NOT NULL,
    chemical_treatment_json TEXT NOT NULL,
    prevention_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table for Leaf Diagnosis & Spring AI Generated Reports
CREATE TABLE IF NOT EXISTS diagnosis_records (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    image_name VARCHAR(255) NOT NULL,
    image_path VARCHAR(500),
    predicted_disease VARCHAR(150) NOT NULL,
    disease_key VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    category VARCHAR(50),
    confidence_score DOUBLE NOT NULL,
    temperature DOUBLE,
    humidity DOUBLE,
    precipitation DOUBLE,
    solar_radiation DOUBLE,
    wind_speed DOUBLE,
    vpd DOUBLE,
    microclimate_risk_level VARCHAR(100),
    report_summary TEXT,
    symptoms_report TEXT,
    reasons_report TEXT,
    organic_recommendations TEXT,
    chemical_recommendations TEXT,
    prevention_recommendations TEXT,
    full_spring_ai_report LONGTEXT,
    heatmap_image LONGTEXT,
    pathology_focus_label VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Table for Interactive Spring AI Chat Inquiries
CREATE TABLE IF NOT EXISTS ai_chat_inquiries (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    diagnosis_record_id BIGINT,
    farmer_question TEXT NOT NULL,
    spring_ai_response LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diagnosis_record_id) REFERENCES diagnosis_records(id) ON DELETE CASCADE
);
