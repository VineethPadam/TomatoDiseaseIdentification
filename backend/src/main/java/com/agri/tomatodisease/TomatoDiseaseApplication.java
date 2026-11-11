package com.agri.tomatodisease;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TomatoDiseaseApplication {

    public static void main(String[] args) {
        SpringApplication.run(TomatoDiseaseApplication.class, args);
        System.out.println("====================================================================");
        System.out.println(" Tomato Leaf Disease Identification System (Spring Boot + Spring AI)");
        System.out.println(" Running on: http://localhost:8080");
        System.out.println(" Model: LeafVision-DINO (ViT-S/16) | Indicators: AgERA5 v2.0");
        System.out.println("====================================================================");
    }
}
