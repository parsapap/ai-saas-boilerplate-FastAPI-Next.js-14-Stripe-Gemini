#!/bin/bash

echo "🚀 Starting FastAPI AI SaaS Platform..."
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo ""
    echo "📝 Note: Using dummy API keys for development"
    echo "   Update backend/.env with real keys for production"
    echo ""
fi

# Stop any existing containers
echo "🧹 Cleaning up old containers..."
docker-compose down

# Build and start
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Access your application:"
echo "   - API: http://localhost:8000"
echo "   - API Docs (Swagger): http://localhost:8000/docs"
echo "   - API Docs (ReDoc): http://localhost:8000/redoc"
echo "   - Flower (Celery Monitor): http://localhost:5555"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f backend"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
