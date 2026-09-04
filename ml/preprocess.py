# ml/preprocess.py

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore
import joblib # type: ignore
import os

def clean_text(text):
    """Membersihkan teks dari karakter aneh dan menstandardisasi atau anomali tak di kenal dan membahayakan."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Hapus karakter spesial kecuali spasi
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Hilangkan spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_preprocess_data(csv_path: str, test_size: float = 0.2):
    """
    Memuat data, membersihkan, memisahkan fitur/label, dan melakukan split.
    Mengembalikan data yang siap untuk feature engineering.
    """
    print(f"Memuat data dari {csv_path}...")
    df = pd.read_csv(csv_path)

    # Cleaning teks
    print("Membersihkan teks...")
    df['clean_text'] = df['text'].apply(clean_text)

    # Encoding Label (legitimate=0, suspicious=1, scam=2)
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df['label']) # type: ignore
    
    # Simpan label encoder untuk inference nanti
    os.makedirs('ml/saved_models', exist_ok=True)
    joblib.dump(le, 'ml/saved_models/label_encoder.pkl')

    # Kolom fitur numerik (binary)
    numeric_features = [
        'has_url', 'has_phone', 'has_email', 'asks_for_payment', 
        'asks_for_otp', 'has_urgency', 'has_threat', 
        'has_unrealistic_reward', 'has_company_name', 'has_official_domain',
        'suspicious_keyword_count'
    ]

    # Split data
    print("Membagi data latih dan uji...")
    X_train, X_test, y_train, y_test = train_test_split(
        df[['clean_text'] + numeric_features],
        df['label_encoded'],
        test_size=test_size,
        random_state=42,
        stratify=df['label_encoded'] # Pastikan distribusi label seimbang
    )

    print(f"Data latih: {len(X_train)} baris, Data uji: {len(X_test)} baris")
    return X_train, X_test, y_train, y_test, le