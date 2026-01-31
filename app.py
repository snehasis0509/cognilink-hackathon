import streamlit as st
import time
import random
import os

# 1. Page Config (Tab Title & Mobile Friendly)
st.set_page_config(page_title="CogniLink Dashboard", page_icon="🧠", layout="centered")

# 2. Styling
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .status-live { color: #00FF00; font-weight: bold; }
    .status-demo { color: #FFAA00; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 3rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 CogniLink Interface")

# 3. The Logic Engine (Live vs Demo)
def get_brain_data():
    data_file = "brain_data.txt"
    
    # Check: Does the file exist AND was it updated in the last 2 seconds?
    if os.path.exists(data_file) and (time.time() - os.path.getmtime(data_file) < 2):
        try:
            with open(data_file, "r") as f:
                value = int(f.read().strip())
                return value, "🟢 LIVE SENSOR DATA"
        except:
            pass # If error, fall back to demo
            
    # Fallback: Generate fake smooth data
    return random.randint(40, 90), "🟠 DEMO SIMULATION"

# 4. Layout
status_text = st.empty()
col1, col2 = st.columns(2)
chart_place = st.empty()

# Initialize data history
if "history" not in st.session_state:
    st.session_state.history = [50] * 30

# 5. The Loop (Runs forever)
while True:
    focus, status = get_brain_data()
    
    # Update History
    st.session_state.history.append(focus)
    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

    # Update UI
    with status_text.container():
        st.markdown(f"**System Status:** {status}")

    with col1:
        st.metric("Focus Level", f"{focus}%")
    
    with col2:
        state = "ACTIVE" if focus > 80 else "STANDBY"
        st.metric("Device Control", state)

    # Update Graph
    chart_place.line_chart(st.session_state.history)

    time.sleep(0.5) # Refresh every half second