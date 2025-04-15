import streamlit as st
import json

# Page config
st.set_page_config(
    page_title="AutoDefend AI Demo",
    page_icon="🛡️",
    layout="wide",
)

# Header
st.title("🛡️ AutoDefend AI")
st.subheader("Real-time AI-Powered Threat Detection & Response")

# Sidebar Navigation
section = st.sidebar.radio("Go to", ["Dashboard", "Threat Analysis", "Logs", "Responses"])

# Load sample logs (limit to 5 for speed)
try:
    with open("synthetic_security_logs.json", "r") as f:
        logs = json.load(f)
        logs = logs[:5]  # Limit for demo
except FileNotFoundError:
    st.error("⚠️ Log file not found. Please run generate_logs.py first.")
    logs = []

# Show pages
if section == "Dashboard":
    st.markdown("### 👁️ Live Threat Overview")
    st.metric(label="Logs Analyzed", value=len(logs))
    st.metric(label="Threats Detected", value=sum(1 for log in logs if log['log_level'] != 'INFO'))

elif section == "Threat Analysis":
    st.markdown("### 📊 AI Threat Summary")
    st.info("This is where your Bedrock AI analysis report will appear.")
    st.code("Run `analyze_logs_with_ai.py` and paste the result here manually (for now).")

elif section == "Logs":
    st.markdown("### 🧾 Raw Security Logs")
    for log in logs:
        with st.expander(f"{log['timestamp']} - {log['log_level']}"):
            st.json(log)

elif section == "Responses":
    st.markdown("### 🛡️ Simulated Security Actions")
    for log in logs:
        if log["log_level"] in ["ERROR", "CRITICAL"]:
            st.success(f"✅ Blocked IP: {log['source_ip']} for threat type: {log['threat_type']}")
