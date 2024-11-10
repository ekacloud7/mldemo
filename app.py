from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the trained model and scaler
model = pickle.load(open("regmodel.pkl", "rb"))
scaler = pickle.load(open("scaling.pkl", "rb"))

# Define input data structure
class PredictionRequest(BaseModel):
    data: list[float]

@app.post("/predict/")
def predict(request: PredictionRequest):
    # Preprocess the input data
    input_data = np.array(request.data).reshape(1, -1)
    scaled_data = scaler.transform(input_data)

    # Predict using the trained model
    prediction = model.predict(scaled_data)
    return {"prediction": prediction.tolist()}
