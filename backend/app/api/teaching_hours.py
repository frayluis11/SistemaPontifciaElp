from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import TeachingHour, User
from app.schemas.schemas import TeachingHourCreate, TeachingHour as TeachingHourSchema, TeachingHourUpdate
from .dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=TeachingHourSchema)
def create_teaching_hour(
    teaching_hour: TeachingHourCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new teaching hour entry."""
    # Only teachers can create teaching hours
    if current_user.role.value != "Docente":
        raise HTTPException(status_code=403, detail="Only teachers can create teaching hours")
    
    db_teaching_hour = TeachingHour(
        **teaching_hour.dict(),
        teacher_id=current_user.id
    )
    db.add(db_teaching_hour)
    db.commit()
    db.refresh(db_teaching_hour)
    return db_teaching_hour


@router.get("/", response_model=List[TeachingHourSchema])
def get_teaching_hours(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get teaching hours."""
    # Teachers see their own, admin/RRHH/Contabilidad see all
    if current_user.role.value in ["TI", "Administración", "RRHH", "Contabilidad"]:
        hours = db.query(TeachingHour).offset(skip).limit(limit).all()
    else:
        hours = db.query(TeachingHour).filter(
            TeachingHour.teacher_id == current_user.id
        ).offset(skip).limit(limit).all()
    return hours


@router.get("/{hour_id}", response_model=TeachingHourSchema)
def get_teaching_hour(
    hour_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific teaching hour entry."""
    hour = db.query(TeachingHour).filter(TeachingHour.id == hour_id).first()
    if not hour:
        raise HTTPException(status_code=404, detail="Teaching hour not found")
    
    # Check permissions
    if hour.teacher_id != current_user.id and current_user.role.value not in ["TI", "Administración", "RRHH", "Contabilidad"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return hour


@router.put("/{hour_id}", response_model=TeachingHourSchema)
def update_teaching_hour(
    hour_id: int,
    hour_update: TeachingHourUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a teaching hour entry."""
    hour = db.query(TeachingHour).filter(TeachingHour.id == hour_id).first()
    if not hour:
        raise HTTPException(status_code=404, detail="Teaching hour not found")
    
    # Teachers can update their own, admin/RRHH can update any
    if hour.teacher_id != current_user.id and current_user.role.value not in ["TI", "Administración", "RRHH"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in hour_update.dict(exclude_unset=True).items():
        setattr(hour, key, value)
    
    db.commit()
    db.refresh(hour)
    return hour


@router.post("/{hour_id}/approve", response_model=TeachingHourSchema)
def approve_teaching_hour(
    hour_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve a teaching hour entry."""
    # Only RRHH and admin can approve
    if current_user.role.value not in ["RRHH", "Administración", "TI"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve")
    
    hour = db.query(TeachingHour).filter(TeachingHour.id == hour_id).first()
    if not hour:
        raise HTTPException(status_code=404, detail="Teaching hour not found")
    
    hour.is_approved = True
    hour.approved_by = current_user.id
    
    db.commit()
    db.refresh(hour)
    return hour


@router.delete("/{hour_id}")
def delete_teaching_hour(
    hour_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a teaching hour entry."""
    hour = db.query(TeachingHour).filter(TeachingHour.id == hour_id).first()
    if not hour:
        raise HTTPException(status_code=404, detail="Teaching hour not found")
    
    # Teachers can delete their own, admin can delete any
    if hour.teacher_id != current_user.id and current_user.role.value not in ["TI", "Administración"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(hour)
    db.commit()
    return {"message": "Teaching hour deleted successfully"}
