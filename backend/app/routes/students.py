from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.auth_utils import get_current_user
from app import models

router = APIRouter()


@router.get("/")
def get_students(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    students = (
        db.query(models.Student)
        .filter(models.Student.teacher_id == user["id"])
        .order_by(models.Student.id.desc())
        .all()
    )

    results = []

    for s in students:

        interventions = (
            db.query(models.Intervention)
            .filter(models.Intervention.student_id == s.id)
            .all()
        )

        results.append({
            "id": s.id,
            "name": s.name,
            "risk_score": s.risk_score,
            "risk_level": s.risk_level,
            "absences": s.absences,
            "failures": s.failures,
            "studytime": s.studytime,
            "created_at": str(s.created_at),
            "shap_factors": json.loads(s.shap_json),
            "interventions": [
                {
                    "id": i.id,
                    "action": i.action,
                    "priority": i.priority,
                    "type": i.action_type,
                    "applied": i.applied
                }
                for i in interventions
            ]
        })

    return results


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    s = (
        db.query(models.Student)
        .filter(
            models.Student.id == student_id,
            models.Student.teacher_id == user["id"]
        )
        .first()
    )

    if not s:
        raise HTTPException(404, "Student not found")

    interventions = (
        db.query(models.Intervention)
        .filter(models.Intervention.student_id == s.id)
        .all()
    )

    return {
        "id": s.id,
        "name": s.name,
        "risk_score": s.risk_score,
        "risk_level": s.risk_level,
        "absences": s.absences,
        "failures": s.failures,
        "studytime": s.studytime,
        "created_at": str(s.created_at),
        "shap_factors": json.loads(s.shap_json),
        "interventions": [
            {
                "id": i.id,
                "action": i.action,
                "priority": i.priority,
                "type": i.action_type,
                "applied": i.applied
            }
            for i in interventions
        ]
    }


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    student = (
        db.query(models.Student)
        .filter(
            models.Student.id == student_id,
            models.Student.teacher_id == user["id"]
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.query(models.Intervention).filter(
        models.Intervention.student_id == student_id
    ).delete()

    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted"
    }