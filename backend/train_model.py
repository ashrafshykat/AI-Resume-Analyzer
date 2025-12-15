"""
Training script to generate and train the resume classifier model
"""

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from app.model import save_model

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text

DATASET_PATH = "./backend/data/UpdatedResumeDataSet.csv"

def train_classifier():

    df = pd.read_csv(DATASET_PATH)

    required_cols = {"Resume", "Category"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dataset must contain columns: {required_cols}")

    df["CleanResume"] = df["Resume"].astype(str).apply(clean_text)

    label_encoder = LabelEncoder()
    df["MappedCategory"] = label_encoder.fit_transform(df["Category"])

    texts = df["CleanResume"].tolist()
    labels = df["MappedCategory"].tolist()

    print(f"Training samples: {len(texts)}")
    print("Detected classes:", list(label_encoder.classes_))

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    clf = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    X = vectorizer.fit_transform(texts)
    clf.fit(X, labels)

    save_model(vectorizer, clf, label_encoder)

    print("Model trained and saved successfully!")

    test_text = clean_text(
        "Python backend developer with 3 years of experience in Django and FastAPI"
    )

    X_test = vectorizer.transform([test_text])
    pred_label = clf.predict(X_test)[0]
    confidence = clf.predict_proba(X_test)[0].max()

    predicted_category = label_encoder.inverse_transform([pred_label])[0]

    print(
        f"\nTest prediction: {predicted_category} "
        f"(confidence: {confidence:.2f})"
    )


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    train_classifier()
