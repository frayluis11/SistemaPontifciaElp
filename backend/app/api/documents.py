from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Document, User
from app.schemas.schemas import DocumentCreate, Document as DocumentSchema, DocumentUpdate
from .dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=DocumentSchema)
def create_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new document."""
    db_document = Document(
        **document.dict(),
        user_id=current_user.id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get("/", response_model=List[DocumentSchema])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's documents."""
    # Admin and RRHH can see all documents
    if current_user.role.value in ["TI", "Administración", "RRHH"]:
        documents = db.query(Document).offset(skip).limit(limit).all()
    else:
        documents = db.query(Document).filter(
            Document.user_id == current_user.id
        ).offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if document.user_id != current_user.id and current_user.role.value not in ["TI", "Administración", "RRHH"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return document


@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if document.user_id != current_user.id and current_user.role.value not in ["TI", "Administración", "RRHH"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in document_update.dict(exclude_unset=True).items():
        setattr(document, key, value)
    
    db.commit()
    db.refresh(document)
    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if document.user_id != current_user.id and current_user.role.value not in ["TI", "Administración"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}


@router.post("/{document_id}/sign", response_model=DocumentSchema)
def sign_document(
    document_id: int,
    signature_data: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sign a document with digital signature."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    from datetime import datetime
    document.is_signed = True
    document.signature_data = signature_data
    document.signed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(document)
    return document
