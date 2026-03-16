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
    st.markdown('<div class="subtitle">No results found yet. Please diagnose first.</div>', unsafe_allow_html=True)

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
        "norwood": "Norwood 1–2"
    },
    "Moderate Loss": {
        "norwood": "Norwood 3–4"
    },
    "Heavy Loss": {
        "norwood": "Norwood 5–6"
    },
    "Bald": {
        "norwood": "Norwood 7"
    }
}

info = analysis_map.get(
    pred_label,
    {
        "norwood": "Unknown"
    }
)

# -----------------------------
# Page UI
# -----------------------------
st.markdown('<div class="title">Result</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Here is your uploaded photo and the estimated hair-loss stage.</div>',
    unsafe_allow_html=True
)

# Show the uploaded photo centered
left, center, right = st.columns([1, 1.2, 1])
with center:
    st.image(img, width=360)

# Bright result box
st.markdown('<div class="resultbox">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:22px;
        font-weight:700;
        color:white;
        margin-bottom:10px;
        text-shadow: 0 4px 18px rgba(0,0,0,0.9);
    ">
        AI Hair Analysis
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        background: rgba(0,255,170,0.15);
        border: 2px solid rgba(0,255,170,0.6);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        color: white;
        text-shadow: 0 4px 18px rgba(0,0,0,0.9);
        box-shadow: 0 0 30px rgba(0,255,170,0.45);
    ">
        <div style="font-size:28px; font-weight:900; margin-bottom:14px;">
            {pred_label}
        </div>

        <div style="font-size:18px; margin-top:8px;">
            Norwood Stage Estimate: <b>{info['norwood']}</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:18px;
        color:rgba(255,255,255,0.85);
        margin-top:18px;
    ">
        Note: This is not medical advice. For professional diagnosis and treatment, please consult a healthcare professional.
    </p>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="backwrap">', unsafe_allow_html=True)
    if st.button("🔁 Back to Diagnose"):
        st.switch_page("pages/2_Diagnose.py")
    st.markdown("</div>", unsafe_allow_html=True)