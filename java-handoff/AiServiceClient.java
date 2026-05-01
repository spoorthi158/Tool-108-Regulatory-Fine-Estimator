package com.internship.tool.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.Collections;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    public AiServiceClient(RestTemplateBuilder builder) {
        this.restTemplate = builder
                .connectTimeout(Duration.ofSeconds(10))
                .readTimeout(Duration.ofSeconds(10))
                .build();
    }

    /**
     * Calls /describe endpoint on the AI service.
     * Returns the AI-generated description string, or null on failure.
     */
    public String describeViolation(Map<String, Object> input) {
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(
                    aiServiceUrl + "/describe",
                    input,
                    Map.class
            );
            if (response.getBody() != null) {
                Object result = response.getBody().get("result");
                return result != null ? result.toString() : null;
            }
        } catch (Exception e) {
            log.error("AiServiceClient.describeViolation failed: {}", e.getMessage());
        }
        return null;
    }

    /**
     * Calls /recommend endpoint on the AI service.
     * Returns a list of 3 recommendation maps, or empty list on failure.
     */
    public List<Map<String, Object>> getRecommendations(Map<String, Object> input) {
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(
                    aiServiceUrl + "/recommend",
                    input,
                    Map.class
            );
            if (response.getBody() != null) {
                Object recommendations = response.getBody().get("recommendations");
                if (recommendations instanceof List) {
                    return (List<Map<String, Object>>) recommendations;
                }
            }
        } catch (Exception e) {
            log.error("AiServiceClient.getRecommendations failed: {}", e.getMessage());
        }
        return Collections.emptyList();
    }

    /**
     * Calls /generate-report endpoint on the AI service.
     * Returns the report as a Map, or null on failure.
     */
    public Map<String, Object> generateReport(Map<String, Object> input) {
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(
                    aiServiceUrl + "/generate-report",
                    input,
                    Map.class
            );
            if (response.getBody() != null) {
                Object report = response.getBody().get("report");
                if (report instanceof Map) {
                    return (Map<String, Object>) report;
                }
            }
        } catch (Exception e) {
            log.error("AiServiceClient.generateReport failed: {}", e.getMessage());
        }
        return null;
    }
}