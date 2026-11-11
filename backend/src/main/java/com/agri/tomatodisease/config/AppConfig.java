package com.agri.tomatodisease.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.io.File;

@Configuration
public class AppConfig {

    @Value("${upload.dir:./uploads}")
    private String uploadDir;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public CommandLineRunner initUploadDirectory() {
        return args -> {
            File dir = new File(uploadDir);
            if (!dir.exists()) {
                boolean created = dir.mkdirs();
                if (created) {
                    System.out.println("Created uploads directory at: " + dir.getAbsolutePath());
                }
            }
        };
    }
}
