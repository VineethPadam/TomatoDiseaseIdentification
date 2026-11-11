package com.agri.tomatodisease.repository;

import com.agri.tomatodisease.model.DiagnosisRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DiagnosisRecordRepository extends JpaRepository<DiagnosisRecord, Long> {

    List<DiagnosisRecord> findAllByOrderByCreatedAtDesc();

    List<DiagnosisRecord> findByDiseaseKeyOrderByCreatedAtDesc(String diseaseKey);
}
