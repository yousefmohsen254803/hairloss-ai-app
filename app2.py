import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

# 1) Names of your 4 classes (edit if your names are different)
CLASS_NAMES = ['Bald', 'Heavy Loss', 'Moderate Loss', 'Normal Hair']

# 2) Image size your model expects (change if you trained on another size)
IMG_SIZE = (224, 224)

# 3) Load model one time (Streamlit remembers it)
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model("model/model.keras")

# 4) Make the image ready for the model
def prepare_image(img):
    img = img.convert("RGB")
    img = img.resize(IMG_SIZE)

    arr = np.array(img).astype("float32")  # keep 0-255
    arr = preprocess_input(arr)            # ✅ same as training notebook
    arr = np.expand_dims(arr, axis=0)
    return arr

# ---------- Screen ----------
st.title("Hair Loss Stage Classifier")
st.write("Upload a photo. The AI system will guess the hair-loss stage.")
st.caption("This is not a medical advice.")

file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if file is not None:
    img = Image.open(file)
    st.image(img, caption="Your uploaded image", use_container_width=True)

    if st.button("Predict my hair-loss stage"):
        model = load_my_model()
        x = prepare_image(img)
        probs = model.predict(x)[0]

        pred_index = int(np.argmax(probs))
        pred_label = CLASS_NAMES[pred_index]

        st.markdown("## Result")

        st.markdown(
            f"""
            <div style='text-align: center; font-size: 28px; font-weight: bold;'>
                {pred_label}
            </div>
            """,
            unsafe_allow_html=True
        )