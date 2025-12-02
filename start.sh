#!/bin/bash

echo "🚀 Starting FastAPI AI SaaS Boilerplate..."
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo ""
    echo "⚠️  IMPORTANT: Update backend/.env with your configuration!"
    echo "   - SECRET_KEY (generate a secure random string)"
    echo "   - STRIPE_SECRET_KEY (from Stripe dashboard)"
    echo "   - STRIPE_PUBLISHABLE_KEY (from Stripe dashboard)"
    echo ""
    read -p "Press Enter to continue after updating .env..."
fi

# Start Docker Compose
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "✨ All services are running!"
echo ""
echo "📍 Access your application:"
echo "   - API: http://localhost:8000"
echo "   - API Docs (Swagger): http://localhost:8000/docs"
echo "   - API Docs (ReDoc): http://localhost:8000/redoc"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f backend"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
