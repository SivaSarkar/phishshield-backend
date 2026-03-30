# core/cognitive_layer.py
import re

class CognitiveVulnerability:
    """Detect psychological triggers in text."""

    def __init__(self):
        # Urgency keywords
        self.urgency_patterns = [
            r'\b(immediate|immediately|urgent|asap|now|quick|instant|right away)\b',
            r'\b(act now|don\'t delay|expires|deadline|limited time)\b'
        ]
        # Fear/threat keywords
        self.fear_patterns = [
            r'\b(suspended|terminated|blocked|locked|violation|fraud|unauthorized)\b',
            r'\b(will be deleted|will be closed|legal action|fine|penalty)\b'
        ]
        # Authority impersonation
        self.authority_patterns = [
            r'\b(bank|paypal|amazon|google|microsoft|apple|irs|gov|tax)\b',
            r'\b(support|security team|administrator|department)\b'
        ]
        # Reward/lure
        self.reward_patterns = [
            r'\b(win|prize|reward|free|gift card|coupon|discount)\b',
            r'\b(congratulations|you have been selected|claim now)\b'
        ]

    def score(self, text):
        text_lower = text.lower()
        reasons = []

        urgency_score = sum(1 for p in self.urgency_patterns if re.search(p, text_lower))
        fear_score = sum(1 for p in self.fear_patterns if re.search(p, text_lower))
        authority_score = sum(1 for p in self.authority_patterns if re.search(p, text_lower))
        reward_score = sum(1 for p in self.reward_patterns if re.search(p, text_lower))

        # Normalize each to 0..1 (max 3 occurrences per category)
        urgency = min(urgency_score / 3, 1.0)
        fear = min(fear_score / 3, 1.0)
        authority = min(authority_score / 3, 1.0)
        reward = min(reward_score / 3, 1.0)

        # Combined cognitive risk (weighted)
        cognitive_score = (urgency * 0.4 + fear * 0.3 + authority * 0.2 + reward * 0.1)

        # Build reasons list (top triggers)
        if urgency > 0.2:
            reasons.append("Urgency detected (e.g., 'immediate', 'urgent')")
        if fear > 0.2:
            reasons.append("Fear or threat detected (e.g., 'suspended', 'blocked')")
        if authority > 0.2:
            reasons.append("Authority impersonation (e.g., bank, support)")
        if reward > 0.2:
            reasons.append("Reward or lure (e.g., 'prize', 'free')")

        return round(cognitive_score, 2), reasons