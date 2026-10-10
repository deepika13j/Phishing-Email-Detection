
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project folders
PROJECT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT / "data" / "processed" / "phishing_emails.csv"
MODEL_DIR = PROJECT / "models"
RESULTS_DIR = PROJECT / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATA_FILE)

X = df["text"].fillna("").astype(str)
y = df["label"].astype(int)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training emails:", len(X_train))
print("Testing emails:", len(X_test))

# Build the machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=100000,
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# Train the model
print("\nTraining model...")
model.fit(X_train, y_train)

# Evaluate the model
print("\nEvaluating model...")
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
report = classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Label 0", "Label 1"],
    zero_division=0
)

print(f"\nAccuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
print("\nConfusion Matrix:")
print(matrix)
print("\nClassification Report:")
print(report)

# Save the trained model
model_path = MODEL_DIR / "email_detector.joblib"
joblib.dump(model, model_path)

# Save evaluation results
results_path = RESULTS_DIR / "evaluation.txt"
with open(results_path, "w", encoding="utf-8") as file:
    file.write(f"Accuracy: {accuracy:.4f}\n\n")
    file.write("Confusion Matrix:\n")
    file.write(str(matrix))
    file.write("\n\nClassification Report:\n")
    file.write(report)

print("\nModel saved to:", model_path)
print("Evaluation saved to:", results_path)