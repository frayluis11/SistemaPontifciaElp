"""
Database initialization script with sample data
Run this script to populate the database with test users and data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.models import User, Document, TeachingHour, Report, RoleEnum
from app.core.security import get_password_hash
from datetime import datetime, timedelta


def init_db():
    """Initialize database with sample data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Create sample users
        users = [
            User(
                username="admin",
                email="admin@pontificia.edu",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrador Sistema",
                role=RoleEnum.ADMINISTRACION,
                is_active=True
            ),
            User(
                username="docente1",
                email="docente1@pontificia.edu",
                hashed_password=get_password_hash("docente123"),
                full_name="Juan Pérez García",
                role=RoleEnum.DOCENTE,
                is_active=True
            ),
            User(
                username="docente2",
                email="docente2@pontificia.edu",
                hashed_password=get_password_hash("docente123"),
                full_name="María López Ruiz",
                role=RoleEnum.DOCENTE,
                is_active=True
            ),
            User(
                username="rrhh1",
                email="rrhh@pontificia.edu",
                hashed_password=get_password_hash("rrhh123"),
                full_name="Carlos Sánchez",
                role=RoleEnum.RRHH,
                is_active=True
            ),
            User(
                username="conta1",
                email="contabilidad@pontificia.edu",
                hashed_password=get_password_hash("conta123"),
                full_name="Ana Martínez",
                role=RoleEnum.CONTABILIDAD,
                is_active=True
            ),
            User(
                username="ti1",
                email="ti@pontificia.edu",
                hashed_password=get_password_hash("ti123"),
                full_name="Pedro Ramírez",
                role=RoleEnum.TI,
                is_active=True
            ),
        ]
        
        db.add_all(users)
        db.commit()
        
        # Refresh to get IDs
        for user in users:
            db.refresh(user)
        
        print(f"Created {len(users)} users")
        
        # Create sample documents
        documents = [
            Document(
                title="Contrato Docente 2024",
                description="Contrato de trabajo para el año académico 2024",
                document_type="Contrato",
                user_id=users[1].id,  # docente1
                is_signed=True,
                signature_data="firma_digital_123",
                signed_at=datetime.utcnow()
            ),
            Document(
                title="Certificado de Capacitación",
                description="Certificado de asistencia a curso de pedagogía",
                document_type="Certificado",
                user_id=users[1].id,  # docente1
                is_signed=False
            ),
            Document(
                title="Informe Mensual Enero",
                description="Informe de actividades del mes de enero",
                document_type="Informe",
                user_id=users[2].id,  # docente2
                is_signed=False
            ),
        ]
        
        db.add_all(documents)
        db.commit()
        
        print(f"Created {len(documents)} documents")
        
        # Create sample teaching hours
        base_date = datetime.utcnow() - timedelta(days=7)
        teaching_hours = [
            TeachingHour(
                teacher_id=users[1].id,  # docente1
                subject="Matemáticas I",
                course="1° Año A",
                hours=4.0,
                date=base_date,
                description="Clase de álgebra básica",
                is_approved=True,
                approved_by=users[3].id  # rrhh1
            ),
            TeachingHour(
                teacher_id=users[1].id,  # docente1
                subject="Matemáticas I",
                course="1° Año B",
                hours=3.5,
                date=base_date + timedelta(days=1),
                description="Clase de geometría",
                is_approved=True,
                approved_by=users[3].id  # rrhh1
            ),
            TeachingHour(
                teacher_id=users[2].id,  # docente2
                subject="Lengua y Literatura",
                course="2° Año A",
                hours=4.0,
                date=base_date + timedelta(days=2),
                description="Análisis de textos narrativos",
                is_approved=False
            ),
            TeachingHour(
                teacher_id=users[2].id,  # docente2
                subject="Lengua y Literatura",
                course="2° Año B",
                hours=3.0,
                date=base_date + timedelta(days=3),
                description="Gramática y ortografía",
                is_approved=False
            ),
        ]
        
        db.add_all(teaching_hours)
        db.commit()
        
        print(f"Created {len(teaching_hours)} teaching hour records")
        
        # Create sample reports
        reports = [
            Report(
                title="Reporte Mensual de Horas",
                report_type="Horas Docentes",
                content="Resumen de horas docentes del mes",
                created_by=users[3].id  # rrhh1
            ),
            Report(
                title="Reporte de Documentos Firmados",
                report_type="Documentos",
                content="Estado de documentos firmados",
                created_by=users[0].id  # admin
            ),
        ]
        
        db.add_all(reports)
        db.commit()
        
        print(f"Created {len(reports)} reports")
        
        print("\n✅ Database initialized successfully!")
        print("\nSample credentials:")
        print("  Admin:        admin / admin123")
        print("  Docente 1:    docente1 / docente123")
        print("  Docente 2:    docente2 / docente123")
        print("  RRHH:         rrhh1 / rrhh123")
        print("  Contabilidad: conta1 / conta123")
        print("  TI:           ti1 / ti123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
