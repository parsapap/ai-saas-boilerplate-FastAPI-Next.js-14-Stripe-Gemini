#!/bin/bash
set -e

echo "🚀 Starting FastAPI SaaS Backend..."

# Wait for postgres
echo "⏳ Waiting for PostgreSQL..."
while ! pg_isready -h postgres -U postgres > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL is ready!"

# Wait for redis
echo "⏳ Waiting for Redis..."
while ! redis-cli -h redis ping > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Redis is ready!"

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head
echo "✅ Migrations completed!"

# Start application
echo "🎉 Starting FastAPI application..."
exec "$@"
