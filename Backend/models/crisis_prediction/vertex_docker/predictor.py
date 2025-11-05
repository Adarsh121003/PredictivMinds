from fastapi import FastAPI, Request
import joblib
import xgboost as xgb
import numpy as np
import os
from google.cloud import storage

app = FastAPI()


MODEL_PATH = os.getenv("AIP_STORAGE_URI", "")
LOCAL_MODEL_PATH = "/tmp/model.pkl"  # Vertex AI writable local path

print(f"🔹 Downloading model from {MODEL_PATH}")

if MODEL_PATH.startswith("gs://"):
    # Split bucket aur path
    path_parts = MODEL_PATH.replace("gs://", "").split("/", 1)
    bucket_name = path_parts[0]
    model_file = "model.pkl"
    prefix = path_parts[1] if len(path_parts) > 1 else ""

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"{prefix}/{model_file}")
    blob.download_to_filename(LOCAL_MODEL_PATH)
    print("✅ Model downloaded successfully to /tmp/")
else:
    LOCAL_MODEL_PATH = os.path.join(MODEL_PATH, "model.pkl")

# Load model
print(f"🔹 Loading model from {LOCAL_MODEL_PATH}")
model = joblib.load(LOCAL_MODEL_PATH)
print("✅ Model loaded successfully!")


@app.get("/")
def home():
    return {"status": "Vertex AI XGBoost Model is live 🚀"}


@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    instances = np.array(data["instances"])
    preds = model.predict(instances).tolist()
    return {"predictions": preds}
