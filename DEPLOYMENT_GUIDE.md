# 🚀 Deployment Guide - FastAPI AI SaaS

## Quick Start (Development)

### Option 1: Using start script (Recommended)

```bash
./start.sh
```

### Option 2: Manual

```bash
# 1. Create .env file
cp backend/.env.example backend/.env

# 2. Start services
docker-compose up --build
```

---

## 📋 Prerequisites

- Docker & Docker Compose installed
- Ports available: 8000 (API), 5432 (PostgreSQL), 6379 (Redis), 5555 (Flower)

---

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```env
# Required for production
SECRET_KEY=<generate-with-openssl-rand-hex-32>
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
GEMINI_API_KEY=<your-real-key>

# Optional
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
```

### Generate SECRET_KEY

```bash
openssl rand -hex 32
```

---

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| **backend** | 8000 | FastAPI application |
| **postgres** | 5432 | PostgreSQL database |
| **redis** | 6379 | Redis cache & broker |
| **celery_worker** | - | Background task worker |
| **celery_beat** | - | Periodic task scheduler |
| **flower** | 5555 | Celery monitoring UI |

---

## 🧪 Testing

### 1. Check Health

```bash
curl http://localhost:8000/health
```

### 2. Access API Docs

```
http://localhost:8000/docs
```

### 3. Test Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

### 4. Run Test Scripts

```bash
# Multi-tenant
cd backend && ./test_multi_tenant.sh

# Stripe
cd backend && ./test_stripe.sh

# AI
cd backend && ./test_ai.sh
```

---

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f postgres
```

### Celery Monitoring (Flower)

```
http://localhost:5555
```

### Database Access

```bash
docker-compose exec postgres psql -U postgres -d saas_db
```

### Redis CLI

```bash
docker-compose exec redis redis-cli
```

---

## 🔄 Common Commands

### Restart Services

```bash
docker-compose restart backend
docker-compose restart celery_worker
```

### Rebuild

```bash
docker-compose up --build -d
```

### Stop All

```bash
docker-compose down
```

### Clean Everything

```bash
docker-compose down -v  # ⚠️ Deletes all data!
```

### Run Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### Create Migration

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database not ready → wait longer
# 2. Migration failed → check alembic/versions/
# 3. Import error → check Python syntax
```

### Database connection error

```bash
# Check postgres is running
docker-compose ps postgres

# Check connection
docker-compose exec backend python -c "from app.database import engine; print('OK')"
```

### Celery not processing tasks

```bash
# Check worker logs
docker-compose logs celery_worker

# Check Redis connection
docker-compose exec redis redis-cli ping
```

### Port already in use

```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

---

## 🚀 Production Deployment

### 1. Update Environment

```env
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=<production-db-url>
STRIPE_SECRET_KEY=sk_live_...
```

### 2. Use Production Database

```yaml
# docker-compose.prod.yml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: <strong-password>
    volumes:
      - /var/lib/postgresql/data:/var/lib/postgresql/data
```

### 3. Enable HTTPS

Use nginx or Traefik as reverse proxy

### 4. Set up Monitoring

- Sentry for error tracking
- Prometheus + Grafana for metrics
- ELK stack for logs

### 5. Backup Strategy

```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres saas_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres saas_db < backup.sql
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`

### Organizations
- `POST /api/v1/orgs`
- `GET /api/v1/orgs`
- `POST /api/v1/orgs/{id}/invite`

### Billing
- `GET /api/v1/billing/plans`
- `POST /api/v1/billing/checkout`
- `POST /api/v1/billing/webhook/stripe`

### AI
- `POST /api/v1/ai/chat`
- `POST /api/v1/ai/chat/stream`
- `GET /api/v1/ai/usage`

Full documentation: http://localhost:8000/docs

---

## 🆘 Support

- Check logs: `docker-compose logs -f`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

**Built with ❤️ using FastAPI, PostgreSQL, Redis, Celery, Stripe, and Gemini AI**
