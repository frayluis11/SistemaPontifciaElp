# Arquitectura del Sistema Pontificia ELP

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE WEB                              │
│                      (React + Vite)                              │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Login/    │  │  Dashboard  │  │  Documentos │            │
│  │  Register   │  │             │  │             │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Horas     │  │   Reportes  │  │   Perfil    │            │
│  │  Docentes   │  │             │  │             │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS + JWT
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      BACKEND API                                 │
│                    (FastAPI + Python)                            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API ENDPOINTS                         │   │
│  │                                                          │   │
│  │  /api/auth/*          - Autenticación y Registro        │   │
│  │  /api/documents/*     - Gestión de Documentos           │   │
│  │  /api/teaching-hours/* - Gestión de Horas Docentes      │   │
│  │  /api/reports/*       - Reportes y Exportación          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Security  │  │   Business  │  │    Data     │            │
│  │   (JWT)     │  │    Logic    │  │   Models    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ SQL (SQLAlchemy ORM)
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    BASE DE DATOS                                 │
│                   (PostgreSQL 15)                                │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │    Users    │  │  Documents  │  │  Teaching   │            │
│  │             │  │             │  │    Hours    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                   │
│  ┌─────────────┐                                                │
│  │   Reports   │                                                │
│  │             │                                                │
│  └─────────────┘                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

### 1. Autenticación

```
Usuario → Login Form → POST /api/auth/login → Verify Credentials
                                              ↓
                                         Generate JWT
                                              ↓
                                    Return Token to Client
                                              ↓
                              Store in localStorage/Context
```

### 2. Operaciones CRUD (Ejemplo: Documentos)

```
Usuario → Acción → Componente React → API Service (axios)
                                             ↓
                                    Incluir JWT Token
                                             ↓
                          POST/GET/PUT/DELETE /api/documents/*
                                             ↓
                                      Validate Token
                                             ↓
                                    Check Permissions
                                             ↓
                                   Database Operation
                                             ↓
                                    Return Response
                                             ↓
                              Update UI (React State)
```

## 🏗️ Estructura de Capas

### Frontend (React)

```
src/
├── pages/          → Páginas principales de la aplicación
├── components/     → Componentes reutilizables
├── services/       → Llamadas a la API
├── contexts/       → Estado global (Auth, etc.)
├── utils/          → Funciones auxiliares
└── App.jsx         → Componente principal y rutas
```

**Responsabilidades:**
- Presentación de datos
- Interacción con usuario
- Validación de formularios
- Gestión de estado local
- Navegación

### Backend (FastAPI)

```
app/
├── api/            → Endpoints y controladores
├── models/         → Modelos de base de datos (SQLAlchemy)
├── schemas/        → Validación de datos (Pydantic)
├── core/           → Configuración, seguridad, database
└── main.py         → Aplicación principal
```

**Responsabilidades:**
- Lógica de negocio
- Validación de datos
- Autenticación y autorización
- Operaciones de base de datos
- Generación de reportes

### Base de Datos (PostgreSQL)

```
Tables:
├── users           → Usuarios del sistema
├── documents       → Documentos laborales
├── teaching_hours  → Registro de horas docentes
└── reports         → Reportes generados
```

**Responsabilidades:**
- Persistencia de datos
- Integridad referencial
- Consultas eficientes
- Transacciones ACID

## 🔐 Seguridad

### Autenticación JWT

```
1. Usuario envía credenciales
2. Backend valida y genera JWT
3. JWT contiene: {user_id, username, role, exp}
4. Cliente almacena JWT
5. Cada request incluye: Authorization: Bearer <token>
6. Backend valida token en cada request
```

### Control de Acceso

```python
Roles:
├── Docente         → Acceso a sus documentos y horas
├── RRHH            → Gestión completa de personal
├── Contabilidad    → Reportes financieros
├── Administración  → Acceso completo
└── TI              → Administración técnica

Permisos por Endpoint:
- POST /documents/    → Todos los roles autenticados
- GET /documents/     → Filtrado por rol
- POST /*/approve     → Solo RRHH, Admin, TI
- GET /reports/export → Solo RRHH, Conta, Admin, TI
```

## 🔌 Integraciones

### Exportación de Datos

```
Frontend Request → Backend API → Generate DataFrame (Pandas)
                                        ↓
                                  Create Excel (openpyxl)
                                        ↓
                                Return File Stream
                                        ↓
                          Browser Download Dialog
```

### Firma Digital

```
Usuario → Canvas de Firma → Capture Signature Data
                                   ↓
                          Convert to Base64
                                   ↓
                     POST /documents/{id}/sign
                                   ↓
                        Update Database
                                   ↓
                  Mark Document as Signed
```

## 📊 Modelo de Datos

### Users
```sql
id: INTEGER (PK)
username: VARCHAR (UNIQUE)
email: VARCHAR (UNIQUE)
hashed_password: VARCHAR
full_name: VARCHAR
role: ENUM (Docente, RRHH, Contabilidad, Administración, TI)
is_active: BOOLEAN
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### Documents
```sql
id: INTEGER (PK)
title: VARCHAR
description: TEXT
document_type: VARCHAR
file_path: VARCHAR
file_name: VARCHAR
user_id: INTEGER (FK → users.id)
is_signed: BOOLEAN
signature_data: TEXT
signed_at: TIMESTAMP
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### Teaching Hours
```sql
id: INTEGER (PK)
teacher_id: INTEGER (FK → users.id)
subject: VARCHAR
course: VARCHAR
hours: FLOAT
date: TIMESTAMP
description: TEXT
is_approved: BOOLEAN
approved_by: INTEGER (FK → users.id)
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### Reports
```sql
id: INTEGER (PK)
title: VARCHAR
report_type: VARCHAR
content: TEXT
file_path: VARCHAR
created_by: INTEGER (FK → users.id)
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

## 🐳 Contenedorización

```
Docker Compose Stack:
├── db          → PostgreSQL 15 (Puerto 5432)
├── backend     → FastAPI (Puerto 8000)
└── frontend    → React + Vite (Puerto 3000)

Networks:
└── pontificia_network (Bridge)

Volumes:
└── postgres_data → Persistencia de datos
```

## 🚀 Flujo de Despliegue

```
Desarrollo:
1. Cambios en código
2. Hot-reload automático (Vite/Uvicorn)
3. Testing local

Staging/Producción:
1. Git push
2. CI/CD (opcional)
3. Build Docker images
4. Deploy a servidor
5. Configurar HTTPS
6. Iniciar servicios
```

## 📈 Escalabilidad

### Horizontal
- Load balancer (Nginx/HAProxy)
- Múltiples instancias de backend
- Database replication

### Vertical
- Aumentar recursos de contenedores
- Optimización de queries
- Caché (Redis)

### Optimizaciones
- Paginación en listados
- Índices en base de datos
- Lazy loading en frontend
- Compresión de respuestas
- CDN para assets estáticos
