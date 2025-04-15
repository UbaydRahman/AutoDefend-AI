import streamlit as st
import json

# Page setup
st.set_page_config(
    page_title="AutoDefend AI Demo",
    page_icon="🛡️",
    layout="wide",
)

# App header
st.title("🛡️ AutoDefend AI")
st.subheader("Real-time AI-Powered Threat Detection & Response")

# Sidebar nav
section = st.sidebar.radio("📂 Navigate", ["Dashboard", "Threat Analysis", "Logs", "Responses"])

# Load sample logs
try:
    with open("synthetic_security_logs.json", "r") as f:
        logs = json.load(f)
        logs = logs[:5]  # Limit for speed
except FileNotFoundError:
    st.error("⚠️ Log file not found. Please run generate_logs.py first.")
    logs = []

# === Sections ===

if section == "Dashboard":
    st.markdown("### 👁️ Live Threat Overview")
    st.metric(label="Logs Analyzed", value=len(logs))
    st.metric(label="Threats Detected", value=sum(1 for log in logs if log["log_level"] != "INFO"))

elif section == "Threat Analysis":
    st.markdown("### 🧠 AI Threat Summary")
    st.info("Paste your latest AI analysis report from `analyze_logs_with_ai.py` below:")
    user_report = st.text_area("📝 Paste AI Report Here:", height=200)
    if user_report:
        st.success("✅ Report received.")
        st.markdown("---")
        st.markdown(user_report)

elif section == "Logs":
    st.markdown("### 🧾 Raw Security Logs")
    for log in logs:
        with st.expander(f"{log['timestamp']} | {log['log_level']} | {log['threat_type']}"):
            st.json(log)

elif section == "Responses":
    st.markdown("### 🛡️ Simulated Security Responses")
    if not logs:
        st.warning("No logs available.")
    for log in logs:
        if log["log_level"] in ["ERROR", "CRITICAL"]:
            st.success(f"✅ Blocked IP: {log['source_ip']} | Threat: {log['threat_type']}")
        elif log["log_level"] == "WARNING":
            st.warning(f"⚠️ Alert issued for: {log['source_ip']} | Suspicious activity detected.")
        else:
            st.info(f"ℹ️ No action needed for: {log['source_ip']}")
