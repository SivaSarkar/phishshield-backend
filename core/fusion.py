# core/fusion.py

def fuse(model_score, cognitive_score, adversarial_flag):
    """
    model_score: phishing probability from detection model (0-1) - Python float
    cognitive_score: 0-1 - Python float
    adversarial_flag: Python bool
    Returns (final_score, risk_level, confidence, reasons)
    """
    # Ensure inputs are Python floats
    model_score = float(model_score)
    cognitive_score = float(cognitive_score)
    
    # Boost if adversarial (treat as more suspicious)
    adjusted_score = model_score
    if adversarial_flag:
        adjusted_score = min(model_score + 0.15, 0.99)
    
    # Final score: weighted average of model and cognitive (0.7/0.3)
    final_score = adjusted_score * 0.7 + cognitive_score * 0.3
    
    # Decision and risk level
    if final_score >= 0.7:
        risk_level = "HIGH"
    elif final_score >= 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    # Confidence is the final_score itself
    confidence = float(final_score)
    
    reasons = []
    if model_score > 0.5:
        reasons.append("URL/text patterns indicate phishing")
    if cognitive_score > 0.3:
        reasons.append("Contains psychological triggers (urgency, fear, etc.)")
    if adversarial_flag:
        reasons.append("Input appears manipulated (possible adversarial attack)")
    
    return final_score, risk_level, confidence, reasons