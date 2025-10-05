# Sistema Pontificia ELP

Sistema web distribuido para la Escuela Superior La Pontificia, que gestiona documentos laborales, horas docentes y reportes digitales.

## 🚀 Características

- **Gestión de Documentos Laborales**: Creación, visualización y gestión de documentos importantes
- **Firma Digital**: Capacidad de firmar documentos digitalmente
- **Registro de Horas Docentes**: Los docentes pueden registrar sus horas de trabajo
- **Aprobación de Horas**: RRHH y Administración pueden aprobar horas docentes
- **Reportes Digitales**: Generación y visualización de reportes del sistema
- **Exportación de Datos**: Exportar información a Excel para análisis
- **Dashboards Personalizados**: Diferentes vistas según el rol del usuario
- **Seguridad**: Autenticación JWT y control de acceso basado en roles

## 👥 Roles del Sistema

El sistema soporta 5 roles diferentes:

1. **Docente**: Puede gestionar sus documentos y registrar horas docentes
2. **RRHH**: Puede ver y aprobar horas docentes, gestionar documentos y generar reportes
3. **Contabilidad**: Acceso a reportes financieros y exportación de datos
4. **Administración**: Acceso completo al sistema
5. **TI**: Administración técnica del sistema

## 🛠 Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para Python
- **JWT**: Autenticación segura con tokens
- **Pydantic**: Validación de datos
- **ReportLab & Pandas**: Generación de reportes

### Frontend
- **React 18**: Librería de UI moderna
- **React Router**: Navegación en la aplicación
- **Axios**: Cliente HTTP para API REST
- **Vite**: Build tool rápido y moderno

### DevOps
- **Docker**: Containerización de aplicaciones
- **Docker Compose**: Orquestación de contenedores

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Git para clonar el repositorio

## 🚀 Instalación y Ejecución

### Usando Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone https://github.com/frayluis11/SistemaPontifciaElp.git
cd SistemaPontifciaElp
```

2. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp backend/.env.example backend/.env

# Editar backend/.env y configurar:
# - DATABASE_URL
# - SECRET_KEY (cambiar por una clave segura en producción)
```

3. **Iniciar los contenedores**
```bash
docker-compose up -d
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

### Instalación Manual

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar servidor
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

## 📊 Estructura del Proyecto

```
SistemaPontifciaElp/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints de la API
│   │   │   ├── auth.py       # Autenticación
│   │   │   ├── documents.py  # Gestión de documentos
│   │   │   ├── teaching_hours.py  # Horas docentes
│   │   │   └── reports.py    # Reportes
│   │   ├── core/             # Configuración central
│   │   │   ├── config.py     # Configuraciones
│   │   │   ├── database.py   # Conexión DB
│   │   │   └── security.py   # JWT y seguridad
│   │   ├── models/           # Modelos de base de datos
│   │   └── schemas/          # Esquemas Pydantic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/            # Páginas principales
│   │   ├── services/         # Servicios API
│   │   ├── contexts/         # Context API
│   │   └── utils/            # Utilidades
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔐 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración configurable
- **Hash de Contraseñas**: Usando bcrypt para almacenamiento seguro
- **Control de Acceso Basado en Roles**: Permisos granulares por rol
- **CORS Configurado**: Para prevenir acceso no autorizado
- **Variables de Entorno**: Credenciales y secretos fuera del código

## 📱 Funcionalidades por Rol

### Docente
- Ver y crear documentos personales
- Firmar documentos digitalmente
- Registrar horas docentes
- Ver estado de aprobación de horas

### RRHH
- Gestionar todos los documentos
- Aprobar horas docentes
- Generar reportes de personal
- Exportar datos a Excel

### Contabilidad
- Ver documentos financieros
- Exportar datos para análisis
- Ver reportes contables

### Administración
- Acceso completo a todos los módulos
- Gestión de usuarios
- Aprobación de horas docentes
- Generación de reportes

### TI
- Administración técnica completa
- Gestión de usuarios y roles
- Acceso a logs y estadísticas

## 🔄 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Documentos
- `GET /api/documents/` - Listar documentos
- `POST /api/documents/` - Crear documento
- `GET /api/documents/{id}` - Obtener documento
- `PUT /api/documents/{id}` - Actualizar documento
- `DELETE /api/documents/{id}` - Eliminar documento
- `POST /api/documents/{id}/sign` - Firmar documento

### Horas Docentes
- `GET /api/teaching-hours/` - Listar horas
- `POST /api/teaching-hours/` - Crear registro
- `GET /api/teaching-hours/{id}` - Obtener registro
- `PUT /api/teaching-hours/{id}` - Actualizar registro
- `DELETE /api/teaching-hours/{id}` - Eliminar registro
- `POST /api/teaching-hours/{id}/approve` - Aprobar horas

### Reportes
- `GET /api/reports/` - Listar reportes
- `POST /api/reports/` - Crear reporte
- `GET /api/reports/export/documents` - Exportar documentos a Excel
- `GET /api/reports/export/teaching-hours` - Exportar horas a Excel

## 🧪 Testing

La documentación interactiva de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es privado y pertenece a la Escuela Superior La Pontificia.

## 📧 Contacto

Para soporte o consultas, contactar al equipo de TI de la institución.

## 🔮 Roadmap

- [ ] Implementación de firma digital con certificados
- [ ] Notificaciones por email
- [ ] Sistema de backup automático
- [ ] App móvil
- [ ] Integración con sistemas externos
- [ ] Reportes avanzados con gráficos
- [ ] Sistema de auditoría completo