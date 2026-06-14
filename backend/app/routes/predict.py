from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth_utils import get_current_user
from app import models
from pathlib import Path
import sys, json, io
import pandas as pd

# Point to the ml/ folder so we can import the Phase 2 files
ML_DIR = Path(__file__).resolve().parents[3] / "ml"
sys.path.append(str(ML_DIR))
from shap_utils import get_shap_explanation
from interventions import generate_interventions

router = APIRouter()

@router.post("/single")
def predict_single(student: dict,
                   db: Session = Depends(get_db),
                   user = Depends(get_current_user)):
    result  = get_shap_explanation(student)
    actions = generate_interventions(student, result['shap_factors'])
    record  = models.Student(
        name=student.get('name','Unknown'),
        teacher_id=user['id'],
        risk_score=result['risk_score'],
        risk_level=result['risk_level'],
        absences=student.get('absences',0),
        studytime=student.get('studytime',2),
        failures=student.get('failures',0),
        shap_json=json.dumps(result['shap_factors'])
    )
    db.add(record); db.flush()
    for a in actions:
        db.add(models.Intervention(
            student_id=record.id,
            action=a['action'],
            action_type=a['type'],
            priority=a['priority']
        ))
    db.commit(); db.refresh(record)
    return {"student_id": record.id, **result, "interventions": actions}

@router.post("/upload")
def upload_csv(file: UploadFile = File(...),
               db: Session = Depends(get_db),
               user = Depends(get_current_user)):

    df = pd.read_csv(io.BytesIO(file.file.read()))
    results = []

    for _, row in df.iterrows():

        student_dict = row.to_dict()

        res = get_shap_explanation(student_dict)
        actions = generate_interventions(
            student_dict,
            res["shap_factors"]
        )

        # Save student
        record = models.Student(
            name=student_dict.get("name", "Unknown"),
            teacher_id=user["id"],
            risk_score=res["risk_score"],
            risk_level=res["risk_level"],
            absences=student_dict.get("absences", 0),
            studytime=student_dict.get("studytime", 2),
            failures=student_dict.get("failures", 0),
            shap_json=json.dumps(res["shap_factors"])
        )

        db.add(record)
        db.flush()

        # Save interventions
        for a in actions:
            db.add(
                models.Intervention(
                    student_id=record.id,
                    action=a["action"],
                    action_type=a["type"],
                    priority=a["priority"]
                )
            )

        results.append({
            "student_id": record.id,
            "name": student_dict.get("name", ""),
            **res
        })

    db.commit()

    return {
        "count": len(results),
        "students": results
    }