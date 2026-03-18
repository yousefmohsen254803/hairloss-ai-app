import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import io
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

app = FastAPI(title="Hair Loss Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ['Bald', 'Heavy Loss', 'Moderate Loss', 'Normal Hair']
IMG_SIZE = (224, 224)

model = None

def prepare_image(img: Image.Image):
    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img).astype("float32")
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)
    return arr

@app.on_event("startup")
def load_model():
    global model
    model = tf.keras.models.load_model("model/model.keras")

    dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
    model.predict(dummy, verbose=0)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))

    x = prepare_image(img)
    probs = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(probs))

    return {
        "prediction": CLASS_NAMES[idx],
        "class_index": idx,
        "probabilities": [float(p) for p in probs]
    }