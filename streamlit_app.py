import streamlit as st
import pandas as pd
import random
import datetime
import time

# ==============================================================================
# 1. SYSTEM INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="Aexis Cyber Intrusion Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize persistent memory for simulation logs
if "intrusion_logs" not in st.session_state:
    st.session_state.intrusion_logs = [
        {"Timestamp": "19:15:22", "Source IP": "185.220.101.5", "Target Port": "SSH (22)", "Threat Level": "High", "Action": "BLOCKED"},
        {"Timestamp": "19:18:40", "Source IP": "45.132.202.12", "Target Port": "HTTP (80)", "Threat Level": "Low", "Action": "LOGGED"},
        {"Timestamp": "19:24:01", "Source IP": "91.241.19.88", "Target Port": "MySQL (3306)", "Threat Level": "Critical", "Action": "BLOCKED"}
    ]

if "lockdown_mode" not in st.session_state:
    st.session_state.lockdown_mode = False

# ==============================================================================
# 2. EMERGENCY LOCKDOWN CONTROL PANEL (SIDEBAR)
# ==============================================================================
st.sidebar.title("🚨 Core Security Control")
st.sidebar.write("---")

if st.session_state.lockdown_mode:
    st.sidebar.error("❌ GLOBAL LOCKDOWN ACTIVE")
    if st.sidebar.button("Deactivate Emergency Protocol", use_container_width=True):
        st.session_state.lockdown_mode = False
        st.rerun()
else:
    st.sidebar.success("🛡️ Systems Operating Normally")
    if st.sidebar.button("TRIGGER SYSTEM LOCKDOWN", use_container_width=True):
        st.session_state.lockdown_mode = True
        st.rerun()

st.sidebar.write("---")
st.sidebar.markdown("### 📊 Live Firewall Integrity")
st.sidebar.progress(35 if st.session_state.lockdown_mode else 98)
st.sidebar.caption("System Load: 12% | Defense Efficiency: 99.8%")

# ==============================================================================
# 3. MAIN DASHBOARD UI
# ==============================================================================
st.title("🛰️ Aexis Cyber Intrusion Tracker")
st.caption("Active Network Threat Mapping & Perimeter Defense Monitor")
st.write("---")

# Banner alert based on state
if st.session_state.lockdown_mode:
    st.error("⚠️ EMERGENCY ALERT: All public API routes isolated. External packet ingestion paused.")

# Metric Blocks
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Threats Neutralized (Today)", value=len(st.session_state.intrusion_logs) * 14 + 120, delta="+24 vs yesterday")
with col2:
    st.metric(label="Active Malicious Probes", value="0" if st.session_state.lockdown_mode else f"{random.randint(2, 6)} Single IPs", delta="-100% Locked down" if st.session_state.lockdown_mode else "Stable")
with col3:
    st.metric(label="Main Firewall Status", value="ISOLATED" if st.session_state.lockdown_mode else "ACTIVE", delta_color="inverse")

st.write("---")

# Interactive Simulation Tools
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.write("### 🎛️ Attack Simulation Engine")
    st.info("Use these controls to safely simulate incoming network vector attacks to test structural defenses.")
    
    sim_threat = st.selectbox("Simulate Attack Vector:", ["DDoS Amplification Attack", "Brute Force Auth Attack", "SQL Injection Vector", "Phishing Link Callback"])
    sim_level = st.select_slider("Threat Vector Severity:", options=["Low", "Medium", "High", "Critical"])
    
    if st.button("Inject Simulated Vector", use_container_width=True, disabled=st.session_state.lockdown_mode):
        random_ip = f"{random.randint(40, 220)}.{random.randint(10, 254)}.{random.randint(0, 254)}.{random.randint(1, 254)}"
        random_ports = {"DDoS Amplification Attack": "UDP (53)", "Brute Force Auth Attack": "SSH (22)", "SQL Injection Vector": "HTTPS (443)", "Phishing Link Callback": "SMTP (25)"}
        
        new_log = {
            "Timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "Source IP": random_ip,
            "Target Port": random_ports[sim_threat],
            "Threat Level": sim_level,
            "Action": "BLOCKED" if sim_level in ["High", "Critical"] else "LOGGED"
        }
        
        st.session_state.intrusion_logs.insert(0, new_log)
        st.toast(f"Defended vector from {random_ip}!", icon="⚔️")
        time.sleep(0.5)
        st.rerun()

with col_right:
    st.write("### 📜 Real-time Network Security Logs")
    
    if not st.session_state.intrusion_logs:
        st.write("Log database empty.")
    else:
        df = pd.DataFrame(st.session_state.intrusion_logs)
        st.dataframe(df, use_container_width=True, hide_index=True)

st.write("---")
st.caption("Aexis Network Systems Protocol Secured Engine V3.2")
