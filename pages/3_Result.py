import streamlit as st
from PIL import Image
import base64
import io

# MUST be first Streamlit call
st.set_page_config(page_title="Result", layout="centered")


# -----------------------------
# Background + UI CSS
# -----------------------------
def set_background_png(path: str):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                        url("data:image/png;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent;
        }}

        .main .block-container {{
            max-width: 950px;
            padding-top: 2rem;
        }}

        .title {{
            text-align: center;
            font-size: 56px;
            color: white;
            font-weight: 900;
            text-shadow: 0 6px 28px rgba(0,0,0,0.9);
            margin-bottom: 6px;
        }}

        .subtitle {{
            text-align: center;
            font-size: 20px;
            color: rgba(255,255,255,0.92);
            margin-top: 0px;
            margin-bottom: 18px;
        }}

        .result-card {{
            background: rgba(0, 0, 0, 0.65);
            border: 2px solid rgba(255,255,255,0.16);
            border-radius: 14px;
            padding: 16px 12px;
            text-align: center;
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
            margin-bottom: 12px;
        }}

        .card-title {{
            font-size: 20px;      /* bigger green text */
            font-weight: 800;
            color: #9fffe0;
            margin-bottom: 8px;
        }}

        .card-value {{
            font-size: 20px;      /* slightly smaller white text */
            font-weight: 400;     /* remove bold */
            color: white;
        }}

        .card-value-small {{
            font-size: 18px;
            font-weight: 400;     /* remove bold */
            color: white;
        }}

        .note {{
            text-align: center;
            font-size: 18px;
            color: rgba(255,255,255,0.88);
            margin-top: 16px;
            line-height: 1.5;
        }}

        div.stButton > button {{
            border-radius: 14px;
            padding: 12px 14px;
            font-weight: 800;
        }}

        .backwrap {{
            max-width: 260px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_background_png("assets/background.png")


# -----------------------------
# Guard: if opened directly
# -----------------------------
if "pred_label" not in st.session_state or "uploaded_image_bytes" not in st.session_state:
    st.markdown('<div class="title">Result</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">No results found yet. Please diagnose first.</div>',
        unsafe_allow_html=True
    )

    if st.button("Back to Diagnose"):
        st.switch_page("pages/2_Diagnose.py")
    st.stop()


pred_label = st.session_state["pred_label"]
img_bytes = st.session_state["uploaded_image_bytes"]
img = Image.open(io.BytesIO(img_bytes))


# -----------------------------
# Stage mapping
# -----------------------------
analysis_map = {
    "Normal Hair": {
        "norwood": "Norwood 1-2",
        "density": "High density (80-100 grafts/cm²)",
        "grafts": "No transplant needed"
    },
    "Moderate Loss": {
        "norwood": "Norwood 3-4",
        "density": "Medium density (60-80 grafts/cm²)",
        "grafts": "1000-2000 grafts"
    },
    "Heavy Loss": {
        "norwood": "Norwood 5-6",
        "density": "Low density (40-60 grafts/cm²)",
        "grafts": "2500-4000 grafts"
    },
    "Bald": {
        "norwood": "Norwood 7",
        "density": "Very low density (<40 grafts/cm²)",
        "grafts": "4500-6000 grafts"
    }
}

info = analysis_map.get(
    pred_label,
    {
        "norwood": "Unknown",
        "density": "Unknown",
        "grafts": "Unknown"
    }
)


# -----------------------------
# Page UI
# -----------------------------
st.markdown('<div class="title">Result</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Here is your uploaded photo and the estimated hair-loss analysis.</div>',
    unsafe_allow_html=True
)

# Show uploaded image centered
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(img, width=400)

st.markdown("<br>", unsafe_allow_html=True)

# 2 x 2 cards
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="card-title">Hair Loss Condition</div>
            <div class="card-value">{pred_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="card-title">Norwood Stage</div>
            <div class="card-value">{info['norwood']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="card-title">Hair Density</div>
            <div class="card-value-small">{info['density']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="card-title">Estimated Grafts</div>
            <div class="card-value-small">{info['grafts']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Note
st.markdown(
"""
<div style="
max-width:850px;
margin:20px auto;
padding:6px 18px;
background:rgba(255, 210, 80, 0.15);
border-left:6px solid #FFD43B;
border-radius:8px;
font-size:16px;
color:white;
line-height:1.6;
">

<b>Note:</b> This result is an <b>AI-based analysis</b>. It is not medical advice. For professional diagnosis or treatment, consult a healthcare professional.
<p><p>
</div>
""",
unsafe_allow_html=True
)

# Back buttons
with st.container():
    st.markdown('<div class="backwrap">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Back to Diagnose"):
            st.switch_page("pages/2_Diagnose.py")

    with col2:
        if st.button("🏠 Back to Home"):
            st.switch_page("Home.py")

    st.markdown("</div>", unsafe_allow_html=True)