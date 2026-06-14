import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("data/student-mat.csv", sep=";")

df["at_risk"] = (df["G3"] < 10).astype(int)

FEATURES = [
    "absences",
    "studytime",
    "failures",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "famrel",
    "traveltime"
]

X = df[FEATURES]
y = df["at_risk"]

# -----------------------------
# Same split as training
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Load saved artifacts
# -----------------------------

model = joblib.load("models/xgb_model.pkl")
scaler = joblib.load("models/scaler.pkl")

X_test_s = scaler.transform(X_test)

# -----------------------------
# Predictions
# -----------------------------

y_pred = model.predict(X_test_s)

y_prob = model.predict_proba(X_test_s)[:, 1]

# -----------------------------
# Metrics
# -----------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

roc_auc = roc_auc_score(y_test, y_prob)

print("\n==========================")
print(" FAILSAFE MODEL RESULTS")
print("==========================\n")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}")

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, y_pred))

print("\nClassification Report\n")

print(classification_report(
    y_test,
    y_pred,
    target_names=[
        "Not At Risk",
        "At Risk"
    ]
))