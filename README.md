# 🛡️ ShadowTrace AI

> **An AI-powered cybersecurity threat intelligence dashboard built with Python & Streamlit.**

ShadowTrace AI helps users identify suspicious digital activities, analyze potential cybersecurity threats, and visualize security-related findings through an interactive, dark-themed dashboard — all in a single Python file.

---

## 📸 Features

| Module | Description |
|---|---|
| **🏠 Dashboard** | Real-time KPIs, 24-hour threat activity chart, top attack origins, severity breakdown cards, and a live event feed |
| **🔍 Threat Analyzer** | Enter any IP or domain to get a risk score, threat level, open ports table, AI findings, and recommendations |
| **📋 Log Scanner** | Paste firewall/auth/IDS logs — keyword-based AI flags SQL injection, brute force, port scans, privilege escalation, and more |
| **ℹ️ About** | Tech stack overview and explanation of how each module works |

---

## 🎨 Design

- Dark background (`#0a0e1a`) with **neon blue** (`#00d4ff`) and **purple** (`#a855f7`) accents
- Color-coded severity badges: 🔴 Critical · 🟠 High · 🟡 Medium · 🟢 Low
- Glowing card boxes and custom CSS animations
- Sidebar toggle for **auto-refresh** (5–60 s) on the dashboard

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** — web UI framework
- **Pandas** — data handling
- **random / datetime / time** — standard library (no extra installs)

---

## ⚡ Quick Start

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/shadowtrace-ai.git
cd shadowtrace-ai
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
shadowtrace-ai/
│
├── app.py          # Entire application (single file)
└── README.md       # This file
```

---

## 🧠 How the AI Works

ShadowTrace AI uses **simulated AI logic** — great for learning and demonstration:

| Module | Technique |
|---|---|
| **Threat Analyzer** | Random risk scoring + simulated port/service enumeration |
| **Log Scanner** | Keyword-pattern matching with confidence scoring |
| **Dashboard** | Randomly generated telemetry refreshed on demand or on a timer |

All data is **randomly generated** for demonstration purposes. No real network traffic is monitored.

---

## 🔑 Key Concepts Demonstrated

- Streamlit page layout, sidebar navigation, and session state
- Custom CSS injection for a professional dark theme
- `pandas` DataFrames displayed as interactive tables
- `st.line_chart` / `st.bar_chart` for data visualization
- Spinner (`st.spinner`) and `time.sleep()` to simulate async processing
- Color-coded alert boxes using `st.markdown` + `unsafe_allow_html`

---

## 📋 Sample Log (for testing)

Paste this into the **Log Scanner** page (or click "Load Sample Log"):

```
2024-01-15 03:22:11 FAILED LOGIN attempt from 192.168.1.105 (admin)
2024-01-15 03:22:14 FAILED LOGIN attempt from 192.168.1.105 (root)
2024-01-15 03:22:18 SQL query detected: SELECT * FROM users WHERE id=1 OR 1=1
2024-01-15 03:22:45 Port scan detected from 10.0.0.55 on ports 22,23,80,443
2024-01-15 03:23:01 Privilege escalation attempt by user 'guest'
2024-01-15 03:23:15 Suspicious outbound connection to 198.51.100.77:4444
```

---

## 🚧 Future Improvements

- [ ] Integrate a real threat-intel API (e.g. AbuseIPDB, VirusTotal)
- [ ] Add user authentication
- [ ] Export findings as PDF or CSV
- [ ] Connect to a live log stream (syslog, Kafka, etc.)
- [ ] Replace simulated AI with an actual ML model

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">Built with ❤️ using Python & Streamlit</p>
