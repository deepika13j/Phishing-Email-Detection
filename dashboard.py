
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

st.set_page_config(
    page_title="Email Detection Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Email Detection Model Evaluation")
st.write("Performance dashboard for the trained email classifier.")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed" / "phishing_emails.csv"
MODEL_FILE = BASE_DIR / "models" / "email_detector.joblib"

if not DATA_FILE.exists() or not MODEL_FILE.exists():
    st.error("Dataset or trained model not found. Check your project folders.")
    st.stop()

df = pd.read_csv(DATA_FILE)
df = df.dropna(subset=["text", "label"])

model = joblib.load(MODEL_FILE)

X = df["text"].astype(str)
y = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Emails", f"{len(df):,}")
col2.metric("Test Emails", f"{len(y_test):,}")
col3.metric("Model Accuracy", f"{accuracy * 100:.2f}%")

st.divider()

# Confusion matrix
st.subheader("Confusion Matrix")

fig, ax = plt.subplots(figsize=(5, 4))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    ax=ax,
    cmap="Blues",
    values_format="d"
)

ax.set_title("Actual vs Predicted Labels")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption("Rows represent actual labels; columns represent predicted labels.")

# Dataset distribution
st.subheader("Dataset Class Distribution")

label_counts = y.value_counts().sort_index()

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(
    label_counts.index.astype(str),
    label_counts.values
)

ax.set_xlabel("Dataset Label")
ax.set_ylabel("Number of Emails")
ax.set_title("Number of Emails in Each Label")

ax.bar_label(bars, fmt="%.0f")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Classification report
st.subheader("Classification Report")

report = classification_report(
    y_test,
    y_pred,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report).transpose()
st.dataframe(report_df.round(3), use_container_width=True)

# Precision, recall and F1-score graph
st.subheader("Precision, Recall and F1-Score")

class_metrics = report_df.loc[
    [str(label) for label in sorted(y.unique())],
    ["precision", "recall", "f1-score"]
]

fig, ax = plt.subplots(figsize=(8, 4))

class_metrics.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Dataset Label")
ax.set_ylabel("Score")
ax.set_ylim(0, 1.05)
ax.set_title("Model Performance by Label")
ax.legend(loc="lower right")
ax.tick_params(axis="x", rotation=0)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Download report
st.subheader("Download Results")

download_df = pd.DataFrame({
    "Actual Label": y_test.reset_index(drop=True),
    "Predicted Label": pd.Series(y_pred)
})

st.download_button(
    "Download Predictions CSV",
    data=download_df.to_csv(index=False).encode("utf-8"),
    file_name="email_predictions.csv",
    mime="text/csv"
)

st.info(
    "Label 0 and Label 1 are dataset classes. "
    "They should not be interpreted as safe and phishing until "
    "the dataset labels are verified."
)
