# Sistema Pontificia ELP - Guía de Despliegue

## Configuración de Producción

### 1. Base de Datos PostgreSQL

```bash
# Crear base de datos
createdb pontificia_db

# O usando Docker
docker run -d \
  --name pontificia_postgres \
  -e POSTGRES_DB=pontificia_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  postgres:15-alpine
```

### 2. Variables de Entorno de Producción

**Backend (.env)**
```
DATABASE_URL=postgresql://user:password@host:5432/pontificia_db
SECRET_KEY=your-super-secure-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env)**
```
VITE_API_URL=https://api.yoursdomain.com
```

### 3. HTTPS/SSL

Para producción, es obligatorio usar HTTPS. Opciones:

1. **Nginx como Proxy Reverso**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. **Let's Encrypt (Certbot)**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 4. Docker Compose para Producción

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  backend:
    build: ./backend
    restart: always
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
    networks:
      - app_network

  frontend:
    build: 
      context: ./frontend
      args:
        VITE_API_URL: ${API_URL}
    restart: always
    depends_on:
      - backend
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - frontend
      - backend
    networks:
      - app_network

volumes:
  postgres_data:

networks:
  app_network:
    driver: bridge
```

### 5. Seguridad Adicional

#### Firewall
```bash
# UFW en Ubuntu
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

#### Backup de Base de Datos
```bash
# Script de backup diario
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgresql"
mkdir -p $BACKUP_DIR

docker exec pontificia_postgres pg_dump -U postgres pontificia_db > \
  $BACKUP_DIR/backup_$DATE.sql

# Mantener solo los últimos 7 días
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

#### Variables de Entorno Seguras
```bash
# Generar SECRET_KEY seguro
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 6. Monitoreo

#### Logs
```bash
# Ver logs de contenedores
docker-compose logs -f backend
docker-compose logs -f frontend

# Configurar rotación de logs
# /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

#### Health Checks
```bash
# Verificar estado de la API
curl http://localhost:8000/health
```

### 7. Performance

#### Optimización del Frontend
```bash
cd frontend
npm run build

# Servir archivos estáticos con Nginx
```

#### Caché de Base de Datos
Configurar Redis para caché (opcional):
```yaml
redis:
  image: redis:alpine
  restart: always
  networks:
    - app_network
```

### 8. Actualización del Sistema

```bash
# 1. Hacer backup
./backup.sh

# 2. Obtener últimos cambios
git pull origin main

# 3. Reconstruir contenedores
docker-compose down
docker-compose build
docker-compose up -d

# 4. Verificar funcionamiento
docker-compose ps
```

## Checklist de Despliegue

- [ ] Configurar variables de entorno de producción
- [ ] Generar SECRET_KEY seguro
- [ ] Configurar base de datos PostgreSQL
- [ ] Configurar HTTPS/SSL
- [ ] Configurar firewall
- [ ] Configurar backups automáticos
- [ ] Configurar monitoreo de logs
- [ ] Configurar dominios DNS
- [ ] Probar todos los endpoints
- [ ] Verificar permisos de roles
- [ ] Documentar credenciales de acceso
