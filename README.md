# 🛡️ Email Threat Detector

A machine learning-based email classification project that analyzes email text using TF-IDF, Logistic Regression, suspicious keyword matching, and basic URL checks.

The project includes an interactive Streamlit application and an evaluation dashboard to explore model performance.

## ✨ Features

- **Email Classification:** Predicts the dataset class of an email using machine learning.
- **Confidence Score:** Displays the model's estimated probability for its prediction.
- **Suspicious Keyword Detection:** Identifies potentially concerning phrases in email text.
- **URL Analysis:** Checks for basic URL patterns.
- **Evaluation Dashboard:** Displays model accuracy and a confusion matrix.
- **Performance Metrics:** Shows precision, recall, and F1-score.
- **Dataset Distribution:** Visualizes the number of emails in each class.
- **Downloadable Report:** Allows prediction results to be downloaded as a CSV file.

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- Streamlit
- Matplotlib
- Seaborn
- Joblib

## 📸 Project Screenshots

### 1. Email Input
![Email Input](app_input.png)

### 2. Email Analysis Results
![Email Analysis](app_analysis.png)

### 3. Analysis Report
![Analysis Report](app_report.png)

### 4. Confusion Matrix
![Confusion Matrix](https://github.com/deepika13j/Phishing-Email-Detection/blob/main/Confusion%20matrix.png?raw=true)

### 5. Dataset Class Distribution
![Class Distribution](https://github.com/deepika13j/Phishing-Email-Detection/blob/main/Class%20distribution.png?raw=true)

### 6. Model Performance Metrics
![Performance Metrics](https://github.com/deepika13j/Phishing-Email-Detection/blob/main/Performance%20metrics.png?raw=true)

## 📊 Model Evaluation

The model achieved approximately **98.91% accuracy** on the test split used during evaluation.

The dashboard provides:
- Accuracy
- Confusion matrix
- Classification report
- Precision
- Recall
- F1-score

Accuracy alone does not establish that a model can reliably identify phishing emails. Performance depends on the dataset, its labels, and how representative the test data is.

## 📂 Project Structure

```text
Phishing-Email-Detection/
├── app.py
├── dashboard.py
├── requirements.txt
├── README.md
├── screenshots/
├── data/
│   └── processed/
├── models/
└── results/
```

## 🚀 Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/deepika13j/Phishing-Email-Detection.git
cd Phishing-Email-Detection
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the email analysis application

```bash
streamlit run app.py
```

### 4. Run the evaluation dashboard

```bash
streamlit run dashboard.py
```

**Note:** The application and dashboard require the trained model and processed dataset at the file paths configured in the Python scripts. The dataset and model must be available locally for the commands to work.

## ⚠️ Disclaimer

This project is intended for educational purposes. Predictions, confidence scores, keyword matches, and URL indicators may be incorrect.

Dataset labels should not be interpreted as definitively safe or phishing unless their original definitions have been verified. Do not rely on this application alone to decide whether an email is safe.
