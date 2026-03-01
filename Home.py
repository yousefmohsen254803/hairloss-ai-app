import base64
import streamlit as st

def set_background_png(path: str):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Apply background to multiple containers (works across Streamlit versions) */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                        url("data:image/png;base64,{b64}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Optional: remove default white background behind main area */
        [data-testid="stAppViewContainer"] > .main {{
            background: transparent;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_png("assets/background.png")

st.set_page_config(page_title="Hair Loss Stage Estimator", layout="centered")

def set_background(image_file, mime="png"):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
    """
    <h1 style="text-align:center; font-size:52px; color:white;
               text-shadow: 0 0 12px rgba(255,255,255,0.6);">
        Hair Loss Stage Estimator
    </h1>
    """,
    unsafe_allow_html=True
)


# ---- CARD START ----
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="
        text-align:center;
        font-size:52px;
        color:white;
        font-weight:700;
        text-shadow: 0 4px 20px rgba(0,0,0,0.8);
    ">
        Hair Loss Stage Esatimator
    </h1>

    <p style="
        text-align:center;
        font-size:18px;
        color:rgba(255,255,255,0.85);
        margin-top:-10px;
    ">
        AI-powered tool that help you estimate your hair-loss stage using images
    </p>

    <p style="
        text-align:center;
        font-size:18px;
        color:rgba(255,255,255,0.85);
        margin-top:-10px;
    ">
        It analyzes the image and estimates your hair-loss stage like the examples below
    </p>
    """,
    unsafe_allow_html=True
)


# Example image smaller + centered
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    st.image("assets/example.jpg", width=2000)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """

    <p style="
        text-align:center;
        font-size:18px;
        color:rgba(255,255,255,0.85);
        margin-top:-10px;
    ">
        This is not a medical advice. For professional diagnosis and treatment, please consult a healthcare professional.
    </p>
    """,
    unsafe_allow_html=True
)

if st.button("Diagnose my hair"):
    st.switch_page("pages/2_Diagnose.py")

# ---- CARD END ----
st.markdown("</div>", unsafe_allow_html=True)