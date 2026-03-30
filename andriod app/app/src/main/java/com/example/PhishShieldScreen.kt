package com.example.phishshieldmobile

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import kotlinx.coroutines.delay

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PhishShieldScreen() {
    var content by remember { mutableStateOf("") }
    var type by remember { mutableStateOf("sms") }
    var result by remember { mutableStateOf<DetectionResult?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    var showHighRiskDialog by remember { mutableStateOf(false) }
    val context = LocalContext.current

    LaunchedEffect(result) {
        if (result?.risk_level == "HIGH") {
            showHighRiskDialog = true
            delay(3000)
            showHighRiskDialog = false
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("🛡️ PhishShield-Lite", style = MaterialTheme.typography.headlineMedium)

        Text("Select Input Type:")
        Row {
            Row {
                RadioButton(selected = type == "sms", onClick = { type = "sms" })
                Text("SMS")
            }
            Row {
                RadioButton(selected = type == "url", onClick = { type = "url" })
                Text("URL")
            }
        }

        OutlinedTextField(
            value = content,
            onValueChange = { content = it },
            label = { Text(if (type == "sms") "Enter SMS" else "Enter URL") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 3
        )

        Button(
            onClick = {
                if (content.isBlank()) {
                    // This is on main thread (safe)
                    Toast.makeText(context, "Enter content", Toast.LENGTH_SHORT).show()
                    return@Button
                }
                isLoading = true
                ApiClient.detect(content, type) { detection ->
                    // This callback runs on OkHttp background thread
                    // Switch to main thread for UI updates
                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                        isLoading = false
                        if (detection != null) {
                            result = detection
                        } else {
                            Toast.makeText(context, "Detection failed", Toast.LENGTH_SHORT).show()
                        }
                    }
                }
            },
            enabled = !isLoading,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (isLoading) Text("Detecting...")
            else Text("Detect")
        }

        result?.let { DetectionResultCard(it) { id, isSafe ->
            ApiClient.sendFeedback(id, if (isSafe) "safe" else "phishing")
            Toast.makeText(context, "Feedback sent", Toast.LENGTH_SHORT).show()
        } }
    }

    if (showHighRiskDialog && result != null) {
        Dialog(onDismissRequest = {}) {
            Card(modifier = Modifier.padding(24.dp)) {
                Column(Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("⚠️ HIGH RISK", color = MaterialTheme.colorScheme.error)
                    Text("This appears to be phishing. Wait 3 seconds.")
                    Row {
                        Button(onClick = { showHighRiskDialog = false }) { Text("OK") }
                    }
                }
            }
        }
    }
}

@Composable
fun DetectionResultCard(result: DetectionResult, onFeedback: (String, Boolean) -> Unit) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp)) {
            Text("Risk: ${result.risk_level}")
            Text("Confidence: ${(result.confidence * 100).toInt()}%")
            Text("Cognitive: ${(result.cognitive_score * 100).toInt()}%")
            Text("Explanation:")
            result.explanation.forEach { Text("• $it") }
            Row {
                Button(onClick = { onFeedback(result.request_id, true) }) { Text("Safe") }
                Spacer(Modifier.width(8.dp))
                Button(onClick = { onFeedback(result.request_id, false) }) { Text("Phishing") }
            }
        }
    }
}
