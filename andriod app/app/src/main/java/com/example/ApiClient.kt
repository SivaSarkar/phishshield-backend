package com.example.phishshieldmobile

import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import com.google.gson.Gson
import java.io.IOException

object ApiClient {
    private const val BASE_URL = "http://192.168.0.6:8000"
    private val client = OkHttpClient()
    private val gson = Gson()
    private val JSON = "application/json".toMediaType()

    fun detect(content: String, type: String, callback: (DetectionResult?) -> Unit) {
        val json = """{"type":"$type","content":"$content"}"""
        android.util.Log.d("ApiClient", "Sending: $json")
        val request = Request.Builder()
            .url("$BASE_URL/detect")
            .post(json.toRequestBody(JSON))
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                android.util.Log.e("ApiClient", "Network failure", e)
                callback(null)
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                android.util.Log.d("ApiClient", "Response code: ${response.code}")
                android.util.Log.d("ApiClient", "Response body: $body")
                if (response.isSuccessful && body != null) {
                    try {
                        val result = gson.fromJson(body, DetectionResult::class.java)
                        callback(result)
                    } catch (e: Exception) {
                        android.util.Log.e("ApiClient", "JSON parsing error", e)
                        callback(null)
                    }
                } else {
                    android.util.Log.e("ApiClient", "Unsuccessful response or null body")
                    callback(null)
                }
            }
        })
    }

    fun sendFeedback(requestId: String, label: String) {
        val json = gson.toJson(FeedbackRequest(requestId, label))
        val request = Request.Builder()
            .url("$BASE_URL/feedback")
            .post(json.toRequestBody(JSON))
            .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                android.util.Log.e("ApiClient", "Feedback network error", e)
            }
            override fun onResponse(call: Call, response: Response) {
                android.util.Log.d("ApiClient", "Feedback sent, code: ${response.code}")
            }
        })
    }
}