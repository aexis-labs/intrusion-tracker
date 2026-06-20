import streamlit as st
import pandas as pd
import random
import datetime
import time
import hashlib
import logging
from typing import List, Dict, Any

# ==============================================================================
# 0. CONFIGURATION (load from secrets / environment)
# ==============================================================================
try:
    TARGET_HASH = st.secrets["INTRUSION_AUTH_HASH"]
except (KeyError, FileNotFoundError):
    # Fallback only for development – change this!
    TARGET_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # "admin"
    logging.warning("INTRUSION_AUTH_HASH not set. Using insecure default.")

LOG_LEVEL = st.secrets.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================================================================
# 1. PAGE CONFIG & THEME (dark cyber‑theme)
# ==============================================================================
st.set_page_config(
    page_title="Aexis Cyber Intrusion Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #00ff9d;
    }
    .stButton>button {
        background-color: #00ff9d;
        color: black;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00cc7a;
    }
    .stButton>button:disabled {
        background-color: #444;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE & AUTHENTICATION
# ==============================================================================
def init_session() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.datetime.now()
    if "intrusion_logs" not in st.session_state:
        st.session_state.intrusion_logs = [
            {"Timestamp": "19:15:22", "Source IP": "185.220.101.5", "Target Port": "SSH (22)", "Threat Level": "High", "Action": "BLOCKED"},
            {"Timestamp": "19:18:40", "Source IP": "45.132.202.12", "Target Port": "HTTP (80)", "Threat Level": "Low", "Action": "LOGGED"},
            {"Timestamp": "19:24:01", "Source IP": "91.241.19.88", "Target Port": "MySQL (3306)", "Threat Level": "Critical", "Action": "BLOCKED"}
        ]
    if "lockdown_mode" not in st.session_state:
        st.session_state.lockdown_mode = False

init_session()

def authenticate(uid: str, token: str) -> bool:
    """Verify UID and token against stored hash."""
    if not uid.strip():
        return False
    input_hash = hashlib.sha256(token.encode()).hexdigest()
    return input_hash == TARGET_HASH

# Authentication gateway
if not st.session_state.authenticated:
    st.title("🛡️ AEXIS SENTINEL: PERIMETER GATEWAY LOGIN")
    st.caption("Secure Infrastructure Authorization Terminal")
    st.write("---")
    
    with st.form(key="secure_gateway_form"):
        user_id = st.text_input("Enter Sentinel Operator Identity (UID):", placeholder="e.g., operator_01")
        access_token = st.text_input("Enter Digital Authorization Token:", type="password")
        submit_auth = st.form_submit_button("Initialize Secure Node Sync", use_container_width=True)
        
        if submit_auth:
            with st.spinner("Verifying credentials..."):
                time.sleep(0.5)
                if authenticate(user_id, access_token):
                    st.session_state.authenticated = True
                    st.session_state.last_activity = datetime.datetime.now()
                    logging.info(f"User {user_id} authenticated successfully.")
                    st.success("🔒 Cryptographic Handshake Verified. Opening local runtime context...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    logging.warning(f"Failed authentication attempt for UID: {user_id}")
                    st.error("🚨 Access Denied. Integrity mismatch detected. Event reported to core memory.")
    st.stop()

# Session timeout (30 minutes)
SESSION_TIMEOUT_MINUTES = 30
if (datetime.datetime.now() - st.session_state.last_activity).seconds > SESSION_TIMEOUT_MINUTES * 60:
    st.session_state.authenticated = False
    st.warning("Session expired. Please re‑authenticate.")
    st.rerun()
else:
    st.session_state.last_activity = datetime.datetime.now()  # refresh

# ==============================================================================
# 3. SIDEBAR – EMERGENCY LOCKDOWN & CONTROLS
# ==============================================================================
st.sidebar.title("🚨 Core Security Control")
st.sidebar.write("---")

if st.session_state.lockdown_mode:
    st.sidebar.error("❌ GLOBAL LOCKDOWN ACTIVE")
    if st.sidebar.button("Deactivate Emergency Protocol", use_container_width=True):
        st.session_state.lockdown_mode = False
        logging.info("Emergency lockdown deactivated by user.")
        st.rerun()
else:
    st.sidebar.success("🛡️ Systems Operating Normally")
    if st.sidebar.button("TRIGGER SYSTEM LOCKDOWN", use_container_width=True):
        st.session_state.lockdown_mode = True
        logging.warning("Emergency lockdown activated by user.")
        st.rerun()

if st.sidebar.button("🔒 Terminate Link Sessions", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.secure_keys = []  # if any
    st.rerun()

# Clear logs button (additional)
if st.sidebar.button("🧹 Clear All Logs", use_container_width=True):
    st.session_state.intrusion_logs = []
    st.rerun()

st.sidebar.write("---")
st.sidebar.markdown("### 📊 Live Firewall Integrity")
st.sidebar.progress(35 if st.session_state.lockdown_mode else 98)
st.sidebar.caption("System Load: 12% | Defense Efficiency: 99.8%")

st.sidebar.write("---")
st.sidebar.caption(f"Session started: {st.session_state.last_activity.strftime('%H:%M:%S')}")

# ==============================================================================
# 4. MAIN DASHBOARD UI
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
    st.metric(
        label="Threats Neutralized (Today)",
        value=len(st.session_state.intrusion_logs) * 14 + 120,
        delta="+24 vs yesterday"
    )
with col2:
    active_probes = "0 (Lockdown)" if st.session_state.lockdown_mode else f"{random.randint(2, 6)} Single IPs"
    st.metric(
        label="Active Malicious Probes",
        value=active_probes,
        delta="-100% Locked down" if st.session_state.lockdown_mode else "Stable"
    )
with col3:
    st.metric(
        label="Main Firewall Status",
        value="ISOLATED" if st.session_state.lockdown_mode else "ACTIVE",
        delta_color="inverse"
    )

st.write("---")

# ==============================================================================
# 5. INTERACTIVE SIMULATION & LOG VIEW
# ==============================================================================
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.write("### 🎛️ Attack Simulation Engine")
    st.info("Use these controls to safely simulate incoming network vector attacks to test structural defenses.")
    
    sim_threat = st.selectbox(
        "Simulate Attack Vector:",
        ["DDoS Amplification Attack", "Brute Force Auth Attack", "SQL Injection Vector", "Phishing Link Callback"],
        key="sim_threat"
    )
    sim_level = st.select_slider(
        "Threat Vector Severity:",
        options=["Low", "Medium", "High", "Critical"],
        key="sim_level"
    )
    
    if st.button(
        "Inject Simulated Vector",
        use_container_width=True,
        disabled=st.session_state.lockdown_mode,
        key="sim_button"
    ):
        random_ip = f"{random.randint(40, 220)}.{random.randint(10, 254)}.{random.randint(0, 254)}.{random.randint(1, 254)}"
        random_ports = {
            "DDoS Amplification Attack": "UDP (53)",
            "Brute Force Auth Attack": "SSH (22)",
            "SQL Injection Vector": "HTTPS (443)",
            "Phishing Link Callback": "SMTP (25)"
        }
        
        new_log = {
            "Timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "Source IP": random_ip,
            "Target Port": random_ports[sim_threat],
            "Threat Level": sim_level,
            "Action": "BLOCKED" if sim_level in ["High", "Critical"] else "LOGGED"
        }
        
        st.session_state.intrusion_logs.insert(0, new_log)
        logging.info(f"Simulated {sim_threat} from {random_ip} with severity {sim_level}")
        st.toast(f"Defended vector from {random_ip}!", icon="⚔️")
        # No rerun needed; the log list updates automatically

with col_right:
    st.write("### 📜 Real-time Network Security Logs")
    
    if not st.session_state.intrusion_logs:
        st.info("Log database empty.")
    else:
        df = pd.DataFrame(st.session_state.intrusion_logs)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Optional: export logs
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Logs (CSV)",
            data=csv,
            file_name="intrusion_logs.csv",
            mime="text/csv",
            use_container_width=True
        )

st.write("---")
st.caption("Aexis Network Systems Protocol Secured Engine V3.2")
