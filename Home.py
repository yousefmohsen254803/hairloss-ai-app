import base64
import streamlit as st

st.set_page_config(page_title="Hair Loss Stage Estimator", layout="centered")


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
            text-align:center;
            font-size:52px;
            color:white;
            font-weight:700;
            text-shadow: 0 4px 20px rgba(0,0,0,0.8);
        }}

        .subtitle {{
            text-align:center;
            font-size:18px;
            color:rgba(255,255,255,0.85);
            margin-top:20px;
        }}

        .subtitle2 {{
            text-align:center;
            font-size:18px;
            color:rgba(255,255,255,0.85);
            margin-top:-10px;
        }}

        div.stButton > button {{
            border-radius:14px;
            padding:12px 16px;
            font-weight:700;
        }}

        .example-img img {{
            border-radius:16px;
            box-shadow:0 10px 30px rgba(0,0,0,0.35);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_background_png("assets/background.png")


# -----------------------------
# Title
# -----------------------------
st.markdown(
"""
<div class="title">
Hair Loss Stage Estimator
</div>
""",
unsafe_allow_html=True
)


# -----------------------------
# Description
# -----------------------------
st.markdown(
"""
<div class="subtitle">
AI-powered tool that helps you estimate your hair-loss stage using images

</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle2">
It analyzes the image and estimates your hair-loss stage according to the Norwood scale like the examples below
</div>
""",
unsafe_allow_html=True
)


st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# Norwood Example Image
# -----------------------------
st.markdown('<div class="example-img">', unsafe_allow_html=True)

st.image(
    "assets/example.png",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------
# Explanation section
# ---------------------------------
st.markdown(
"""
<div style="
    max-width:850px;
    margin:20px auto;
    padding:28px;
    background:rgba(0,0,0,0.55);
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.15);
    color:rgba(255,255,255,0.9);
    font-size:17px;
    line-height:1.6;
">

<p style="margin-top:0;">
<b>This AI tool does more than classify your hair-loss stage.</b>
It also analyzes the <b>hair density</b> in the visible scalp area and estimates the
<b>number of grafts that may be required for a potential hair transplant.</b>
</p>

<h4 style="color:#9fffe0;margin-top:18px;">Hair Density</h4>

<p>
Hair density refers to the number of hair follicles growing in a specific
area of the scalp, typically measured in grafts per square centimeter.
Higher density means the scalp is well covered with hair,
while lower density can indicate thinning or advanced hair loss.
</p>

<p>
By estimating hair density from the uploaded image, the system
provides a clearer picture of how much hair coverage remains
and how severe the thinning might be.
</p>

<h4 style="color:#9fffe0;margin-top:18px;">Estimated Grafts</h4>

<p>
Estimated grafts represent an approximate number of hair follicle
grafts that could be required if a hair transplant procedure were considered.
This estimate is based on the predicted Norwood stage and the visible hair density.
</p>

</div>
""",
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Button
# -----------------------------
col1, col2, col3 = st.columns([2,2,2])

with col2:
    if st.button("Diagnose my hair"):
        st.switch_page("pages/2_Diagnose.py")