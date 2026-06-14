from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.auth_utils import get_current_user
from app import models

router = APIRouter()


@router.patch("/{intervention_id}/complete")
def complete_intervention(
    intervention_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    intervention = (
        db.query(models.Intervention)
        .filter(
            models.Intervention.id == intervention_id
        )
        .first()
    )

    if not intervention:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    intervention.applied = True
    intervention.applied_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Completed"
    }