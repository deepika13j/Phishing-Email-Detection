# Phishing Email Detection Using Machine Learning

## Project Overview
This project uses Machine Learning and Natural Language Processing (NLP) to classify email text into dataset labels. It includes an interactive Streamlit application and a model evaluation dashboard.

## Technologies Used
- Python
- Pandas and NumPy
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- Streamlit
- Matplotlib

## Features
- Email text classification
- Prediction confidence display
- Suspicious keyword analysis
- URL analysis
- Model accuracy evaluation
- Confusion matrix
- Dataset class distribution
- Precision, recall, and F1-score graphs
- Downloadable prediction results

## Model Performance
The current test accuracy is approximately 98.91%. Results may change when the dataset or model is updated. Accuracy alone does not establish phishing detection reliability.

## Dataset
The project combines CEAS_08 and Enron email datasets. The model currently predicts dataset labels 0 and 1. These labels should not be interpreted as safe and phishing without verifying the original dataset definitions.

## How to Run

1. Install the dependencies:

   `pip install -r requirements.txt`

2. Start the email detection application:

   `streamlit run app.py`

3. Start the evaluation dashboard in another terminal:

   `streamlit run dashboard.py`

## Disclaimer
This project is intended for educational purposes. Predictions are automated estimates and should not be treated as proof that an email is safe or malicious.