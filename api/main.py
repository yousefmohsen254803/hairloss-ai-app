from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
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

CLASS_NAMES = ["Bald", "Heavy Loss", "Moderate Loss", "Normal Hair"]
IMG_SIZE = (224, 224)

model = None
model_ready = False


def prepare_image(img: Image.Image):
    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img).astype("float32")
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, axis=0)
    return arr


@app.on_event("startup")
def load_model():
    global model, model_ready

    model = tf.keras.models.load_model("model/model.keras")

    # Warm up the model once so the first real prediction is faster
    dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
    model.predict(dummy, verbose=0)

    model_ready = True


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_ready": model_ready
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model, model_ready

    if model is None or not model_ready:
        raise HTTPException(status_code=503, detail="Model is not ready yet")

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        img = Image.open(io.BytesIO(contents))
        x = prepare_image(img)

        probs = model.predict(x, verbose=0)[0]
        idx = int(np.argmax(probs))

        return {
            "prediction": CLASS_NAMES[idx],
            "class_index": idx,
            "probabilities": [float(p) for p in probs]
        }

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")