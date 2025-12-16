import joblib
import numpy as np
from pathlib import Path
from app.repositories.mongo_repo import MongoRepo


class MLService:
    """
    MLService loads trained ML model artifacts and exposes prediction functions.
    This service handles:
        - loading model, scaler, imputer
        - single prediction
        - bulk prediction saving
    """

    MODEL_PATH = Path("models/risk_model_v1.joblib")

    def __init__(self):
        """
        Load model artifacts from disk if available.
        """
        if self.MODEL_PATH.exists():
            artifacts = joblib.load(self.MODEL_PATH)
            self.model = artifacts.get("model")
            self.imputer = artifacts.get("imputer")
            self.scaler = artifacts.get("scaler")
        else:
            self.model = None
            self.imputer = None
            self.scaler = None

    # ----------------------------------------------------
    # Single Prediction
    # ----------------------------------------------------
    def predict_risk(self, feature_list: list) -> float:
        """
        Predict the risk probability of a student.

        Args:
            feature_list: list of numeric features

        Returns:
            float: probability (0 - 1)
        """
        if self.model is None:
            raise RuntimeError("Risk model not found. Train the model first.")

        # Convert to numpy array
        X = np.array([feature_list])

        # Apply imputer if available
        if self.imputer is not None:
            X = self.imputer.transform(X)

        # Apply scaler if available
        if self.scaler is not None:
            X = self.scaler.transform(X)

        prob = self.model.predict_proba(X)[0][1]
        return float(prob)

    # ----------------------------------------------------
    # Bulk Prediction Saving (for ETL)
    # ----------------------------------------------------
    def bulk_save_predictions(self, pred_list: list):
        """
        Save ML results to MongoDB.

        pred_list format example:
        [
            {
                "StudentID": 12,
                "risk_prob": 0.82,
            },
            {
                "StudentID": 5,
                "risk_prob": 0.21,
            }
        ]
        """
        if not pred_list:
            return

        MongoRepo.insert_predictions(pred_list)
