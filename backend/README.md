# FastAPI SaaS Boilerplate

Production-ready FastAPI backend for AI SaaS applications with authentication, billing, and database management.

## Features

- ✅ JWT Authentication with refresh tokens
- ✅ User registration and login
- ✅ Stripe integration (customer creation on signup)
- ✅ PostgreSQL with async SQLAlchemy
- ✅ Redis for caching/sessions
- ✅ Alembic migrations
- ✅ Docker & Docker Compose
- ✅ Beautiful API docs (Swagger & ReDoc)
- ✅ Password hashing with bcrypt
- ✅ CORS middleware
- ✅ Environment-based configuration

## Quick Start

### 1. Setup Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker (Recommended)

```bash
# From project root
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### 3. Run Locally (Alternative)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (returns access + refresh tokens)
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user info

### Billing
- `POST /api/v1/billing/create-checkout-session` - Create Stripe checkout
- `GET /api/v1/billing/customer-portal` - Access Stripe customer portal

## Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Database connection
│   ├── dependencies.py      # Dependency injection
│   ├── core/
│   │   ├── config.py        # Settings
│   │   └── security.py      # JWT & password hashing
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py      # Auth endpoints
│   │       ├── users.py     # User endpoints
│   │       └── billing.py   # Stripe endpoints
│   ├── models/
│   │   └── user.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── user.py          # Pydantic schemas
│   │   └── token.py         # Token schemas
│   └── crud/
│       └── user.py          # Database operations
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Environment Variables

See `.env.example` for all required variables:
- Database connection
- Redis URL
- JWT secret key
- Stripe API keys
- CORS origins

## Tech Stack

- FastAPI - Modern Python web framework
- SQLAlchemy - Async ORM
- PostgreSQL - Database
- Redis - Caching
- Alembic - Migrations
- Stripe - Payment processing
- JWT - Authentication
- Docker - Containerization
