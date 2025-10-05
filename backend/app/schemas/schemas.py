from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import RoleEnum


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: RoleEnum


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Document Schemas
class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    document_type: str


class DocumentCreate(DocumentBase):
    file_name: Optional[str] = None
    file_path: Optional[str] = None


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_signed: Optional[bool] = None
    signature_data: Optional[str] = None


class Document(DocumentBase):
    id: int
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    user_id: int
    is_signed: bool
    signature_data: Optional[str] = None
    signed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Teaching Hour Schemas
class TeachingHourBase(BaseModel):
    subject: str
    course: str
    hours: float
    date: datetime
    description: Optional[str] = None


class TeachingHourCreate(TeachingHourBase):
    pass


class TeachingHourUpdate(BaseModel):
    subject: Optional[str] = None
    course: Optional[str] = None
    hours: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    is_approved: Optional[bool] = None


class TeachingHour(TeachingHourBase):
    id: int
    teacher_id: int
    is_approved: bool
    approved_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Report Schemas
class ReportBase(BaseModel):
    title: str
    report_type: str
    content: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    report_type: Optional[str] = None
    content: Optional[str] = None


class Report(ReportBase):
    id: int
    file_path: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str
