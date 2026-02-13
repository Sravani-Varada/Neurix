import streamlit as st
import numpy as np
import string
from sklearn.ensemble import IsolationForest

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="SecureDrop AI", layout="centered")

# ----------------------------
# CYBER GREEN THEME
# ----------------------------
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
.stApp {
    background: radial-gradient(circle at top left, #0f2e1c, #050a07);
    color: #00ff88;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADINGS */
h1, h2, h3 {
    color: #00ff88;
    text-shadow: 0 0 8px rgba(0, 255, 136, 0.6);
}

/* SECTION BOX */
.section-box {
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(145deg, #0a1f14, #07130d);
    border: 1px solid rgba(0,255,136,0.4);
    box-shadow: 0 0 15px rgba(0,255,136,0.15);
    margin-bottom: 18px;
    transition: 0.3s ease;
}

.section-box:hover {
    box-shadow: 0 0 25px rgba(0,255,136,0.4);
}

/* RISK CARD */
.risk-card {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    animation: fadeIn 0.6s ease-in-out;
}

/* LOW */
.low {
    background: linear-gradient(90deg, #00c853, #00ff88);
    color: black;
}

/* MEDIUM */
.medium {
    background: linear-gradient(90deg, #ff9800, #ffc107);
    color: black;
}

/* HIGH */
.high {
    background: linear-gradient(90deg, #b71c1c, #ff1744);
    color: white;
    box-shadow: 0 0 20px rgba(255,0,0,0.6);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    border: 1px solid rgba(0,255,136,0.6);
    border-radius: 12px;
    padding: 12px;
    background-color: #0a1a12;
}

/* ANIMATION */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Synthetic Baseline
# ----------------------------
def generate_baseline(n=500):
    entropy = np.random.normal(4.8, 0.6, n)
    printable_ratio = np.random.normal(0.9, 0.05, n)
    size_kb = np.abs(np.random.normal(200, 100, n))
    double_ext = np.zeros(n)
    exe_flag = np.zeros(n)
    symbol_density = np.random.normal(0.08, 0.04, n)

    return np.column_stack([
        entropy,
        printable_ratio,
        size_kb,
        double_ext,
        exe_flag,
        symbol_density
    ])

baseline = generate_baseline()
model = IsolationForest(contamination=0.15, random_state=42)
model.fit(baseline)

# ----------------------------
# Feature Extraction
# ----------------------------
def calculate_entropy(data):
    if len(data) == 0:
        return 0
    counts = np.bincount(data)
    probs = counts / len(data)
    probs = probs[counts > 0]
    return -np.sum(probs * np.log2(probs))

def extract_features(file_bytes, filename):
    data = np.frombuffer(file_bytes, dtype=np.uint8)

    entropy = calculate_entropy(data)
    printable = sum(chr(b) in string.printable for b in file_bytes)
    printable_ratio = printable / len(file_bytes) if len(file_bytes) else 0
    size_kb = len(file_bytes) / 1024
    double_ext = 1 if filename.count('.') > 1 else 0
    exe_flag = 1 if file_bytes[:2] == b'MZ' else 0
    symbol_density = sum(chr(b) in "!@#$%^&*()_+-=" for b in file_bytes) / len(file_bytes) if len(file_bytes) else 0

    return np.array([[entropy, printable_ratio, size_kb,
                      double_ext, exe_flag, symbol_density]])

# ----------------------------
# Risk Calculation
# ----------------------------
def calculate_risk(features):
    raw_score = model.decision_function(features)[0]
    anomaly_score = -raw_score
    anomaly_score = 1 / (1 + np.exp(-anomaly_score * 5))

    entropy = features[0][0]
    double_ext = features[0][3]
    exe_flag = features[0][4]

    entropy_risk = min(entropy / 8, 1)

    risk_score = (
        0.5 * anomaly_score +
        0.2 * entropy_risk +
        0.15 * double_ext +
        0.15 * exe_flag
    )

    risk_score = max(0, min(risk_score, 1))

    if risk_score < 0.35:
        level = "LOW"
    elif risk_score < 0.7:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return risk_score, level

# ----------------------------
# Circular Gauge
# ----------------------------
def risk_gauge(risk_score):
    percentage = int(risk_score * 100)

    gauge_html = f"""
    <div style="display:flex; justify-content:center; margin-bottom:20px;">
        <div style="
            width:160px;
            height:160px;
            border-radius:50%;
            background:conic-gradient(
                #00ff88 {percentage*3.6}deg,
                #1a1a1a {percentage*3.6}deg
            );
            display:flex;
            align-items:center;
            justify-content:center;
            box-shadow:0 0 20px rgba(0,255,136,0.5);
        ">
            <div style="
                width:120px;
                height:120px;
                border-radius:50%;
                background:#0E1117;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#00ff88;
                font-size:24px;
                font-weight:bold;
            ">
                {percentage}%
            </div>
        </div>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)

# ----------------------------
# UI Header
# ----------------------------
st.markdown("""
<h1 style='text-align: center;'>
🔒 SecureDrop AI
</h1>
<h4 style='text-align: center; color:#00ffaa;'>
Intelligent Download Risk Advisor
</h4>
""", unsafe_allow_html=True)

st.write("Upload a file to assess potential security risk before opening it.")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader("Upload a file (Max 10MB)")

if uploaded_file:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("File too large. Maximum size is 10MB.")
    else:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name

        features = extract_features(file_bytes, filename)
        risk_score, level = calculate_risk(features)

        # File Overview
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📄 File Overview")
        st.write(f"**File Name:** {filename}")
        st.write(f"**File Size:** {round(len(file_bytes)/1024,2)} KB")
        st.markdown('</div>', unsafe_allow_html=True)

        # Risk Assessment
        st.subheader("⚠ Risk Assessment")
        risk_gauge(risk_score)

        risk_percentage = round(risk_score * 100, 2)

        if level == "LOW":
            risk_class = "low"
        elif level == "MEDIUM":
            risk_class = "medium"
        else:
            risk_class = "high"

        st.markdown(f"""
        <div class="risk-card {risk_class}">
        Risk Level: {level} <br>
        Risk Score: {risk_percentage}%
        </div>
        """, unsafe_allow_html=True)

        # Indicators
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🚨 Detected Indicators")

        if filename.count('.') > 1:
            st.write("• Double extension detected")

        if file_bytes[:2] == b'MZ':
            st.write("• Executable file signature detected")

        if features[0][0] > 7:
            st.write("• High entropy detected")

        st.markdown('</div>', unsafe_allow_html=True)

        # Recommendations
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🛡 Recommended Actions")

        if level == "LOW":
            st.write("• Open normally but ensure antivirus is active.")
        elif level == "MEDIUM":
            st.write("• Scan with antivirus before opening.")
            st.write("• Avoid enabling macros or scripts.")
        else:
            st.write("• DO NOT open the file.")
            st.write("• Verify the source.")
            st.write("• Upload to VirusTotal for further analysis.")

        st.markdown('</div>', unsafe_allow_html=True)

        # Technical Details
        with st.expander("🔍 Technical Details"):
            feature_names = [
                "Entropy",
                "Printable Ratio",
                "File Size (KB)",
                "Double Extension Flag",
                "Executable Signature Flag",
                "Symbol Density"
            ]

            for name, value in zip(feature_names, features[0]):
                st.write(f"**{name}:** {round(value, 4)}")

            st.write("**Model:** IsolationForest (Anomaly Detection)")
