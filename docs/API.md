# API Documentation - Sistema Pontificia ELP

## 🌐 Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## 🔐 Autenticación

Todas las rutas (excepto `/api/auth/login` y `/api/auth/register`) requieren autenticación JWT.

### Formato del Header

```
Authorization: Bearer <your-jwt-token>
```

## 📋 Endpoints

### Authentication

#### POST /api/auth/register
Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string",
  "role": "Docente" | "RRHH" | "Contabilidad" | "Administración" | "TI"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "juan.perez",
  "email": "juan@pontificia.edu",
  "full_name": "Juan Pérez",
  "role": "Docente",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

**Errors:**
- `400 Bad Request`: Usuario o email ya existe

---

#### POST /api/auth/login
Inicia sesión y obtiene un token JWT.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401 Unauthorized`: Credenciales incorrectas
- `400 Bad Request`: Usuario inactivo

---

#### GET /api/auth/me
Obtiene información del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "juan.perez",
  "email": "juan@pontificia.edu",
  "full_name": "Juan Pérez",
  "role": "Docente",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

---

#### GET /api/auth/users
Lista todos los usuarios (Solo Admin/TI).

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: número (default: 0) - Offset para paginación
- `limit`: número (default: 100) - Límite de resultados

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "juan.perez",
    "email": "juan@pontificia.edu",
    "full_name": "Juan Pérez",
    "role": "Docente",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

**Errors:**
- `403 Forbidden`: No autorizado

---

### Documents

#### POST /api/documents/
Crea un nuevo documento.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "document_type": "string",
  "file_name": "string (optional)",
  "file_path": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Contrato Docente 2024",
  "description": "Contrato para el año académico",
  "document_type": "Contrato",
  "file_path": null,
  "file_name": null,
  "user_id": 1,
  "is_signed": false,
  "signature_data": null,
  "signed_at": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

---

#### GET /api/documents/
Lista documentos del usuario (o todos si es admin/RRHH).

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: número (default: 0)
- `limit`: número (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Contrato Docente 2024",
    "document_type": "Contrato",
    "is_signed": true,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

#### GET /api/documents/{document_id}
Obtiene un documento específico.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Contrato Docente 2024",
  "description": "Contrato para el año académico",
  "document_type": "Contrato",
  "file_path": null,
  "file_name": null,
  "user_id": 1,
  "is_signed": true,
  "signature_data": "firma_base64...",
  "signed_at": "2024-01-15T11:00:00",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

**Errors:**
- `404 Not Found`: Documento no existe
- `403 Forbidden`: No autorizado

---

#### PUT /api/documents/{document_id}
Actualiza un documento.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "is_signed": "boolean (optional)",
  "signature_data": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Contrato Actualizado",
  ...
}
```

**Errors:**
- `404 Not Found`: Documento no existe
- `403 Forbidden`: No autorizado

---

#### DELETE /api/documents/{document_id}
Elimina un documento.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Document deleted successfully"
}
```

**Errors:**
- `404 Not Found`: Documento no existe
- `403 Forbidden`: No autorizado

---

#### POST /api/documents/{document_id}/sign
Firma un documento digitalmente.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `signature_data`: string - Datos de la firma digital

**Response (200 OK):**
```json
{
  "id": 1,
  "is_signed": true,
  "signature_data": "firma_digital...",
  "signed_at": "2024-01-15T11:00:00",
  ...
}
```

**Errors:**
- `404 Not Found`: Documento no existe
- `403 Forbidden`: Solo el propietario puede firmar

---

### Teaching Hours

#### POST /api/teaching-hours/
Registra horas docentes (Solo Docentes).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "subject": "string",
  "course": "string",
  "hours": 4.0,
  "date": "2024-01-15T08:00:00",
  "description": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "teacher_id": 1,
  "subject": "Matemáticas I",
  "course": "1° Año A",
  "hours": 4.0,
  "date": "2024-01-15T08:00:00",
  "description": "Clase de álgebra",
  "is_approved": false,
  "approved_by": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

**Errors:**
- `403 Forbidden`: Solo docentes pueden crear registros

---

#### GET /api/teaching-hours/
Lista horas docentes.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: número (default: 0)
- `limit`: número (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "teacher_id": 1,
    "subject": "Matemáticas I",
    "course": "1° Año A",
    "hours": 4.0,
    "date": "2024-01-15T08:00:00",
    "is_approved": true,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

#### GET /api/teaching-hours/{hour_id}
Obtiene un registro específico.

**Response (200 OK):**
```json
{
  "id": 1,
  "teacher_id": 1,
  "subject": "Matemáticas I",
  ...
}
```

**Errors:**
- `404 Not Found`: Registro no existe
- `403 Forbidden`: No autorizado

---

#### PUT /api/teaching-hours/{hour_id}
Actualiza un registro de horas.

**Request Body:**
```json
{
  "subject": "string (optional)",
  "course": "string (optional)",
  "hours": "number (optional)",
  "date": "datetime (optional)",
  "description": "string (optional)",
  "is_approved": "boolean (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "subject": "Matemáticas Actualizado",
  ...
}
```

---

#### POST /api/teaching-hours/{hour_id}/approve
Aprueba horas docentes (Solo RRHH/Admin/TI).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "is_approved": true,
  "approved_by": 3,
  ...
}
```

**Errors:**
- `403 Forbidden`: No autorizado para aprobar
- `404 Not Found`: Registro no existe

---

#### DELETE /api/teaching-hours/{hour_id}
Elimina un registro de horas.

**Response (200 OK):**
```json
{
  "message": "Teaching hour deleted successfully"
}
```

---

### Reports

#### GET /api/reports/
Lista reportes generados.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: número (default: 0)
- `limit`: número (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Reporte Mensual",
    "report_type": "Horas Docentes",
    "content": "...",
    "file_path": null,
    "created_by": 3,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

#### POST /api/reports/
Crea un nuevo reporte.

**Request Body:**
```json
{
  "title": "string",
  "report_type": "string",
  "content": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Reporte Mensual",
  "report_type": "Documentos",
  "created_by": 3,
  "created_at": "2024-01-15T10:30:00"
}
```

---

#### GET /api/reports/export/documents
Exporta documentos a Excel (RRHH/Conta/Admin/TI).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Archivo Excel descargable

**Errors:**
- `403 Forbidden`: No autorizado

---

#### GET /api/reports/export/teaching-hours
Exporta horas docentes a Excel (RRHH/Conta/Admin/TI).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Archivo Excel descargable

**Errors:**
- `403 Forbidden`: No autorizado

---

## 🔍 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - No autorizado |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## 📝 Notas

- Todas las fechas están en formato ISO 8601: `YYYY-MM-DDTHH:mm:ss`
- Los tokens JWT expiran en 30 minutos por defecto
- Las contraseñas deben tener al menos 6 caracteres
- Los archivos Excel se generan en memoria y se envían como stream

## 🧪 Testing con cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Obtener documentos
curl -X GET "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Crear documento
curl -X POST "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","document_type":"Contrato","description":"Test doc"}'
```

## 📚 Interactive Documentation

Accede a la documentación interactiva (Swagger UI):
- http://localhost:8000/docs
