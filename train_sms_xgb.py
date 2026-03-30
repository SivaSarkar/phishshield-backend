# train_sms_xgb.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib
import os

# Load dataset
df = pd.read_csv('data/sms/sms_phishing.csv')  # adjust filename

# Assuming columns: 'text' and 'label' (1=phishing, 0=legitimate)
X = df['text']
y = df['label']

# TF-IDF features (500 dimensions for speed)
vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Train XGBoost (lightweight settings)
model = xgb.XGBClassifier(
    n_estimators=100,        # fewer trees for speed
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"✅ XGBoost Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/sms_xgb.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
print("✅ Saved to models/sms_xgb.pkl and models/tfidf_vectorizer.pkl")