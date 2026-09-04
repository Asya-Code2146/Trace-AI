# ml/evaluate.py

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score # type: ignore
import joblib # type: ignore
import pandas as pd

from .preprocess import clean_text

LABEL_MAP = {0: "legitimate", 1: "suspicious", 2: "scam"}

def evaluate_saved_model(csv_test_path: str = "data/raw/dummy_dataset.csv"):
    """
    Memuat model dan vectorizer yang sudah disimpan, lalu mengevaluasi 
    menggunakan data dari csv_test_path.
    """
    print("Memuat model dan vectorizer...")
    model = joblib.load('ml/saved_models/best_model.pkl')
    tfidf = joblib.load('ml/saved_models/tfidf_vectorizer.pkl')
    le = joblib.load('ml/saved_models/label_encoder.pkl')

    # Load data (dalam kasus nyata, ini adalah data uji terpisah)
    df = pd.read_csv(csv_test_path)
    df['clean_text'] = df['text'].apply(clean_text)

    numeric_features = [
        'has_url', 'has_phone', 'has_email', 'asks_for_payment', 
        'asks_for_otp', 'has_urgency', 'has_threat', 
        'has_unrealistic_reward', 'has_company_name', 'has_official_domain',
        'suspicious_keyword_count'
    ]

    # Transform fitur
    X_tfidf = tfidf.transform(df['clean_text'])
    X_numeric = df[numeric_features].values
    
    from scipy.sparse import hstack # type: ignore
    X_vec = hstack([X_tfidf, X_numeric])
    
    y_true = le.transform(df['label'])

    # Prediksi
    print("Melakukan prediksi...")
    y_pred = model.predict(X_vec)

    # Evaluasi
    print("\n" + "="*40)
    print("EVALUASI MODEL")
    print("="*40)
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=list(LABEL_MAP.values())))

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                xticklabels=list(LABEL_MAP.values()), 
                yticklabels=list(LABEL_MAP.values()))
    plt.title('Evaluasi Model Tersimpan')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.savefig('ml/saved_models/eval_confusion_matrix.png')
    print("Confusion matrix disimpan di ml/saved_models/eval_confusion_matrix.png")

if __name__ == "__main__":
    evaluate_saved_model()