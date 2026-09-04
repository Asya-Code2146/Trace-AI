import re
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack

from .preprocess import clean_text

LABEL_MAP_REVERSE = {0: "legitimate", 1: "suspicious", 2: "scam"}

def _extract_heuristic_features(text: str) -> dict:
    text_lower = text.lower()
    return {
        "has_url": 1 if re.search(r'http|www|\.com|\.id', text_lower) else 0,
        "has_phone": 1 if re.search(r'\b\d{10,13}\b', text_lower) else 0,
        "has_email": 1 if re.search(r'@\w+\.\w+', text_lower) else 0,
        "asks_for_payment": 1 if re.search(r'transfer|bayar|biaya|dp|admin', text_lower) else 0,
        "asks_for_otp": 1 if 'otp' in text_lower else 0,
        "has_urgency": 1 if re.search(r'segera|cepat|hari ini|terakhir|kuota', text_lower) else 0,
        "has_threat": 1 if re.search(r'blokir|hapus|dilarang|pidana|dicabut', text_lower) else 0,
        "has_unrealistic_reward": 1 if re.search(r'pasti|garansi|juta|profit|hadiah', text_lower) else 0,
        "has_company_name": 1 if re.search(r'pt\.|cv\.|inc\.|corp', text_lower) else 0,
        "has_official_domain": 1 if re.search(r'\.co\.id|\.go\.id|\.ac\.id', text_lower) else 0,
        "suspicious_keyword_count": len(re.findall(r'gratis|murah|hadiah|menang|verifikasi|klik', text_lower))
    }

def predict_ml(text: str, case_type: str, predefined_features: dict = None) -> dict: # type: ignore
    try:
        if not text:
            return {
                "ml_prediction": "unknown",
                "ml_probability": 0.0,
                "ml_probabilities": {},
                "ml_status": "skipped_no_text"
            }

        model = joblib.load('ml/saved_models/best_model.pkl')
        tfidf = joblib.load('ml/saved_models/tfidf_vectorizer.pkl')
        le = joblib.load('ml/saved_models/label_encoder.pkl')

        features = predefined_features or _extract_heuristic_features(text)
        features['clean_text'] = clean_text(text)

        numeric_features = [
            'has_url', 'has_phone', 'has_email', 'asks_for_payment',
            'asks_for_otp', 'has_urgency', 'has_threat',
            'has_unrealistic_reward', 'has_company_name', 'has_official_domain',
            'suspicious_keyword_count'
        ]

        df = pd.DataFrame([features])

        X_tfidf = tfidf.transform(df['clean_text'])
        X_numeric = df[numeric_features].values
        X_vec = hstack([X_tfidf, X_numeric])

        pred_encoded = model.predict(X_vec)[0]

        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X_vec)[0]
            confidence = float(np.max(probas))
            prob_details = {}
            for i, p in enumerate(probas):
                label_name = le.inverse_transform([i])[0]
                prob_details[label_name] = round(float(p), 4)
        else:
            confidence = 1.0 if pred_encoded == 1 else 0.8
            prob_details = {"unknown": confidence}

        label_str = le.inverse_transform([pred_encoded])[0]

        return {
            "ml_prediction": label_str,
            "ml_probability": round(confidence, 4),
            "ml_probabilities": prob_details,
            "ml_status": "success"
        }

    except Exception as e:
        return {
            "ml_prediction": "unknown",
            "ml_probability": 0.0,
            "ml_probabilities": {},
            "ml_status": f"failed: {str(e)}"
        }