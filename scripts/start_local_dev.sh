#!/bin/bash

echo "🚀 Starting PostgreSQL and Redis in Docker..."
docker-compose -f docker-compose.local.yml up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

echo ""
echo "✅ Docker services started!"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "🔧 Starting backend on localhost:8000..."
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head

echo ""
echo "🎉 Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
