import os
import base64
import requests
import streamlit as st
from PIL import Image

# -----------------------------
# Page config (MUST be first)
# -----------------------------
st.set_page_config(page_title="Diagnose", layout="centered")

# -----------------------------
# Background
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
            font-size: 52px;
            color: white;
            font-weight: 900;
            text-shadow: 0 6px 28px rgba(0,0,0,0.9);
            margin-bottom: 8px;
        }}

        .subtitle {{
            text-align: center;
            font-size: 16px;
            color: rgba(255,255,255,0.95);
            margin-bottom: 20px;
        }}

        /* ---------- FIX RADIO TEXT (BRIGHT WHITE) ---------- */

        div[data-testid="stRadio"] > label {{
            color: rgba(255,255,255,0.95) !important;
            font-weight: 800 !important;
        }}

        div[role="radiogroup"] label {{
            color: rgba(255,255,255,0.95) !important;
            font-weight: 700 !important;
        }}

        /* ---------- CAMERA BOX STYLE ---------- */

        div[data-testid="stCameraInput"] {{
            background: rgba(255,255,255,0.96) !important;
            padding: 18px !important;
            border-radius: 16px !important;
            border: 2px solid rgba(255,255,255,0.96) !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25) !important;
            max-width: 760px;
            margin-left: auto;
            margin-right: auto;
        }}

        div[data-testid="stCameraInput"] label {{
            color: #111 !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stFileUploader"] {{
            background: rgba(255,255,255,0.96) !important;
            padding: 18px !important;
            border-radius: 16px !important;
            border: 2px solid rgba(255,255,255,0.96) !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25) !important;
            max-width: 760px;
            margin-left: auto;
            margin-right: auto;
        }}

        div[data-testid="stFileUploader"] label {{
            color: #111 !important;
            font-weight: 700 !important;
        }}

        div.stButton > button {{
            border-radius: 14px;
            padding: 12px 14px;
            font-weight: 800;
        }}

        .predictwrap {{
            max-width: 760px;
            margin-left: auto;
            margin-right: auto;
        }}

        .btnrow {{
            display: flex;
            gap: 12px;
            margin-top: 14px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


set_background_png("assets/background.png")

# -----------------------------
# API URL (Render deployed)
# -----------------------------
API_URL = os.getenv(
    "API_URL",
    "https://hairloss-ai-app.onrender.com/predict"
)

# -----------------------------
# Page Header
# -----------------------------
st.markdown('<div class="title">Diagnose</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Choose how to add a photo:</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Radio selector (bright now)
# -----------------------------
mode = st.radio(
    "",
    ["📷 Take a photo", "🖼️ Choose from device"],
    horizontal=True
)

file = None

if mode == "📷 Take a photo":
    file = st.camera_input("Take a photo")
else:
    file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

clicked = False

# -----------------------------
# Preview + Predict
# -----------------------------
if file is not None:
    img = Image.open(file)

    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    with col_center:
        st.image(img, width=320)

    st.markdown('<div class="predictwrap">', unsafe_allow_html=True)
    clicked = st.button("Estimate my hair-loss stage")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Send to FastAPI
# -----------------------------
if clicked and file is not None:
    files = {
        "file": (
            file.name or "image.png",
            file.getvalue(),
            file.type or "image/png",
        )
    }

    response = requests.post(API_URL, files=files, timeout=60)
    response.raise_for_status()

    data = response.json()

    st.session_state["pred_label"] = data.get("prediction", "Unknown")
    st.session_state["uploaded_image_bytes"] = file.getvalue()

    st.switch_page("pages/3_Result.py")

# -----------------------------
# Navigation Buttons
# -----------------------------
st.markdown('<div class="btnrow">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🔄 Try Again"):
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)