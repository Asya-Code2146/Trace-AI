# ml/train.py

import os
import numpy as np
import matplotlib
matplotlib.use('Agg') # Agar bisa jalan di server tanpa GUI
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.svm import LinearSVC # type: ignore
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score # type: ignore

from .preprocess import load_and_preprocess_data
from .features import build_feature_pipeline, transform_features
import joblib # type: ignore

# Mapping label yang disimpan
LABEL_MAP = {0: "legitimate", 1: "suspicious", 2: "scam"}

def train_and_evaluate():
    """Pipeline lengkap: Load -> Fitur -> Train -> Evaluasi -> Save."""
    
    # 1. Load & Preprocess
    csv_path = 'data/raw/dummy_dataset.csv'
    X_train, X_test, y_train, y_test, le = load_and_preprocess_data(csv_path)

    # 2. Feature Engineering
    X_train_vec = build_feature_pipeline(X_train)
    X_test_vec = transform_features(X_test)

    # 3. Definisikan Models (Baseline)
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Linear SVM": LinearSVC(random_state=42)
    }

    best_model = None
    best_f1 = 0
    best_name = ""

    # 4. Train & Evaluate
    for name, model in models.items():
        print(f"\n--- Melatih {name} ---")
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        
        # Metrik
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=list(LABEL_MAP.values())))
        
        # Ambil F1-score rata-rata (macro) untuk pembandingan
        report = classification_report(y_test, y_pred, output_dict=True, target_names=list(LABEL_MAP.values()))
        macro_f1 = report['macro avg']['f1-score'] # type: ignore
        
        if macro_f1 > best_f1: # type: ignore
            best_f1 = macro_f1
            best_model = model
            best_name = name

    print(f"\n✅ Model terbaik berdasarkan Macro F1-Score: {best_name} (F1: {best_f1:.4f})")

    # 5. Simpan Model Terbaik
    model_path = 'ml/saved_models/best_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Model disimpan di {model_path}")

    # 6. Buat Confusion Matrix untuk model terbaik
    print("Menyimpan hasil evaluasi...")
    y_pred_best = best_model.predict(X_test_vec) # type: ignore
    cm = confusion_matrix(y_test, y_pred_best)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=list(LABEL_MAP.values()), 
                yticklabels=list(LABEL_MAP.values()))
    plt.title(f'Confusion Matrix - {best_name} (Dummy Data)')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    
    os.makedirs('ml/saved_models', exist_ok=True)
    plt.savefig('ml/saved_models/confusion_matrix.png')
    print("Confusion matrix disimpan di ml/saved_models/confusion_matrix.png")

if __name__ == "__main__":
    train_and_evaluate()