package com.agri.tomatodisease.controller;

import com.agri.tomatodisease.service.SpringAiReportService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
public class AiAssistantController {

    private final SpringAiReportService springAiService;

    public AiAssistantController(SpringAiReportService springAiService) {
        this.springAiService = springAiService;
    }

    @PostMapping("/ask")
    public ResponseEntity<?> askAgronomist(@RequestBody Map<String, String> request) {
        String question = request.get("question");
        String context = request.getOrDefault("context", "General Tomato Plant Health");

        if (question == null || question.trim().isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Question cannot be empty."));
        }

        String answer = springAiService.answerFollowUpQuestion(context, question);
        return ResponseEntity.ok(Map.of(
                "question", question,
                "answer", answer,
                "engine", "Spring AI Agronomic Diagnostic Specialist"
        ));
    }
}
