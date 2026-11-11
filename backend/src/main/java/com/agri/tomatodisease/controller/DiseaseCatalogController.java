package com.agri.tomatodisease.controller;

import com.agri.tomatodisease.model.DiseaseEntity;
import com.agri.tomatodisease.service.DiseaseCatalogService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/diseases")
public class DiseaseCatalogController {

    private final DiseaseCatalogService catalogService;

    public DiseaseCatalogController(DiseaseCatalogService catalogService) {
        this.catalogService = catalogService;
    }

    @GetMapping
    public ResponseEntity<List<DiseaseEntity>> getAllDiseases() {
        return ResponseEntity.ok(catalogService.getAllDiseases());
    }

    @GetMapping("/{key}")
    public ResponseEntity<?> getDiseaseByKey(@PathVariable String key) {
        return catalogService.getDiseaseByKey(key)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
