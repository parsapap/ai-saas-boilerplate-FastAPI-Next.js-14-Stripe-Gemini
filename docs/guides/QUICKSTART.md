# ⚡ Quick Start Guide

Get your FastAPI AI SaaS backend running in 5 minutes.

## 🚀 Fastest Way (Docker)

```bash
# 1. Copy environment file
cp backend/.env.example backend/.env

# 2. Update SECRET_KEY in backend/.env (required)
# Generate one: openssl rand -hex 32

# 3. Start everything
./start.sh

# 4. Test it
curl http://localhost:8000/health
```

**Done!** API is running at http://localhost:8000

## 📖 API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## 🧪 Test the API

```bash
# Run automated tests
cd backend
./test_api.sh
```

Or test manually:

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"pass123","full_name":"Test"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@test.com&password=pass123"
```

## 📁 What You Got

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── database.py          # DB connection
│   ├── dependencies.py      # Auth dependencies
│   ├── core/
│   │   ├── config.py        # Settings
│   │   └── security.py      # JWT & passwords
│   ├── api/v1/
│   │   ├── auth.py          # /register, /login, /refresh
│   │   ├── users.py         # /me
│   │   └── billing.py       # Stripe integration
│   ├── models/
│   │   └── user.py          # User model
│   ├── schemas/
│   │   ├── user.py          # User schemas
│   │   └── token.py         # Token schemas
│   └── crud/
│       └── user.py          # User operations
├── alembic/                 # Migrations
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 🔑 Key Features

✅ **JWT Authentication** - Access + refresh tokens  
✅ **User Management** - Register, login, profile  
✅ **Stripe Integration** - Customer creation on signup  
✅ **PostgreSQL** - Async database with SQLAlchemy  
✅ **Redis** - Caching ready  
✅ **Alembic** - Database migrations  
✅ **Docker** - Full containerization  
✅ **API Docs** - Swagger + ReDoc  

## 🛠️ Common Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Restart
docker-compose restart backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Access database
docker-compose exec db psql -U postgres -d saas_db

# Access Redis
docker-compose exec redis redis-cli
```

## 🔧 Configuration

Edit `backend/.env`:

```env
# Required
SECRET_KEY=your-secret-key              # Generate: openssl rand -hex 32

# Optional (for Stripe features)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Database (auto-configured with Docker)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/saas_db

# Redis (auto-configured with Docker)
REDIS_URL=redis://redis:6379/0
```

## 📚 Next Steps

1. **Customize User Model** - Add fields in `backend/app/models/user.py`
2. **Add Endpoints** - Create new routes in `backend/app/api/v1/`
3. **Setup Stripe** - Get keys from https://dashboard.stripe.com/apikeys
4. **Add Business Logic** - Implement in `backend/app/crud/`
5. **Deploy** - See SETUP.md for production deployment

## 🆘 Troubleshooting

**Port 8000 already in use?**
```bash
lsof -i :8000
kill -9 <PID>
```

**Database connection error?**
```bash
docker-compose restart db
docker-compose logs db
```

**Need to reset everything?**
```bash
docker-compose down -v
docker-compose up -d
```

## 📖 Full Documentation

- **Setup Guide**: See SETUP.md
- **API Docs**: http://localhost:8000/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Questions?** Check the docs or open an issue.
