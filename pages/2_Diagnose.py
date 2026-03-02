import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
import base64
import requests

# MUST be first Streamlit call
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
            font-weight: 800 !important;
        }}
        div[data-testid="stFileUploader"] span {{
            color: #333 !important;
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

        .backwrap {{
            max-width: 260px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_png("assets/background.png")

# -----------------------------
# Page UI
# -----------------------------
st.markdown('<div class="title">Diagnose</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Take a photo like the example below and upload it to estimate your hair-loss stage</div>',
    unsafe_allow_html=True)
st.markdown('<div class="subtitle">Make sure the photo is clear and well-lit and try to capture the top of your head as much as possible</div>',
    unsafe_allow_html=True
)

# Example image centered (160px)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image("assets/hero.jpg", width=450)

st.markdown("<br>", unsafe_allow_html=True)

file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

# IMPORTANT: define API_URL once
API_URL = "https://hairloss-ai-app.onrender.com/predict"

if file is not None:
    img = Image.open(file)

    # Show uploaded image centered
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    with col_center:
        st.image(img, width=320)

    st.markdown('<div class="predictwrap">', unsafe_allow_html=True)
    clicked = st.button("Estimate my hair-loss stage")
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(API_URL, files=files, timeout=30)

            if response.status_code != 200:
                st.error(f"API error {response.status_code}: {response.text}")
            else:
                data = response.json()
                pred_label = data["prediction"]

                # Save for Result page
                st.session_state["pred_label"] = pred_label
                st.session_state["uploaded_image_bytes"] = file.getvalue()

                st.switch_page("pages/3_Result.py")

        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Make sure FastAPI is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# Back to Home with icon
with st.container():
    st.markdown('<div class="backwrap">', unsafe_allow_html=True)
    if st.button("🏠  Back to Home"):
        st.switch_page("Home.py")
    st.markdown("</div>", unsafe_allow_html=True)