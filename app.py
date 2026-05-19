import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import json

# --- 1. CONFIGURATION BRIDGE ---
# This part opens your JSON doc and loads the 'programming'
with open('config.json', 'r') as f:
    config = json.load(f)

# Assigning variables from the JSON for easy use
AI_NAME = config['ai_settings']['name']
UI_COLOR = config['hud_design']['primary_ui']
GLOW = config['hud_design']['glow_accent']
INTEL = config['mission_data']

# --- 2. BRAIN SETUP ---
# Replace with your actual Groq API Key
client = Groq(api_key="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")

# --- 3. SPACESHIP INTERFACE (CSS) ---
st.set_page_config(page_title=f"{AI_NAME} HUD", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {config['hud_design']['background']}; color: {UI_COLOR}; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {GLOW} !important; text-shadow: 0 0 10px {GLOW}; }}
    .stTextInput>div>div>input {{ background-color: #0d1621; color: {UI_COLOR}; border: 1px solid {UI_COLOR}; }}
    .main .block-container {{ border: 1px solid {UI_COLOR}; padding: 2rem; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. HUD CONTENT ---
st.title(f"{AI_NAME} : MISSION INTERFACE")
st.write(f"SYSTEM STATUS: {config['ai_settings']['status']}")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Telemetry")
    st.metric("SOLAR CORE (BOG)", "0.27 W", "ANOMALY")
    st.metric("POLYMER MATRIX", "STABLE", "Sorbitolo")
    
    # Radar Visualization
    fig = go.Figure(go.Scatterpolar(
      r=[1.18, 0.93, 0.27, 1.3],
      theta=['Cumaral H','Cumaral L','Bogotá','Safety'],
      fill='toself', line_color=UI_COLOR
    ))
    fig.update_layout(
        polar=dict(bgcolor='#0d1621', radialaxis=dict(visible=False, range=[0, 1.5])),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font_color=UI_COLOR, height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(f"COMMS LINK: {AI_NAME}")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Command {AI_NAME}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response Generation
        # Note: Using the updated llama-3.1 model name
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are {AI_NAME}. {config['ai_settings']['personality']}. Intel: {INTEL['solar_telemetry']} {INTEL['polymer_report']}. Address the user as {config['ai_settings']['callsign']}."},
                *st.session_state.messages
            ],
            model="llama-3.1-8b-instant",
        )
        
        reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})