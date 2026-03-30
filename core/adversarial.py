# core/adversarial.py
import joblib
import numpy as np

_iso_forest = None
_adv_vectorizer = None

def load_adversarial_models():
    global _iso_forest, _adv_vectorizer
    if _iso_forest is None:
        try:
            _iso_forest = joblib.load('models/adv_iforest.pkl')
            _adv_vectorizer = joblib.load('models/adv_vectorizer.pkl')
        except Exception as e:
            print(f"Warning: Adversarial models not found: {e}")
            _iso_forest = None
            _adv_vectorizer = None
    return _iso_forest, _adv_vectorizer

def is_adversarial(text):
    """Return True if input is adversarial (anomaly). Returns Python bool."""
    iso, vec = load_adversarial_models()
    if iso is None or vec is None:
        return False
    try:
        X = vec.transform([text]).toarray()
        # IsolationForest returns -1 (anomaly) or 1 (normal)
        # Convert numpy.int64 to Python int, then compare
        result = int(iso.predict(X)[0])
        return result == -1  # This returns a Python bool
    except Exception as e:
        print(f"Adversarial detection error: {e}")
        return False