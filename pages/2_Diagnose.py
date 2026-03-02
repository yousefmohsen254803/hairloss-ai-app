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

        /* Make the main area transparent (so background shows) */
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

        /* --- FORCE BRIGHT WIDGET LOOK (even in phone dark mode) --- */

        /* Camera box */
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

        /* Hide the default label text above the camera input */
        div[data-testid="stCameraInput"] label {{
            display: none !important;
        }}

        /* Make any text inside camera input dark */
        div[data-testid="stCameraInput"] * {{
            color: #111 !important;
        }}

        /* Buttons */
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

        .backrow {{
            display: flex;
            gap: 12px;
            margin-top: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


set_background_png("assets/background.png")

# -----------------------------
# API endpoint (use your deployed FastAPI)
# Put your Render URL here (example):
#   https://YOUR-SERVICE.onrender.com/predict
# -----------------------------
API_URL = os.getenv("API_URL", "https://hairloss-ai-app.onrender.com/predict")

# -----------------------------
# Page UI
# -----------------------------
st.markdown('<div class="title">Diagnose</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Tap the camera button to take a picture (or choose one from your device).</div>',
    unsafe_allow_html=True,
)

# Optional example image (centered)
l, c, r = st.columns([1, 1, 1])
with c:
    st.image("assets/hero.jpg", width=180)

st.markdown("<br>", unsafe_allow_html=True)

# ✅ This is the “app-style” mobile behavior:
# On phone it opens camera, and lets you pick from gallery too.
camera_file = st.camera_input("Take Picture", label_visibility="collapsed")

clicked = False

if camera_file is not None:
    img = Image.open(camera_file)

    # Preview centered
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    with col_center:
        st.image(img, width=320)

    st.markdown('<div class="predictwrap">', unsafe_allow_html=True)
    clicked = st.button("Estimate my hair-loss stage")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Predict -> go to Result page
# -----------------------------
if clicked and camera_file is not None:
    # send to API as multipart/form-data
    files = {
        "file": (
            camera_file.name or "camera.png",
            camera_file.getvalue(),
            camera_file.type or "image/png",
        )
    }

    resp = requests.post(API_URL, files=files, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    st.session_state["pred_label"] = data.get("prediction", "Unknown")
    st.session_state["uploaded_image_bytes"] = camera_file.getvalue()

    st.switch_page("pages/3_Result.py")

# -----------------------------
# Navigation buttons
# -----------------------------
st.markdown('<div class="backrow">', unsafe_allow_html=True)
colA, colB = st.columns([1, 1])
with colA:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
with colB:
    # (optional) let user refresh/take again
    if st.button("📷 Take another photo"):
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)