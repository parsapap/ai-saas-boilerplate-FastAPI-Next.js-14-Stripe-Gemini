#!/bin/bash

echo "🚀 Starting services manually with docker..."
echo ""

# Create network
docker network create saas_network 2>/dev/null || true

# Start PostgreSQL
echo "📦 Starting PostgreSQL..."
docker run -d \
  --name saas_postgres \
  --network saas_network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=saas_db \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
echo "📦 Starting Redis..."
docker run -d \
  --name saas_redis \
  --network saas_network \
  -p 6379:6379 \
  redis:7-alpine

# Wait for services
echo "⏳ Waiting for services..."
sleep 10

# Build backend
echo "🏗️  Building backend..."
docker build -t saas_backend ./backend

# Start backend
echo "📦 Starting backend..."
docker run -d \
  --name saas_backend \
  --network saas_network \
  -p 8000:8000 \
  -v $(pwd)/backend:/app \
  -e DATABASE_URL=postgresql+asyncpg://postgres:postgres@saas_postgres:5432/saas_db \
  -e DATABASE_URL_SYNC=postgresql://postgres:postgres@saas_postgres:5432/saas_db \
  -e REDIS_URL=redis://saas_redis:6379/0 \
  -e SECRET_KEY=dev-secret-key-change-in-production-min-32-chars-long \
  -e STRIPE_SECRET_KEY=sk_test_dummy \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_dummy \
  -e STRIPE_WEBHOOK_SECRET=whsec_dummy \
  -e GEMINI_API_KEY=dummy_key \
  -e APP_NAME="FastAPI SaaS" \
  -e APP_VERSION=1.0.0 \
  -e DEBUG=True \
  -e ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000 \
  saas_backend \
  sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo ""
echo "✅ Services started!"
echo ""
echo "📍 Access:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""
echo "📝 View logs:"
echo "   docker logs -f saas_backend"
echo ""
echo "🛑 Stop:"
echo "   docker stop saas_backend saas_postgres saas_redis"
echo "   docker rm saas_backend saas_postgres saas_redis"
echo ""
