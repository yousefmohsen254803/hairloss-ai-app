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
            max-width: 900px;
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
            font-size: 16px;
            color: rgba(255,255,255,0.92);
            margin-top: 0px;
            margin-bottom: 18px;
        }}

        .resultbox {{
            max-width: 760px;
            margin: 18px auto 0 auto;
            background: rgba(0,255,170,0.15);
            border: 2px solid rgba(0,255,170,0.6);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            color: white;
            box-shadow: 0 0 30px rgba(0,255,170,0.45);
        }}

        .result-label {{
            font-size: 22px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
            text-shadow: 0 4px 18px rgba(0,0,0,0.9);
        }}

        .prediction {{
            font-size: 42px;
            font-weight: 900;
            color: white;
            margin-bottom: 20px;
            text-shadow: 0 4px 18px rgba(0,0,0,0.9);
        }}

        .info-line {{
            font-size: 20px;
            color: white;
            margin-top: 10px;
            text-shadow: 0 4px 18px rgba(0,0,0,0.9);
        }}

        .note {{
            text-align: center;
            font-size: 18px;
            color: rgba(255,255,255,0.85);
            margin-top: 18px;
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
        "grafts": "0 grafts needed"
    },
    "Moderate Loss": {
        "norwood": "Norwood 3-4",
        "density": "Medium density (60-80 grafts/cm²)",
        "grafts": "1000-2000 grafts estimated"
    },
    "Heavy Loss": {
        "norwood": "Norwood 5-6",
        "density": "Low density (40-60 grafts/cm²)",
        "grafts": "2500-4000 grafts estimated"
    },
    "Bald": {
        "norwood": "Norwood 7",
        "density": "Very low density (<40 grafts/cm²)",
        "grafts": "4500-6000 grafts estimated"
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
left, center, right = st.columns([1, 1.2, 1])
with center:
    st.image(img, width=360)

# Result card
st.markdown(
    f"""
    <div class="resultbox">
        <div class="result-label">AI Hair Analysis</div>
        <div class="prediction">{pred_label}</div>
        <div class="info-line">Norwood Stage Estimate: <b>{info['norwood']}</b></div>
        <div class="info-line">Hair Density: <b>{info['density']}</b></div>
        <div class="info-line">Estimated Grafts: <b>{info['grafts']}</b></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Note
st.markdown(
    """
    <div class="note">
        Note: This is an AI-based estimate for project purposes only. It is not medical advice.
        For professional diagnosis and treatment, please consult a healthcare professional.
    </div>
    """,
    unsafe_allow_html=True
)

# Back button
with st.container():
    st.markdown('<div class="backwrap">', unsafe_allow_html=True)
    if st.button("🔁 Back to Diagnose"):
        st.switch_page("pages/2_Diagnose.py")
    st.markdown("</div>", unsafe_allow_html=True)