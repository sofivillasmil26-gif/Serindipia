import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import plotly.graph_objects as go
import json
import numpy as np

# --- 1. CONFIGURATION BRIDGE & STYLES ---
# Load configurations from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Assign variables from config.json
AI_NAME = config['ai_settings']['name']
UI_COLOR = config['hud_design']['primary_ui']
GLOW = config['hud_design']['glow_accent']
INTEL = config['mission_data']

# Load external stylesheet
st.set_page_config(page_title=f"{AI_NAME} Bridge Console", layout="wide")
with open("style.css", "r") as f:
    css_content = f.read()
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# --- 2. SECURE BRAIN SETUP ---
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY", "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")
except Exception:
    groq_api_key = "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"

client = Groq(api_key=groq_api_key)

# Helper to convert hex to rgba for Plotly charts
def hex_to_rgba(hex_str, opacity):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = "".join([c*2 for c in hex_str])
    return f"rgba({int(hex_str[0:2], 16)}, {int(hex_str[2:4], 16)}, {int(hex_str[4:6], 16)}, {opacity})"

# --- 3. SESSION STATE STATE MACHINE ---
if "current_view" not in st.session_state:
    st.session_state.current_view = "system"

if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = "Bogotá Vector"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_spoken_idx" not in st.session_state:
    st.session_state.last_spoken_idx = -1

# --- 4. VIEWPORT: DEEP SPACE STARFIELD ---
st.markdown("<div class='viewport-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin: 0 0 5px 0; text-align: center; font-size: 0.95rem; opacity: 0.85;'>🔭 VIEWPORT: ORBITAL DEEP SPACE SECTOR</h3>", unsafe_allow_html=True)

# Generate a deterministic starfield viewport using Plotly
np.random.seed(1337)
num_stars = 75
x_stars = np.random.rand(num_stars) * 100
y_stars = np.random.rand(num_stars) * 100
sizes = np.random.rand(num_stars) * 6 + 2
opacities = np.random.rand(num_stars) * 0.5 + 0.4

fig_stars = go.Figure()

# Add Stars Scatter
fig_stars.add_trace(go.Scatter(
    x=x_stars,
    y=y_stars,
    mode='markers',
    marker=dict(
        size=sizes,
        color=UI_COLOR,
        opacity=opacities,
        line=dict(width=0)
    ),
    hoverinfo='text',
    text=[f"Star ID: STR-{i:03d} | Mag: {sizes[i]:.2f}" for i in range(num_stars)]
))

# Connect some stars to form constellations
c_x1 = [x_stars[12], x_stars[25], x_stars[34], x_stars[50], x_stars[12]]
c_y1 = [y_stars[12], y_stars[25], y_stars[34], y_stars[50], y_stars[12]]
c_x2 = [x_stars[8], x_stars[18], x_stars[42], x_stars[60], x_stars[8]]
c_y2 = [y_stars[8], y_stars[18], y_stars[42], y_stars[60], y_stars[8]]

fig_stars.add_trace(go.Scatter(
    x=c_x1, y=c_y1, mode='lines',
    line=dict(color=GLOW, width=1, dash='dot'),
    hoverinfo='skip'
))
fig_stars.add_trace(go.Scatter(
    x=c_x2, y=c_y2, mode='lines',
    line=dict(color=UI_COLOR, width=0.8, dash='dash'),
    hoverinfo='skip'
))

# Make layout fit as a cockpit viewport
fig_stars.update_layout(
    xaxis=dict(visible=False, range=[0, 100]),
    yaxis=dict(visible=False, range=[0, 100]),
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13, 22, 33, 0.4)',
    height=160,
    margin=dict(l=5, r=5, t=5, b=5)
)

st.plotly_chart(fig_stars, width="stretch", config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

# --- 5. TERMINAL NAVIGATION PANEL ---
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
with col_nav1:
    if st.button("[ SYSTEM MONITOR ]", use_container_width=True):
        st.session_state.current_view = "system"
        st.rerun()
with col_nav2:
    if st.button("[ NAVIGATION CORE ]", use_container_width=True):
        st.session_state.current_view = "nav"
        st.rerun()
with col_nav3:
    if st.button("[ SOLAR MATRIX ]", use_container_width=True):
        st.session_state.current_view = "solar"
        st.rerun()
with col_nav4:
    if st.button("[ BIOPOLYMER LAB ]", use_container_width=True):
        st.session_state.current_view = "polymer"
        st.rerun()

st.markdown("<div class='terminal-separator'></div>", unsafe_allow_html=True)

# --- 6. SPLIT CONSOLE CONTROL LAYOUT ---
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    # ------------------ VIEW 1: SYSTEM MONITOR ------------------
    if st.session_state.current_view == "system":
        st.subheader("🖥️ Spaceship System Monitor")
        st.write("CORE SUB-SYSTEM MATRIX STATUS:")
        
        sys1, sys2, sys3 = st.columns(3)
        with sys1:
            st.metric("REACTOR CORE TEMP", "4500 K", "STABLE")
            st.metric("SHIELD EMITTER", "98.4%", "ACTIVE")
        with sys2:
            st.metric("WARP CORE CAPACITOR", "100%", "CHARGED")
            st.metric("LIFE SUPPORT FLOW", "1.2 kg/s", "NOMINAL")
        with sys3:
            st.metric("GRAVITY MATRIX", "1.0 G", "NOMINAL")
            st.metric("AI CORE INTEGRITY", "100%", "OPTIMIZED")
            
        st.markdown("#### 📡 RESEARCH DATA STREAM SUMMARY")
        st.write(
            f"**Photovoltaic Solar Efficiency Stream**: active telemetry from two sectors (Bogotá & Cumaral). "
            f"Maximum recorded power is **1.18W** under high solar intensity. High conversion efficiency reached **14.83%**."
        )
        st.write(
            f"**Starch-Based Biopolymer Synthesis**: evaluating five organic additives to optimize material structures. "
            f"Agar-agar represents the most stable matrix for packaging, whereas Sorbitol achieves maximum mechanical tensile strength."
        )

    # ------------------ VIEW 2: NAVIGATION CORE ------------------
    elif st.session_state.current_view == "nav":
        st.subheader("🗺️ Orbital Navigation Core")
        st.write("SELECT TARGET VECTOR SECTOR FOR SENSOR LOGS:")
        
        nav_options = ["Bogotá Vector", "Cumaral Vector"]
        selected_nav = st.selectbox("Target Sector Coordinates", nav_options)
        st.session_state.selected_sector = selected_nav
        
        st.markdown(f"#### 🛰️ SENSOR TELEMETRY LOGS: {st.session_state.selected_sector.upper()}")
        
        if st.session_state.selected_sector == "Bogotá Vector":
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                st.metric("COORDINATES", "04° 37' N, 74° 04' W")
                st.metric("SECTOR ALTITUDE", "2,640 Meters")
            with nav_col2:
                st.metric("WEATHER METRIC", "Sunny / Clear")
                st.metric("SOLAR FLUX INDEX", "Medium-High")
            st.write(
                "**Sector Notes**: Elevated high-altitude coordinates. The atmospheric density is lower, resulting in high "
                "solar irradiance purity. Cell conversion efficiency peaks in this region at **14.83%**, producing up to **0.93W**."
            )
        else:
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                st.metric("COORDINATES", "04° 16' N, 73° 29' W")
                st.metric("SECTOR ALTITUDE", "340 Meters")
            with nav_col2:
                st.metric("WEATHER METRIC", "High Humidity / Dynamic Cloud Cover")
                st.metric("SOLAR FLUX INDEX", "Variable")
            st.write(
                "**Sector Notes**: Low-altitude plains with elevated ambient humidity. Solar flux ranges from low (morning) "
                "to high (noon). Maximum power spikes to **1.18W** under peak irradiance ($11.36\%$ efficiency), but drops to **0.27W** ($6.44\%$ efficiency) during morning cloud coverage."
            )

    # ------------------ VIEW 3: SOLAR MATRIX ------------------
    elif st.session_state.current_view == "solar":
        st.subheader("☀️ Solar Core Matrix")
        st.write("SOLAR CELL TELEMETRY LOGS:")
        
        solar_cores = list(INTEL["solar_telemetry"].keys())
        selected_solar = st.selectbox("Solar Core Data Set", solar_cores)
        solar_data = INTEL["solar_telemetry"][selected_solar]
        
        sol_col1, sol_col2 = st.columns(2)
        with sol_col1:
            st.metric("MAX POWER OUTPUT", solar_data["max_power"])
            st.metric("CONVERSION EFFICIENCY", solar_data["efficiency"])
            st.metric("V_MPP / I_MPP", f"{solar_data['voltage_mpp']} / {solar_data['current_mpp']}")
        with sol_col2:
            st.metric("OPTIMAL RESISTANCE", solar_data["optimal_resistance"])
            st.metric("OPEN-CIRCUIT VOLTAGE (V_oc)", solar_data["open_circuit_voltage"])
            st.metric("SHORT-CIRCUIT CURRENT (I_sc)", solar_data["short_circuit_current"])
            
        st.markdown("#### 📊 COMPARATIVE SOLAR POWER VECTOR")
        
        # Radar chart mapping corrected values
        fig = go.Figure(go.Scatterpolar(
          r=[1.18, 0.93, 0.27, 1.30],
          theta=['Cumaral High (1.18W)','Bogotá (0.93W)','Cumaral Low (0.27W)','Target Baseline (1.3W)'],
          fill='toself', 
          fillcolor=hex_to_rgba(UI_COLOR, 0.08),
          line=dict(color=UI_COLOR, width=2),
          marker=dict(color=GLOW, size=8)
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(13, 22, 33, 0.5)',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 1.5], 
                    gridcolor=hex_to_rgba(UI_COLOR, 0.13),
                    linecolor='rgba(0,0,0,0)',
                    tickfont=dict(size=8, color=hex_to_rgba(UI_COLOR, 0.53))
                ),
                angularaxis=dict(
                    linecolor=UI_COLOR, 
                    gridcolor=hex_to_rgba(UI_COLOR, 0.13),
                    tickfont=dict(size=9, color=UI_COLOR, family='Share Tech Mono')
                )
            ),
            showlegend=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color=UI_COLOR, family='Share Tech Mono'), 
            height=250,
            margin=dict(l=45, r=45, t=10, b=10)
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    # ------------------ VIEW 4: BIOPOLYMER LAB ------------------
    elif st.session_state.current_view == "polymer":
        st.subheader("🧬 Biopolymer Synthesis Lab")
        st.write("STARCH-BASED BIOPOLYMER MATRIX:")
        
        polymers = list(INTEL["polymer_report"].keys())
        selected_poly = st.selectbox("Polymer Additive Variant", polymers)
        poly_data = INTEL["polymer_report"][selected_poly]
        
        poly_col1, poly_col2 = st.columns(2)
        with poly_col1:
            st.metric("THICKNESS (Group 6)", poly_data["thickness"])
            st.metric("FLEXIBILITY RANGE", poly_data["flexibility"])
        with poly_col2:
            st.metric("TENSILE LOAD STRENGTH", poly_data["strength"])
            st.metric("WATER ABSORPTION RATIO", poly_data["water_absorption"])
            
        st.markdown(f"**LAB NOTES:** <span style='color: {GLOW};'>{poly_data['observation']}</span>", unsafe_allow_html=True)
        
        st.markdown("#### 🔬 STARCH MOLECULAR LINKAGES (GLYCOSIDIC)")
        st.markdown(
            "Starch biopolymers are synthesized from natural **Amylose** and **Amylopectin** structures:\n"
            "* **Amylose**: Linear chains of glucose molecules linked via **$\\alpha(1\\rightarrow4)$** glycosidic bonds.\n"
            "* **Amylopectin**: Highly branched chains linked via **$\\alpha(1\\rightarrow4)$** linear bonds and **$\\alpha(1\\rightarrow6)$** branching bonds."
        )
        st.text(
            "   [Glucose]--α(1→4)--[Glucose]--α(1→4)--[Glucose]\n"
            "                             |\n"
            "                          α(1→6)\n"
            "                             |\n"
            "                          [Glucose]--α(1→4)--[Glucose]"
        )
        
        st.markdown("#### 📝 LAB RECORD: COMPREHENSIVE ADDITIVES LIST")
        st.markdown(
            "| Additive Variant | Thickness (cm) | Flexibility (degrees) | Load Capacity (g) | Water Absorption (%) |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n"
            "| **Sorbitolo** | 0.64 | 160° | 50.10 | -4.79% |\n"
            "| **Agar-Agar** | 1.00 | 90° | 23.38 | 16.00% |\n"
            "| **Miele (Honey)** | Heterogeneous | 90° | Undetermined | 10.87% |\n"
            "| **Fondi di Caffè** | 1.12 | 100° | 43.03 | 3.15% |\n"
            "| **Cellulosa** | 0.78 | 90° | 16.70 | 4.98% |\n"
            "| **Amido (Control)** | 0.80 | 50° | 6.68 | -6.77% |"
        )

with col_right:
    st.subheader(f"💬 COMMS LINK: {AI_NAME}")
    
    # Render chat logs
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Command {AI_NAME}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build grounded prompt passing the complete telemetry and console view context
        system_content = (
            f"You are {AI_NAME}. {config['ai_settings']['personality']} "
            f"The Captain is currently viewing the [{st.session_state.current_view.upper()}] console panel. "
            f"Here is your official experimental database: {json.dumps(INTEL)}. "
            f"Refer strictly to this database. For metrics or details not included in this database, "
            f"you must stay in character and respond: 'Current sensor logs lack telemetry on this parameter.' "
            f"Do not invent any details. Address the user as {config['ai_settings']['callsign']}."
        )
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_content},
                *st.session_state.messages
            ],
            model="llama-3.1-8b-instant",
        )
        
        reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# --- 7. WEB SPEECH API TTS (Text-to-Speech) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    msg_idx = len(st.session_state.messages) - 1
    if msg_idx > st.session_state.last_spoken_idx:
        st.session_state.last_spoken_idx = msg_idx
        # Sanitize reply for JavaScript speech synthesis
        clean_reply = (st.session_state.messages[-1]["content"]
                       .replace('**', '')
                       .replace('*', '')
                       .replace('`', '')
                       .replace('"', '\\"')
                       .replace('\n', ' '))
        
        components.html(f"""
            <script>
            const speak = () => {{
                const synth = window.speechSynthesis || window.parent.speechSynthesis;
                if (!synth) return;
                synth.cancel(); // Interrupt prior speakings
                
                const utterance = new SpeechSynthesisUtterance("{clean_reply}");
                utterance.pitch = 0.98;
                utterance.rate = 1.02;
                
                const setVoiceAndSpeak = () => {{
                    const voices = synth.getVoices();
                    const preferredVoice = voices.find(v => v.lang.startsWith("en-") && v.name.includes("Google")) || voices.find(v => v.lang.startsWith("en-"));
                    if (preferredVoice) utterance.voice = preferredVoice;
                    synth.speak(utterance);
                }};
                
                if (synth.getVoices().length > 0) {{
                    setVoiceAndSpeak();
                }} else {{
                    synth.onvoiceschanged = setVoiceAndSpeak;
                }}
            }};
            
            // Invoke speech synthesis
            if (document.readyState === "complete") {{
                speak();
            }} else {{
                window.addEventListener("load", speak);
            }}
            </script>
        """, height=0)