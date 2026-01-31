 import streamlit as st
import time
import random
import os

# 1. Page Config
st.set_page_config(page_title="CogniLink Dashboard", page_icon="🧠", layout="centered")

# 2. Styling
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 CogniLink Interface")

# --- FIXED LAYOUT SECTION ---
# We create these empty boxes ONCE, so we can refill them later
status_placeholder = st.empty()

col1, col2 = st.columns(2)
with col1:
    focus_metric = st.empty() # Empty box for Focus
with col2:
    device_metric = st.empty() # Empty box for Device

chart_placeholder = st.empty()
# -----------------------------

# 3. The Logic Engine
def get_brain_data():
    data_file = "brain_data.txt"
    if os.path.exists(data_file) and (time.time() - os.path.getmtime(data_file) < 2):
        try:
            with open(data_file, "r") as f:
                value = int(f.read().strip())
                return value, "🟢 LIVE SENSOR DATA"
        except:
            pass
    return random.randint(40, 90), "🟠 DEMO SIMULATION"

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = [50] * 30

# 4. The Loop
while True:
    focus, status = get_brain_data()
    
    # Update History
    st.session_state.history.append(focus)
    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

    # REFRESH THE UI (This part was broken before)
    status_placeholder.markdown(f"**System Status:** {status}")
    
    # We update the empty boxes we made earlier
    focus_metric.metric("Focus Level", f"{focus}%")
    
    state = "ACTIVE" if focus > 80 else "STANDBY"
    device_metric.metric("Device Control", state)

    # Update Graph
    chart_placeholder.line_chart(st.session_state.history)

    time.sleep(0.5)
