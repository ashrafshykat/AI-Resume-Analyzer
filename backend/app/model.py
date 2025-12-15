from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_DIR.mkdir(exist_ok=True)

# -------------------------------
# Save Model
# -------------------------------
def save_model(
    vectorizer: TfidfVectorizer,
    clf: LogisticRegression,
    label_encoder: LabelEncoder,
    out_dir: Path = MODEL_DIR
):
    """Save trained model, vectorizer, and label encoder"""
    joblib.dump(vectorizer, out_dir / "vectorizer.joblib")
    joblib.dump(clf, out_dir / "classifier.joblib")
    joblib.dump(label_encoder, out_dir / "label_encoder.joblib")

# -------------------------------
# Load Model
# -------------------------------
def load_model(out_dir: Path = MODEL_DIR):
    """Load trained model, vectorizer, and label encoder"""
    vect = joblib.load(out_dir / "vectorizer.joblib")
    clf = joblib.load(out_dir / "classifier.joblib")
    label_encoder = joblib.load(out_dir / "label_encoder.joblib")
    return vect, clf, label_encoder

# -------------------------------
# Check Model Exists
# -------------------------------
def model_exists(out_dir: Path = MODEL_DIR) -> bool:
    """Check if model files exist"""
    return (
        (out_dir / "vectorizer.joblib").exists()
        and (out_dir / "classifier.joblib").exists()
        and (out_dir / "label_encoder.joblib").exists()
    )
