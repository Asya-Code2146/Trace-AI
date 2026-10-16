from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.compose import ColumnTransformer # type: ignore
from scipy.sparse import hstack # type: ignore
import joblib # type: ignore

def build_feature_pipeline(X_train):
    """
    Membangun pipeline TF-IDF untuk teks dan menggabungkannya dengan fitur numerik.
    """
    print("Membangun pipeline TF-IDF...")
    
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    
    X_train_tfidf = tfidf.fit_transform(X_train['clean_text'])
    
    joblib.dump(tfidf, 'ml/saved_models/tfidf_vectorizer.pkl')

    numeric_features = [
        'has_url', 'has_phone', 'has_email', 'asks_for_payment', 
        'asks_for_otp', 'has_urgency', 'has_threat', 
        'has_unrealistic_reward', 'has_company_name', 'has_official_domain',
        'suspicious_keyword_count'
    ]
    X_train_numeric = X_train[numeric_features].values

    X_train_combined = hstack([X_train_tfidf, X_train_numeric])

    return X_train_combined

def transform_features(X_data):
    """
    Dia mengubah data baru (uji/inferensi) menggunakan TF-IDF yang sudah di-fit.
    """
    tfidf = joblib.load('ml/saved_models/tfidf_vectorizer.pkl')
    
    X_data_tfidf = tfidf.transform(X_data['clean_text'])
    
    numeric_features = [
        'has_url', 'has_phone', 'has_email', 'asks_for_payment', 
        'asks_for_otp', 'has_urgency', 'has_threat', 
        'has_unrealistic_reward', 'has_company_name', 'has_official_domain',
        'suspicious_keyword_count'
    ]
    X_data_numeric = X_data[numeric_features].values

    X_data_combined = hstack([X_data_tfidf, X_data_numeric])
    return X_data_combined
