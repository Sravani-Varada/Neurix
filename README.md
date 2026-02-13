# 🔒 SecureDrop AI  
### Intelligent Download Risk Advisor

SecureDrop AI is an AI-powered file risk assessment tool designed to help users evaluate potential threats before opening downloaded files.

It analyzes structural characteristics of files using anomaly detection and behavioral indicators to classify risk levels as **Low, Medium, or High**.

---

## 🚀 Key Features

- 🔍 **Anomaly Detection (Isolation Forest)**
- 📊 **Entropy Analysis** (detects randomness / packing)
- 🧠 **Statistical Baseline Modeling**
- 📁 **Double Extension Detection** (e.g., `invoice.pdf.exe`)
- ⚙️ **Executable Signature Detection (MZ header)**
- 📈 **Circular Risk Gauge Visualization**
- 🎨 Modern Cyber-Themed UI
- 📄 Structured Technical Breakdown Panel

---

## 🧠 How It Works

SecureDrop AI models normal file characteristics using a synthetic statistical baseline and evaluates uploaded files using anomaly detection.

### Risk Score Composition

| Component | Weight |
|------------|--------|
| Anomaly Score | 50% |
| Entropy Analysis | 20% |
| Double Extension Detection | 15% |
| Executable Signature Detection | 15% |

The final output classifies files into:

- 🟢 **LOW Risk**
- 🟡 **MEDIUM Risk**
- 🔴 **HIGH Risk**

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **NumPy**
- **Scikit-learn (Isolation Forest)**
- 
---

## 🎯 Intended Use Case

SecureDrop AI is designed as a **download safety advisor** that:

- Helps users assess potential risks
- Encourages safer file handling practices
- Improves awareness of common attack patterns

It is not a replacement for antivirus software but serves as a proactive risk analysis layer.

---

## ⚠ Disclaimer

This tool performs structural risk analysis and does not guarantee malware detection.  
Always use trusted antivirus software for complete protection.

---

## 📌 Future Improvements

- Batch file analysis
- PDF report export
- Threat intelligence API integration
- Advanced feature modeling
- Deployment version (Cloud)
