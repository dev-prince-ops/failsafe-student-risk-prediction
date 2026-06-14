from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth_utils import get_current_user
from app import models

router = APIRouter()


@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    students = (
        db.query(models.Student)
        .filter(models.Student.teacher_id == user["id"])
        .all()
    )

    return {
        "total": len(students),
        "high": len([s for s in students if s.risk_level == "High"]),
        "medium": len([s for s in students if s.risk_level == "Medium"]),
        "low": len([s for s in students if s.risk_level == "Low"]),
    }