# Setup Guide - FastAPI AI SaaS Boilerplate

## Prerequisites

- Docker & Docker Compose (recommended)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if not using Docker)
- Redis (if not using Docker)

## Quick Setup (Docker - Recommended)

### 1. Clone and Configure

```bash
# Navigate to project
cd ai-saas-boilerplate

# Copy environment file
cp backend/.env.example backend/.env
```

### 2. Update Environment Variables

Edit `backend/.env`:

```env
# Generate a secure SECRET_KEY (use: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-change-this-in-production

# Get from Stripe Dashboard (https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 3. Start Services

```bash
# Make start script executable
chmod +x start.sh

# Run the start script
./start.sh

# Or manually:
docker-compose up -d
```

### 4. Verify Installation

```bash
# Check services are running
docker-compose ps

# View backend logs
docker-compose logs -f backend

# Test API
curl http://localhost:8000/health
```

### 5. Access Your Application

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Local Development Setup (Without Docker)

### 1. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your settings

# Setup database (make sure PostgreSQL is running)
# Create database: createdb saas_db

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### 2. Setup PostgreSQL

```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database
createdb saas_db

# Create user (optional)
psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE saas_db TO postgres;"
```

### 3. Setup Redis

```bash
# Install Redis
# Ubuntu/Debian:
sudo apt-get install redis-server

# macOS:
brew install redis

# Start Redis
sudo service redis-server start  # Linux
brew services start redis  # macOS
```

## Testing the API

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePass123!"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 3. Get Current User

```bash
# Replace YOUR_ACCESS_TOKEN with the token from login
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Refresh Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh?refresh_token=YOUR_REFRESH_TOKEN"
```

## Database Migrations

### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Add new table"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

## Stripe Setup

### 1. Get API Keys

1. Go to https://dashboard.stripe.com/apikeys
2. Copy your **Secret key** (starts with `sk_test_`)
3. Copy your **Publishable key** (starts with `pk_test_`)

### 2. Setup Webhooks (Optional)

1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `http://your-domain.com/api/v1/billing/webhook`
3. Select events to listen to
4. Copy the **Signing secret** (starts with `whsec_`)

### 3. Test Stripe Integration

```bash
# Create checkout session (requires authentication)
curl -X POST "http://localhost:8000/api/v1/billing/create-checkout-session" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_1234567890",
    "success_url": "http://localhost:3000/success",
    "cancel_url": "http://localhost:3000/cancel"
  }'
```

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Redis Connection Error

```bash
# Check Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

### Migration Errors

```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d

# Or manually:
alembic downgrade base
alembic upgrade head
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

## Production Deployment

### Environment Variables

Update these for production:

```env
# Use strong random key
SECRET_KEY=<generate-with-openssl-rand-hex-32>

# Use production Stripe keys
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Disable debug mode
DEBUG=False

# Update CORS origins
ALLOWED_ORIGINS=https://yourdomain.com

# Use production database
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/dbname
```

### Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use production Stripe keys
- [ ] Set DEBUG=False
- [ ] Configure proper CORS origins
- [ ] Use HTTPS in production
- [ ] Set up proper database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Use environment-specific .env files
- [ ] Never commit .env files to git

## Next Steps

1. Customize the User model in `backend/app/models/user.py`
2. Add more API endpoints in `backend/app/api/v1/`
3. Implement business logic in `backend/app/crud/`
4. Add Celery tasks for background jobs
5. Set up email notifications
6. Add more Stripe features (subscriptions, invoices)
7. Implement rate limiting
8. Add comprehensive tests

## Support

- Check API docs: http://localhost:8000/docs
- View logs: `docker-compose logs -f`
- Report issues: GitHub Issues
- Read FastAPI docs: https://fastapi.tiangolo.com/
