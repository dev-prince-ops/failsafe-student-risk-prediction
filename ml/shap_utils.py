import shap
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

def get_shap_explanation(student_data: dict) -> dict:
    """
    Takes a dict of student features.
    Returns risk score + top 3 SHAP factors as plain English.
    """

    model = joblib.load(MODEL_DIR / "xgb_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    features = joblib.load(MODEL_DIR / "features.pkl")

    df = pd.DataFrame([student_data])[features]
    X = scaler.transform(df)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    risk_score = float(model.predict_proba(X)[0][1])

    risk_level = (
        "High" if risk_score > 0.7
        else "Medium" if risk_score > 0.4
        else "Low"
    )

    sv = dict(zip(features, shap_values[0]))
    top3 = sorted(
        sv.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]

    factors = []

    for feat, val in top3:
        direction = "increases" if val > 0 else "decreases"

        factors.append({
            "feature": feat,
            "shap_value": round(float(val), 3),
            "impact": direction,
            "readable": f"{feat} {direction} risk"
        })

    return {
        "risk_score": round(risk_score, 3),
        "risk_level": risk_level,
        "shap_factors": factors
    }