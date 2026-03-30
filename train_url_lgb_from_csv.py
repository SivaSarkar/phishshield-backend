# train_url_lgb_from_csv.py
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ''
    return [
        len(url),
        sum(c.isdigit() for c in url) / max(len(url), 1),
        sum(c in '-_@?=&%' for c in url),
        hostname.count('.'),
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0,
        1 if any(s in url for s in ['bit.ly','tinyurl','goo.gl','t.co']) else 0,
        1 if url.startswith('https') else 0,
        1 if '@' in url else 0,
        1 if '//' in url[7:] else 0,
        len(parsed.path),
        len(parsed.query)
    ]

print("Loading CSV dataset...")
df = pd.read_csv('data/raw/url/url_subset_20k.csv')
print(f"Loaded {len(df)} URLs")

print("Extracting features...")
X = np.array([extract_features(url) for url in df['url']])
y = df['label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training LightGBM...")
model = lgb.LGBMClassifier(num_leaves=31, learning_rate=0.05, n_estimators=100, verbose=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ URL model accuracy: {acc:.4f}")

joblib.dump(model, 'models/url_lgb.pkl')
print("✅ Model saved to models/url_lgb.pkl")