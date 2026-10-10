
import re
import ipaddress
from pathlib import Path
from urllib.parse import urlparse

import joblib
import streamlit as st


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "email_detector.joblib"

st.set_page_config(
    page_title="Email Threat Detector",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# 2. LOAD TRAINED ML MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


try:
    model = load_model()
except Exception as error:
    st.error(f"Could not load the trained model: {error}")
    st.stop()


# ==========================================
# 3. SUSPICIOUS KEYWORD ANALYSIS
# ==========================================

SUSPICIOUS_KEYWORDS = [
    "verify your account",
    "account suspended",
    "account will be suspended",
    "urgent action",
    "click here",
    "password expired",
    "confirm your password",
    "update your payment",
    "limited time",
    "claim your prize",
    "you have won",
    "send your password",
    "bank details",
    "immediately",
    "unusual activity",
    "login immediately",
    "payment failed",
    "reset your password",
]


def analyze_keywords(text):
    text_lower = text.lower()
    found = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)

    return found


# ==========================================
# 4. URL ANALYSIS
# ==========================================

def analyze_urls(text):
    pattern = r"""https?://[^\s<>"']+|www\.[^\s<>"']+"""
    urls = re.findall(pattern, text, flags=re.IGNORECASE)

    results = []
    seen = set()

    for url in urls:
        url = url.rstrip(".,!?;:)]}")
        if url in seen:
            continue
        seen.add(url)

        normalized = (
            url if re.match(r"^https?://", url, re.IGNORECASE)
            else "http://" + url
        )

        try:
            parsed = urlparse(normalized)
            hostname = parsed.hostname or ""
            reasons = []

            if not hostname:
                reasons.append("Could not identify the hostname")
            else:
                try:
                    ipaddress.ip_address(hostname)
                    reasons.append("Uses an IP address instead of a domain")
                except ValueError:
                    pass

                if hostname.startswith("xn--") or ".xn--" in hostname:
                    reasons.append("Contains an internationalized domain label")

                if hostname.count(".") >= 4:
                    reasons.append("Contains many subdomains")

            if len(url) > 75:
                reasons.append("Unusually long URL")

            if "@" in parsed.netloc:
                reasons.append("Contains an @ symbol in the address")

            if parsed.scheme.lower() != "https":
                reasons.append("Does not use HTTPS")

            results.append({
                "url": url,
                "hostname": hostname,
                "reasons": reasons
            })

        except ValueError:
            results.append({
                "url": url,
                "hostname": "",
                "reasons": ["Could not parse the URL"]
            })

    return results


# ==========================================
# 5. PAGE HEADER
# ==========================================

st.title("🛡️ Email Threat Detector")

st.markdown(
    "Analyze email text using machine learning, "
    "suspicious keyword matching, and basic URL checks."
)

st.warning(
    "Educational tool: predictions and URL indicators can be wrong. "
    "Do not use this app alone to decide whether an email is safe."
)

st.divider()


# ==========================================
# 6. EMAIL INPUT
# ==========================================

left, right = st.columns([3, 1])

with left:
    st.subheader("📩 Email Analysis")

    email_text = st.text_area(
        "Paste the email subject and body",
        height=260,
        placeholder=(
            "Subject: Urgent Account Verification\n\n"
            "Dear user,\n"
            "Please review this message..."
        ),
        key="email_input"
    )

with right:
    st.subheader("🔍 What gets checked?")
    st.markdown(
        """
        - Machine learning prediction
        - Model confidence
        - Suspicious phrases
        - URL patterns
        - Basic security indicators
        """
    )

    st.caption(
        "The app analyzes the text you provide. "
        "It does not open links or contact the sender."
    )


# ==========================================
# 7. ANALYZE EMAIL BUTTON
# ==========================================

if st.button("🔎 Analyze Email", type="primary", use_container_width=True):

    if not email_text.strip():
        st.warning("Please paste an email before analyzing.")

    else:
        st.divider()
        st.header("📊 Analysis Results")

        # Machine learning prediction
        prediction = int(model.predict([email_text])[0])

        probabilities = model.predict_proba([email_text])[0]
        classes = list(model.named_steps["classifier"].classes_)
        class_probabilities = dict(zip(classes, probabilities))

        confidence = float(class_probabilities[prediction]) * 100

        # NOTE:
        # These are dataset labels, not verified phishing labels.
        # Confirm the meaning of labels 0 and 1 before renaming them.

        result_col, confidence_col = st.columns(2)

        with result_col:
            st.subheader("Machine Learning Prediction")
            st.metric("Predicted dataset label", str(prediction))

            if prediction == 1:
                st.warning(
                    "The model classified this email as Label 1. "
                    "Verify the dataset's label definition."
                )
            else:
                st.info(
                    "The model classified this email as Label 0. "
                    "This does not prove the email is safe."
                )

        with confidence_col:
            st.subheader("Model Confidence")
            st.metric("Estimated probability", f"{confidence:.2f}%")
            st.progress(min(max(confidence / 100, 0.0), 1.0))

            st.caption(
                "This is the model's estimated probability for its "
                "predicted class, not a guarantee of correctness."
            )

        # Keyword analysis
        st.divider()
        st.subheader("🚩 Suspicious Keyword Analysis")

        keywords = analyze_keywords(email_text)

        if keywords:
            st.warning(f"Found {len(keywords)} matching phrase(s).")

            for keyword in keywords:
                st.write(f"• {keyword}")
        else:
            st.success("No phrases from the keyword list were found.")

        st.caption(
            "Keyword matches are indicators only. Legitimate emails "
            "can contain these phrases, and phishing emails can avoid them."
        )

        # URL analysis
        st.divider()
        st.subheader("🔗 URL Analysis")

        url_results = analyze_urls(email_text)

        if not url_results:
            st.info("No HTTP/HTTPS or www-style URLs were found.")
        else:
            st.write(f"URLs found: {len(url_results)}")

            for index, item in enumerate(url_results, start=1):
                with st.expander(
                    f"URL {index}: {item['hostname'] or item['url']}"
                ):
                    st.code(item["url"], language=None)

                    if item["reasons"]:
                        st.warning("Potential indicators:")

                        for reason in item["reasons"]:
                            st.write(f"• {reason}")
                    else:
                        st.info(
                            "No configured URL indicators were found. "
                            "This does not mean the URL is safe."
                        )

        # Summary
        st.divider()
        st.subheader("📝 Analysis Summary")

        summary = [
            "EMAIL THREAT DETECTOR REPORT",
            "=" * 35,
            f"Predicted dataset label: {prediction}",
            f"Model confidence: {confidence:.2f}%",
            f"Suspicious keyword matches: {len(keywords)}",
            f"URLs found: {len(url_results)}",
            "",
            "Important: This report is an automated screening result,",
            "not proof that an email is malicious or safe."
        ]

        st.text("\n".join(summary))

        st.download_button(
            label="📥 Download Analysis Report",
            data="\n".join(summary),
            file_name="email_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# ==========================================
# 8. FOOTER
# ==========================================

st.divider()

st.caption(
    "Email Threat Detector | Python • Streamlit • "
    "TF-IDF • Logistic Regression"
)