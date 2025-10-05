#!/bin/bash

# Script to initialize the database with sample data

echo "🚀 Initializing Sistema Pontificia ELP Database..."
echo ""

# Check if Docker is running
if ! docker-compose ps | grep -q "pontificia_backend"; then
    echo "⚠️  Backend container is not running. Starting services..."
    docker-compose up -d
    echo "⏳ Waiting for services to start (30 seconds)..."
    sleep 30
fi

# Run initialization script
echo "📊 Populating database with sample data..."
docker-compose exec backend python init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database initialized successfully!"
    echo ""
    echo "🌐 Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "👤 Sample credentials:"
    echo "   Admin:        admin / admin123"
    echo "   Docente 1:    docente1 / docente123"
    echo "   Docente 2:    docente2 / docente123"
    echo "   RRHH:         rrhh1 / rrhh123"
    echo "   Contabilidad: conta1 / conta123"
    echo "   TI:           ti1 / ti123"
else
    echo ""
    echo "❌ Error initializing database. Check the logs:"
    echo "   docker-compose logs backend"
    exit 1
fi
