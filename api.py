from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from core.detection_engine import predict_sms_phishing, predict_url_phishing
from core.cognitive_layer import CognitiveVulnerability
from core.adversarial import is_adversarial
from core.fusion import fuse

app = FastAPI(title="PhishShield Detection API", version="1.0")

# Initialize the cognitive vulnerability layer
cognitive = CognitiveVulnerability()

class DetectionRequest(BaseModel):
    type: str
    content: str

class FeedbackRequest(BaseModel):
    request_id: str
    feedback_label: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/detect")
async def detect(request: DetectionRequest):
    # 1. Detection
    if request.type in ['sms', 'email']:
        model_score = predict_sms_phishing(request.content)
    elif request.type == 'url':
        model_score = predict_url_phishing(request.content)
    else:
        raise HTTPException(status_code=400, detail="Invalid type. Use 'sms', 'email', or 'url'")

    # 2. Cognitive vulnerability
    cognitive_score, cognitive_reasons = cognitive.score(request.content)

    # 3. Adversarial detection (only for text types)
    adv_flag = False
    if request.type in ['sms', 'email']:
        adv_flag = is_adversarial(request.content)

    # 4. Fusion
    final_score, risk_level, confidence, fusion_reasons = fuse(model_score, cognitive_score, adv_flag)

    # Combine all reasons
    all_reasons = cognitive_reasons + fusion_reasons
    if adv_flag and "adversarial" not in str(all_reasons).lower():
        all_reasons.append("Input appears manipulated")

    # Return all values as native Python types (already ensured by our fixes)
    return {
        "request_id": str(uuid.uuid4()),
        "decision": "phishing" if risk_level != "LOW" else "legitimate",
        "risk_level": risk_level,
        "confidence": confidence,
        "cognitive_score": cognitive_score,
        "adversarial_detected": adv_flag,
        "explanation": all_reasons[:5]
    }

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    print(f"Feedback received: {request.request_id} -> {request.feedback_label}")
    return {"status": "feedback received", "request_id": request.request_id}