import streamlit as st
import pandas as pd
import random
import datetime
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ShadowTrace AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  – dark cyberpunk theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- base ---------- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0e1a;
    color: #c9d1e0;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #0d1224;
    border-right: 1px solid #1e2d50;
}
[data-testid="stSidebar"] .css-1d391kg { padding-top: 1rem; }

/* ---------- headings ---------- */
h1 { color: #00d4ff !important; letter-spacing: 2px; }
h2 { color: #a855f7 !important; }
h3 { color: #00d4ff !important; }

/* ---------- metric cards ---------- */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1224, #1a2340);
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.15);
}
[data-testid="stMetricValue"] { color: #00d4ff !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: #a0aec0 !important; }
[data-testid="stMetricDelta"] { color: #a855f7 !important; }

/* ---------- buttons ---------- */
.stButton > button {
    background: linear-gradient(90deg, #1a2a6c, #b21f1f, #1a2a6c) !important;
    color: #fff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    letter-spacing: 1px;
    transition: box-shadow 0.3s;
}
.stButton > button:hover {
    box-shadow: 0 0 18px rgba(0, 212, 255, 0.6) !important;
}

/* ---------- text inputs ---------- */
.stTextInput > div > div > input,
.stTextArea textarea {
    background-color: #0d1224 !important;
    color: #c9d1e0 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 6px !important;
}

/* ---------- select / radio ---------- */
.stSelectbox > div > div,
.stRadio > div { color: #c9d1e0; }

/* ---------- dataframes ---------- */
[data-testid="stDataFrame"] { background-color: #0d1224 !important; }

/* ---------- custom alert boxes ---------- */
.alert-critical {
    background: rgba(220, 38, 38, 0.15);
    border-left: 4px solid #dc2626;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #fca5a5;
}
.alert-high {
    background: rgba(234, 88, 12, 0.15);
    border-left: 4px solid #ea580c;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #fdba74;
}
.alert-medium {
    background: rgba(234, 179, 8, 0.15);
    border-left: 4px solid #eab308;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #fde047;
}
.alert-low {
    background: rgba(34, 197, 94, 0.15);
    border-left: 4px solid #22c55e;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    color: #86efac;
}
.glow-box {
    border: 1px solid #00d4ff;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    background: #0d1224;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS & FAKE DATA
# ─────────────────────────────────────────────

THREAT_TYPES = [
    "SQL Injection", "Brute Force", "Port Scan", "Phishing",
    "DDoS Attack", "Ransomware", "Privilege Escalation",
    "Credential Stuffing", "Man-in-the-Middle", "Zero-Day Exploit",
]

SEVERITIES   = ["Critical", "High", "Medium", "Low"]
SEVERITY_MAP = {"Critical": "alert-critical", "High": "alert-high",
                "Medium": "alert-medium",   "Low":  "alert-low"}

COUNTRIES    = ["Russia", "China", "USA", "Brazil", "Germany",
                "India",  "UK",    "Iran", "North Korea", "Ukraine"]

IP_PREFIXES  = ["192.168", "10.0", "172.16", "203.0", "198.51"]


def random_ip():
    prefix = random.choice(IP_PREFIXES)
    return f"{prefix}.{random.randint(1,254)}.{random.randint(1,254)}"


def generate_events(n=20):
    rows = []
    now  = datetime.datetime.now()
    for i in range(n):
        rows.append({
            "Time":      (now - datetime.timedelta(minutes=i * random.randint(1, 15))).strftime("%H:%M:%S"),
            "Source IP": random_ip(),
            "Threat":    random.choice(THREAT_TYPES),
            "Severity":  random.choice(SEVERITIES),
            "Country":   random.choice(COUNTRIES),
            "Status":    random.choice(["Blocked", "Detected", "Investigating"]),
        })
    return pd.DataFrame(rows)


def analyze_log_text(text: str):
    """Very simple keyword-based AI simulation for log analysis."""
    findings = []
    keywords = {
        "failed login":         ("Brute Force",              "High"),
        "sql":                  ("SQL Injection",             "Critical"),
        "select * from":        ("SQL Injection",             "Critical"),
        "drop table":           ("SQL Injection",             "Critical"),
        "port scan":            ("Port Scan",                 "Medium"),
        "nmap":                 ("Port Scan",                 "Medium"),
        "ddos":                 ("DDoS Attack",               "Critical"),
        "flood":                ("DDoS Attack",               "High"),
        "phishing":             ("Phishing",                  "High"),
        "malware":              ("Malware Detected",          "Critical"),
        "ransomware":           ("Ransomware",                "Critical"),
        "privilege":            ("Privilege Escalation",      "High"),
        "root access":          ("Unauthorized Root Access",  "Critical"),
        "suspicious":           ("Suspicious Activity",       "Medium"),
        "unauthorized":         ("Unauthorized Access",       "High"),
        "credential":           ("Credential Stuffing",       "High"),
        "exploit":              ("Exploit Attempt",           "Critical"),
        "vulnerability":        ("Vulnerability Probe",       "Medium"),
    }
    lower = text.lower()
    for keyword, (threat, severity) in keywords.items():
        if keyword in lower:
            findings.append({"Threat": threat, "Severity": severity,
                              "Keyword": keyword, "Confidence": f"{random.randint(75,99)}%"})
    return findings


def severity_badge(s):
    colours = {"Critical": "#dc2626", "High": "#ea580c",
               "Medium":   "#eab308", "Low":  "#22c55e"}
    c = colours.get(s, "#6b7280")
    return f'<span style="background:{c};color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem;">{s}</span>'


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <h1 style='font-size:1.6rem;'>🛡️ ShadowTrace AI</h1>
        <p style='color:#6b7280; font-size:0.8rem; margin-top:-0.5rem;'>
            Cybersecurity Intelligence Platform
        </p>
        <hr style='border-color:#1e3a5f;'>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Dashboard", "🔍  Threat Analyzer", "📋  Log Scanner", "ℹ️  About"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1e3a5f;'>", unsafe_allow_html=True)

    st.markdown("**⚙️ Settings**")
    auto_refresh = st.toggle("Auto-refresh dashboard", value=False)
    refresh_rate = st.slider("Refresh interval (s)", 5, 60, 15, disabled=not auto_refresh)

    st.markdown("<hr style='border-color:#1e3a5f;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280;font-size:0.75rem;text-align:center;'>"
        "v1.0.0 &nbsp;|&nbsp; Demo Mode<br>"
        "All data is simulated.</p>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  PAGE 1 – DASHBOARD
# ─────────────────────────────────────────────

if page == "🏠  Dashboard":

    st.markdown("<h1>🛡️ ShadowTrace AI — Security Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280;'>Real-time simulated threat intelligence & monitoring</p>",
        unsafe_allow_html=True,
    )

    # ── KPI row ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚨 Active Threats",    str(random.randint(12, 35)),  f"+{random.randint(1,8)} today")
    with col2:
        st.metric("🛑 Blocked Attacks",   str(random.randint(120, 400)), f"+{random.randint(10,50)} today")
    with col3:
        st.metric("📡 Monitored IPs",     str(random.randint(500, 2000)), "Live")
    with col4:
        st.metric("⚠️ Critical Alerts",   str(random.randint(3, 12)),   f"+{random.randint(1,4)} today")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Threat distribution chart ──
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("<h2>📊 Threat Activity (Last 24 Hours)</h2>", unsafe_allow_html=True)
        hours   = [f"{h:02d}:00" for h in range(24)]
        attacks = [random.randint(5, 80) for _ in hours]
        blocked = [int(a * random.uniform(0.6, 0.95)) for a in attacks]

        chart_df = pd.DataFrame({"Hour": hours, "Attacks Detected": attacks, "Attacks Blocked": blocked})
        chart_df = chart_df.set_index("Hour")
        st.line_chart(chart_df, color=["#00d4ff", "#a855f7"], height=260)

    with right:
        st.markdown("<h2>🌍 Top Threat Origins</h2>", unsafe_allow_html=True)
        country_data = {c: random.randint(10, 200) for c in random.sample(COUNTRIES, 6)}
        country_df   = pd.DataFrame(list(country_data.items()), columns=["Country", "Attacks"])
        country_df   = country_df.sort_values("Attacks", ascending=False)
        st.bar_chart(country_df.set_index("Country"), color="#a855f7", height=260)

    # ── Severity breakdown ──
    st.markdown("<h2>🎯 Threat Severity Breakdown</h2>", unsafe_allow_html=True)
    sev_cols = st.columns(4)
    sev_vals = {
        "🔴 Critical": (random.randint(3, 15),  "#dc2626"),
        "🟠 High":     (random.randint(10, 40), "#ea580c"),
        "🟡 Medium":   (random.randint(20, 60), "#eab308"),
        "🟢 Low":      (random.randint(30, 80), "#22c55e"),
    }
    for (label, (val, colour)), col in zip(sev_vals.items(), sev_cols):
        with col:
            st.markdown(
                f'<div class="glow-box" style="border-color:{colour};text-align:center;">'
                f'<p style="font-size:2rem;font-weight:700;color:{colour};">{val}</p>'
                f'<p style="color:#a0aec0;font-size:0.85rem;">{label}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Live event feed ──
    st.markdown("<h2>📡 Live Event Feed</h2>", unsafe_allow_html=True)

    if auto_refresh:
        placeholder = st.empty()
        with placeholder.container():
            df = generate_events(15)
            st.dataframe(df, use_container_width=True, hide_index=True)
        time.sleep(refresh_rate)
        st.rerun()
    else:
        df = generate_events(15)
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("🔄 Refresh Feed"):
            st.rerun()


# ─────────────────────────────────────────────
#  PAGE 2 – THREAT ANALYZER
# ─────────────────────────────────────────────

elif page == "🔍  Threat Analyzer":

    st.markdown("<h1>🔍 AI Threat Analyzer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280;'>Analyze an IP address or domain for potential threats.</p>",
        unsafe_allow_html=True,
    )

    col_input, col_type = st.columns([3, 1])
    with col_input:
        target = st.text_input("🎯 Enter IP Address or Domain", placeholder="e.g. 192.168.1.100 or example.com")
    with col_type:
        scan_type = st.selectbox("Scan Type", ["Quick Scan", "Deep Scan", "Full Recon"])

    if st.button("🚀 Run AI Analysis"):
        if not target:
            st.warning("Please enter a target IP or domain.")
        else:
            with st.spinner("ShadowTrace AI is analyzing the target..."):
                time.sleep(2)  # Simulate processing

            risk_score    = random.randint(10, 99)
            threat_level  = ("Critical" if risk_score > 80 else
                             "High"     if risk_score > 60 else
                             "Medium"   if risk_score > 40 else "Low")
            css_class     = SEVERITY_MAP[threat_level]

            # ── Risk score card ──
            st.markdown(f"""
            <div class="glow-box">
                <h3 style="margin:0;">🎯 Analysis Results for: <code style="color:#00d4ff;">{target}</code></h3>
                <p style="color:#a0aec0;font-size:0.85rem;">Scan type: {scan_type} &nbsp;|&nbsp;
                   Completed: {datetime.datetime.now().strftime('%H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)

            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("🔥 Risk Score",    f"{risk_score}/100")
            with r2:
                st.metric("⚠️ Threat Level",  threat_level)
            with r3:
                st.metric("🌍 Origin Country", random.choice(COUNTRIES))

            # ── Findings ──
            st.markdown("<h2>🔎 Detected Findings</h2>", unsafe_allow_html=True)
            findings_count = random.randint(2, 7)
            for _ in range(findings_count):
                severity = random.choice(SEVERITIES)
                threat   = random.choice(THREAT_TYPES)
                port     = random.choice([21, 22, 23, 80, 443, 3306, 8080, 8443])
                st.markdown(
                    f'<div class="{SEVERITY_MAP[severity]}">'
                    f'<strong>{threat}</strong> &nbsp; {severity_badge(severity)}<br>'
                    f'<small>Port {port} &nbsp;|&nbsp; Confidence: {random.randint(70,99)}% &nbsp;|&nbsp; '
                    f'First seen: {random.randint(1,30)} days ago</small>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # ── Recommendations ──
            st.markdown("<h2>💡 AI Recommendations</h2>", unsafe_allow_html=True)
            recs = [
                "🔒 Immediately block this IP at the firewall level.",
                "📧 Enable multi-factor authentication on all exposed services.",
                "🔄 Rotate credentials that may have been compromised.",
                "📋 File an incident report and notify the security team.",
                "🛡️ Apply latest security patches to reduce attack surface.",
                "🔍 Enable deep packet inspection on this traffic segment.",
                "📊 Increase monitoring frequency for this IP range.",
            ]
            for rec in random.sample(recs, 4):
                st.markdown(f"- {rec}")

            # ── Port scan simulation ──
            st.markdown("<h2>🔭 Open Ports Discovered</h2>", unsafe_allow_html=True)
            port_services = {
                21: "FTP",    22: "SSH",    23: "Telnet",  25: "SMTP",
                80: "HTTP",  443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Alt",
                8443: "HTTPS-Alt", 3389: "RDP",
            }
            open_ports = random.sample(list(port_services.items()), random.randint(3, 7))
            port_df = pd.DataFrame(open_ports, columns=["Port", "Service"])
            port_df["Risk"]   = [random.choice(SEVERITIES) for _ in open_ports]
            port_df["Status"] = ["Open"] * len(open_ports)
            st.dataframe(port_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE 3 – LOG SCANNER
# ─────────────────────────────────────────────

elif page == "📋  Log Scanner":

    st.markdown("<h1>📋 AI Log Scanner</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280;'>Paste system logs or network traffic snippets. "
        "The AI will identify suspicious patterns.</p>",
        unsafe_allow_html=True,
    )

    sample_log = """\
2024-01-15 03:22:11 FAILED LOGIN attempt from 192.168.1.105 (admin)
2024-01-15 03:22:14 FAILED LOGIN attempt from 192.168.1.105 (root)
2024-01-15 03:22:18 SQL query detected: SELECT * FROM users WHERE id=1 OR 1=1
2024-01-15 03:22:45 Port scan detected from 10.0.0.55 on ports 22,23,80,443
2024-01-15 03:23:01 Privilege escalation attempt by user 'guest'
2024-01-15 03:23:15 Suspicious outbound connection to 198.51.100.77:4444
"""

    if st.button("📥 Load Sample Log"):
        st.session_state["log_text"] = sample_log

    log_text = st.text_area(
        "📄 Paste Log Data Here",
        value=st.session_state.get("log_text", ""),
        height=240,
        placeholder="Paste firewall logs, auth logs, IDS alerts, etc. ...",
        key="log_input",
    )

    if st.button("🤖 Scan with AI"):
        if not log_text.strip():
            st.warning("Please paste some log data first.")
        else:
            with st.spinner("Analyzing logs with ShadowTrace AI..."):
                time.sleep(1.5)
            findings = analyze_log_text(log_text)

            if not findings:
                st.success("✅ No threats detected in the provided logs.")
            else:
                st.markdown(
                    f"<div class='alert-high'><strong>⚠️ {len(findings)} potential threat(s) detected!</strong></div>",
                    unsafe_allow_html=True,
                )
                st.markdown("<h2>🔎 Scan Results</h2>", unsafe_allow_html=True)

                for f in findings:
                    css_class = SEVERITY_MAP.get(f["Severity"], "alert-low")
                    st.markdown(
                        f'<div class="{css_class}">'
                        f'<strong>{f["Threat"]}</strong> &nbsp; {severity_badge(f["Severity"])}<br>'
                        f'<small>Triggered by keyword: <code>"{f["Keyword"]}"</code> '
                        f'&nbsp;|&nbsp; Confidence: {f["Confidence"]}</small>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Summary
                st.markdown("<h2>📊 Summary</h2>", unsafe_allow_html=True)
                summary_df = pd.DataFrame(findings)[["Threat", "Severity", "Confidence"]]
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

                # Severity counts
                sev_counts = summary_df["Severity"].value_counts().reset_index()
                sev_counts.columns = ["Severity", "Count"]
                st.markdown("<h3>Findings by Severity</h3>", unsafe_allow_html=True)
                st.bar_chart(sev_counts.set_index("Severity"), color="#00d4ff", height=180)


# ─────────────────────────────────────────────
#  PAGE 4 – ABOUT
# ─────────────────────────────────────────────

elif page == "ℹ️  About":

    st.markdown("<h1>ℹ️ About ShadowTrace AI</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glow-box">
        <h2 style="margin-top:0;">🛡️ What is ShadowTrace AI?</h2>
        <p>
            ShadowTrace AI is a <strong>beginner-friendly cybersecurity dashboard</strong> built with
            Python and Streamlit. It simulates an AI-powered threat intelligence platform where you can:
        </p>
        <ul style="color:#c9d1e0; line-height:2;">
            <li>📊 Monitor a real-time (simulated) security dashboard</li>
            <li>🔍 Analyze suspicious IP addresses and domains</li>
            <li>📋 Scan log files for threat indicators</li>
            <li>📈 Visualize threat trends and severity breakdowns</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2>🧠 How the AI Works</h2>", unsafe_allow_html=True)
    st.markdown("""
    | Module | Technique |
    |---|---|
    | **Threat Analyzer** | Risk scoring + simulated port/service enumeration |
    | **Log Scanner** | Keyword-pattern matching with confidence scoring |
    | **Dashboard** | Real-time simulated telemetry with trend analysis |
    """)

    st.markdown("<h2>🛠️ Tech Stack</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glow-box" style="text-align:center;">
            <p style="font-size:2rem;">🐍</p>
            <strong>Python 3.8+</strong>
            <p style="color:#6b7280;font-size:0.8rem;">Core language</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glow-box" style="text-align:center;">
            <p style="font-size:2rem;">⚡</p>
            <strong>Streamlit</strong>
            <p style="color:#6b7280;font-size:0.8rem;">Web UI framework</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glow-box" style="text-align:center;">
            <p style="font-size:2rem;">🐼</p>
            <strong>Pandas</strong>
            <p style="color:#6b7280;font-size:0.8rem;">Data handling</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 All data displayed in this app is **randomly generated** for demonstration purposes. No real network traffic is monitored.")
