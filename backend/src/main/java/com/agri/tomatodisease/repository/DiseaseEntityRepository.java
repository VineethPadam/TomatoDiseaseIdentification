package com.agri.tomatodisease.repository;

import com.agri.tomatodisease.model.DiseaseEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DiseaseEntityRepository extends JpaRepository<DiseaseEntity, Long> {

    Optional<DiseaseEntity> findByDiseaseKey(String diseaseKey);

    boolean existsByDiseaseKey(String diseaseKey);
}
