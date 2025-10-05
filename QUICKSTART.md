# Quick Start Guide - Sistema Pontificia ELP

## 🚀 Inicio Rápido (5 minutos)

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/frayluis11/SistemaPontifciaElp.git
cd SistemaPontifciaElp

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Esperar a que los servicios inicien (30-60 segundos)
docker-compose logs -f

# 4. Acceder a la aplicación
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Desarrollo Local

#### Backend

```bash
# Requisitos: Python 3.11+, PostgreSQL

cd backend

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
# Editar .env con tus credenciales de PostgreSQL
cp .env.example .env

# Iniciar servidor
uvicorn app.main:app --reload
# Servidor corriendo en http://localhost:8000
```

#### Frontend

```bash
# Requisitos: Node.js 18+

cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
# Aplicación corriendo en http://localhost:3000
```

## 👤 Primer Usuario

### Crear Usuario Administrador

1. **Navegar a http://localhost:3000/register**

2. **Llenar el formulario:**
   - Usuario: `admin`
   - Email: `admin@pontificia.edu`
   - Nombre: `Administrador`
   - Contraseña: `admin123` (cambiar en producción)
   - Rol: `TI` o `Administración`

3. **Iniciar sesión en http://localhost:3000/login**

### Crear Usuarios de Prueba

```bash
# Usando la API directamente
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "docente1",
    "email": "docente1@pontificia.edu",
    "password": "docente123",
    "full_name": "Juan Pérez",
    "role": "Docente"
  }'
```

## 📝 Casos de Uso Comunes

### 1. Registrar Horas Docentes

```
1. Iniciar sesión como Docente
2. Navegar a "Horas Docentes"
3. Click en "Registrar Horas"
4. Llenar formulario:
   - Materia: Matemáticas
   - Curso: 1° Año A
   - Horas: 4
   - Fecha: Seleccionar fecha
5. Click en "Registrar"
```

### 2. Aprobar Horas (RRHH/Admin)

```
1. Iniciar sesión como RRHH o Administración
2. Navegar a "Horas Docentes"
3. Buscar horas pendientes (estado "Pendiente")
4. Click en "Aprobar"
5. Confirmación de aprobación
```

### 3. Crear y Firmar Documento

```
1. Navegar a "Documentos"
2. Click en "Nuevo Documento"
3. Llenar formulario:
   - Título: Contrato de Trabajo
   - Tipo: Contrato
   - Descripción: Contrato docente 2024
4. Click en "Crear Documento"
5. Click en "Firmar" en el documento creado
6. Ingresar firma digital
```

### 4. Exportar Datos (RRHH/Contabilidad/Admin)

```
1. Navegar a "Reportes"
2. Click en "Exportar Documentos" o "Exportar Horas Docentes"
3. El archivo Excel se descargará automáticamente
```

## 🔧 Solución de Problemas

### Error: No se puede conectar a la base de datos

```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart db backend

# Ver logs para más información
docker-compose logs db
docker-compose logs backend
```

### Error: Puerto ya en uso

```bash
# Cambiar puertos en docker-compose.yml
# Ejemplo: cambiar 3000:3000 por 3001:3000
```

### Error: Frontend no puede conectar con Backend

```bash
# Verificar que VITE_API_URL está correcto
# En frontend/.env debería ser:
VITE_API_URL=http://localhost:8000

# Reiniciar frontend
cd frontend
npm run dev
```

## 🧪 Testing de API

### Usando Swagger UI

```
1. Navegar a http://localhost:8000/docs
2. Probar endpoints interactivamente
3. Usar el botón "Authorize" para autenticación JWT
```

### Usando curl

```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# Obtener información del usuario actual
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# Listar documentos
curl -X GET "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Datos de Prueba

Para poblar la base de datos con datos de prueba, crear usuarios adicionales:

- **Docente**: usuario: `docente1`, password: `docente123`
- **RRHH**: usuario: `rrhh1`, password: `rrhh123`
- **Contabilidad**: usuario: `conta1`, password: `conta123`
- **Admin**: usuario: `admin`, password: `admin123`

## 🔐 Seguridad

**IMPORTANTE**: Los valores por defecto son solo para desarrollo. 

Para producción:
1. Cambiar SECRET_KEY en backend/.env
2. Usar contraseñas seguras
3. Configurar HTTPS
4. Cambiar credenciales de base de datos

Ver `DEPLOYMENT.md` para más detalles.

## 📚 Documentación Adicional

- **README.md**: Documentación completa del proyecto
- **DEPLOYMENT.md**: Guía de despliegue en producción
- **API Docs**: http://localhost:8000/docs

## 🆘 Soporte

Para problemas o preguntas:
1. Revisar los logs: `docker-compose logs`
2. Consultar la documentación de la API
3. Contactar al equipo de TI de la institución
