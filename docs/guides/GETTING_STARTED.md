# 🎯 Getting Started - FastAPI AI SaaS Backend

Welcome! This guide will get you from zero to a running API in under 5 minutes.

## 📋 What You're Getting

A production-ready FastAPI backend with:
- ✅ User authentication (JWT)
- ✅ Stripe billing integration
- ✅ PostgreSQL database
- ✅ Redis caching
- ✅ Docker deployment
- ✅ API documentation
- ✅ Database migrations

## ⚡ Quick Start (5 Minutes)

### Step 1: Setup Environment (1 min)

```bash
# Copy environment file
cp backend/.env.example backend/.env

# Generate a secret key
openssl rand -hex 32

# Edit backend/.env and paste the secret key
# Update SECRET_KEY=<paste-your-key-here>
```

### Step 2: Start Services (2 min)

```bash
# Make start script executable
chmod +x start.sh

# Start everything
./start.sh
```

Wait for Docker to download images and start services...

### Step 3: Verify (1 min)

```bash
# Check health
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### Step 4: Explore (1 min)

Open your browser:
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Test Your API

### Option 1: Use the Test Script

```bash
cd backend
./test_api.sh
```

### Option 2: Manual Testing

#### Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "SecurePass123!",
    "full_name": "Demo User"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=SecurePass123!"
```

You'll get a response like:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get User Profile
```bash
# Replace YOUR_TOKEN with the access_token from login
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📚 Available Documentation

We've created comprehensive documentation for you:

1. **QUICKSTART.md** - Fast setup guide (you are here!)
2. **SETUP.md** - Detailed setup instructions
3. **PROJECT_OVERVIEW.md** - Complete project documentation
4. **ARCHITECTURE.md** - System architecture and design
5. **CHECKLIST.md** - Step-by-step setup checklist
6. **README.md** - Main project README

## 🎨 What's Included

### API Endpoints

#### Authentication (`/api/v1/auth`)
- `POST /register` - Create new user account
- `POST /login` - Login and get tokens
- `POST /refresh` - Refresh access token

#### Users (`/api/v1/users`)
- `GET /me` - Get current user profile

#### Billing (`/api/v1/billing`)
- `POST /create-checkout-session` - Create Stripe checkout
- `GET /customer-portal` - Access Stripe portal

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB connection
│   ├── dependencies.py      # Auth dependencies
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── security.py      # JWT & passwords
│   ├── api/v1/
│   │   ├── auth.py          # Auth endpoints
│   │   ├── users.py         # User endpoints
│   │   └── billing.py       # Billing endpoints
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

## 🔧 Common Tasks

### View Logs
```bash
docker-compose logs -f backend
```

### Stop Services
```bash
docker-compose down
```

### Restart Backend
```bash
docker-compose restart backend
```

### Access Database
```bash
docker-compose exec db psql -U postgres -d saas_db
```

### Run Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Create New Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## 🚀 Next Steps

### 1. Add Stripe Integration (Optional)

If you want to use billing features:

1. Create account at https://stripe.com
2. Get API keys from https://dashboard.stripe.com/apikeys
3. Add to `backend/.env`:
   ```env
   STRIPE_SECRET_KEY=sk_test_your_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key
   ```
4. Restart backend: `docker-compose restart backend`

### 2. Customize the User Model

Edit `backend/app/models/user.py` to add fields:

```python
class User(Base):
    __tablename__ = "users"
    
    # Existing fields...
    
    # Add your custom fields
    phone_number = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    subscription_tier = Column(String, default="free")
```

Then create and run migration:
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add custom fields"
docker-compose exec backend alembic upgrade head
```

### 3. Add New Endpoints

Create a new file `backend/app/api/v1/your_feature.py`:

```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/your-endpoint")
async def your_endpoint(current_user: User = Depends(get_current_active_user)):
    return {"message": "Hello from your endpoint!"}
```

Register it in `backend/app/main.py`:

```python
from app.api.v1 import your_feature

app.include_router(
    your_feature.router,
    prefix="/api/v1/your-feature",
    tags=["Your Feature"]
)
```

### 4. Add Background Tasks

Celery is already configured! Create tasks in `backend/app/tasks.py`:

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery("tasks", broker=settings.REDIS_URL)

@celery_app.task
def send_welcome_email(user_email: str):
    # Your email sending logic
    pass
```

### 5. Deploy to Production

See SETUP.md for production deployment instructions.

## 🆘 Troubleshooting

### Port 8000 Already in Use
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Redis Connection Error
```bash
# Restart Redis
docker-compose restart redis

# Test connection
docker-compose exec redis redis-cli ping
```

### Reset Everything
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

## 📖 Learning Resources

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### SQLAlchemy
- Official Docs: https://docs.sqlalchemy.org/
- Async Tutorial: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

### Stripe
- API Docs: https://stripe.com/docs/api
- Python Library: https://stripe.com/docs/api/python

### Docker
- Get Started: https://docs.docker.com/get-started/
- Compose: https://docs.docker.com/compose/

## 💡 Tips

1. **Use the Swagger UI** at http://localhost:8000/docs to test endpoints interactively
2. **Check logs frequently** with `docker-compose logs -f backend`
3. **Use migrations** for all database changes
4. **Test locally** before deploying to production
5. **Keep secrets secure** - never commit `.env` files

## 🎉 You're Ready!

You now have a fully functional FastAPI backend. Here's what to do next:

1. ✅ Test all endpoints in Swagger UI
2. ✅ Customize the User model for your needs
3. ✅ Add your business logic
4. ✅ Set up Stripe if needed
5. ✅ Deploy to production

## 🤝 Need Help?

- **Documentation**: Check the other .md files in this project
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open a GitHub issue
- **FastAPI Community**: https://github.com/tiangolo/fastapi/discussions

---

**Happy coding! 🚀**
