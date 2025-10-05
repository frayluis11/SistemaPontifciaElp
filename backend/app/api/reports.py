from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse

from app.core.database import get_db
from app.models.models import Report, User, Document, TeachingHour
from app.schemas.schemas import ReportCreate, Report as ReportSchema
from .dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=ReportSchema)
def create_report(
    report: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new report."""
    db_report = Report(
        **report.dict(),
        created_by=current_user.id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.get("/", response_model=List[ReportSchema])
def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get reports."""
    # All roles can view reports
    reports = db.query(Report).offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ReportSchema)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/export/documents")
def export_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export documents to Excel."""
    # Only admin, RRHH, and Contabilidad can export
    if current_user.role.value not in ["TI", "Administración", "RRHH", "Contabilidad"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    documents = db.query(Document).all()
    
    # Convert to DataFrame
    data = [{
        "ID": doc.id,
        "Título": doc.title,
        "Tipo": doc.document_type,
        "Usuario ID": doc.user_id,
        "Firmado": doc.is_signed,
        "Fecha Creación": doc.created_at
    } for doc in documents]
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Documentos', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment; filename=documentos.xlsx"}
    )


@router.get("/export/teaching-hours")
def export_teaching_hours(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export teaching hours to Excel."""
    # Only admin, RRHH, and Contabilidad can export
    if current_user.role.value not in ["TI", "Administración", "RRHH", "Contabilidad"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    hours = db.query(TeachingHour).all()
    
    # Convert to DataFrame
    data = [{
        "ID": h.id,
        "Profesor ID": h.teacher_id,
        "Materia": h.subject,
        "Curso": h.course,
        "Horas": h.hours,
        "Fecha": h.date,
        "Aprobado": h.is_approved,
        "Fecha Creación": h.created_at
    } for h in hours]
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Horas Docentes', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment; filename=horas_docentes.xlsx"}
    )


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Only creator or admin can delete
    if report.created_by != current_user.id and current_user.role.value not in ["TI", "Administración"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}
