package com.example.phishshieldmobile

data class DetectionResult(
    val request_id: String,
    val decision: String,
    val risk_level: String,
    val confidence: Double,
    val cognitive_score: Double,
    val adversarial_detected: Boolean,
    val explanation: List<String>
)