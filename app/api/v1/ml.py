from fastapi import APIRouter, Depends
from pydantic import BaseModel
import joblib
import os

router = APIRouter(
    prefix="/ml",
    tags=["ML Services"]
)

# --------------------------------------------------------
# MODELS FOR INPUT
# --------------------------------------------------------
class RiskPredictionInput(BaseModel):
    age: int
    avg_gpa_last_sem: float
    courses_failed: int
    attendance_rate: float

class GPAInput(BaseModel):
    credits_taken: int
    assignment_score: float
    exam_score: float


# --------------------------------------------------------
# DUMMY TEST ROUTE (guaranteed to run)
# --------------------------------------------------------
@router.get("/test")
def test():
    return {
        "message": "ML router is working!",
        "status": "ok"
    }


# --------------------------------------------------------
# RISK PREDICTION ENDPOINT (placeholder)
# --------------------------------------------------------
@router.post("/predict-risk")
def predict_risk(data: RiskPredictionInput):
    # Replace later with real model load
    # Ex:
    # artifact = joblib.load("models/risk_model_v1.joblib")
    # model = artifact["model"]
    # scaler = artifact["scaler"]
    # ...
    risk_score = (
        (data.avg_gpa_last_sem * -0.8) +
        (data.courses_failed * 1.2) +
        ((1 - data.attendance_rate) * 1.4) +
        (0.01 * data.age)
    )

    return {
        "predicted_risk_score": round(risk_score, 3)
    }


# --------------------------------------------------------
# GPA PREDICTION ENDPOINT (placeholder)
# --------------------------------------------------------
@router.post("/predict-gpa")
def predict_gpa(data: GPAInput):
    # Example placeholder formula
    predicted_gpa = (
        (data.assignment_score * 0.4) +
        (data.exam_score * 0.6)
    ) / 25  # normalize to 0–4 scale

    return {
        "predicted_gpa": round(predicted_gpa, 2)
    }
