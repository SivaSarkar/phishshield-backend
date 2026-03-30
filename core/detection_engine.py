# core/detection_engine.py
import joblib
import numpy as np
import re
from urllib.parse import urlparse
import tldextract
import onnxruntime as ort

# Global variables for lazy loading
_sms_model = None
_tfidf = None
_url_model = None
_mobilebert_session = None

def _load_sms_model():
    global _sms_model, _tfidf
    if _sms_model is None:
        print("Loading SMS model...")
        _sms_model = joblib.load('models/sms_xgb.pkl')
        _tfidf = joblib.load('models/tfidf_vectorizer.pkl')
    return _sms_model, _tfidf

def _load_url_model():
    global _url_model
    if _url_model is None:
        print("Loading URL model...")
        _url_model = joblib.load('models/url_lgb.pkl')
    return _url_model

def _load_mobilebert():
    global _mobilebert_session
    if _mobilebert_session is None:
        print("Loading MobileBERT model...")
        _mobilebert_session = ort.InferenceSession(
            "models/model_quantized.onnx",
            providers=["CPUExecutionProvider"]
        )
    return _mobilebert_session

def extract_url_features(url: str):
    """Extract 11 features for URL phishing detection"""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    
    return [
        len(url),                                           # url_length
        sum(c.isdigit() for c in url) / max(len(url), 1),   # digit_ratio
        sum(c in '-_@?=&%' for c in url),                   # special_char_count
        hostname.count('.'),                                # subdomain_count
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0,  # has_ip
        1 if any(s in url for s in ['bit.ly','tinyurl','goo.gl','t.co']) else 0,  # is_shortened
        1 if url.startswith('https') else 0,                # has_https
        1 if '@' in url else 0,                             # has_at_symbol
        1 if '//' in url[7:] else 0,                        # has_double_slash
        len(parsed.path),                                   # path_length
        len(parsed.query),                                  # query_length
    ]

def predict_sms_phishing(text: str) -> float:
    """Return phishing probability (0-1) for SMS/email text (Python float)"""
    model, tfidf = _load_sms_model()
    vec = tfidf.transform([text])
    prob = model.predict_proba(vec)[0][1]
    return float(prob)  # Convert numpy.float to Python float

def predict_url_phishing(url: str) -> float:
    """Return phishing probability (0-1) for URL (Python float)"""
    model = _load_url_model()
    features = np.array([extract_url_features(url)], dtype=np.float32)
    prob = model.predict_proba(features)[0][1]
    return float(prob)  # Convert numpy.float to Python float

def get_mobilebert_embedding(text: str):
    """Get semantic embedding from MobileBERT (optional)"""
    session = _load_mobilebert()
    return None