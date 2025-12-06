# 📋 Project Overview - FastAPI AI SaaS Boilerplate

## 🎯 What Is This?

A production-ready FastAPI backend boilerplate for building AI SaaS applications. Includes authentication, billing, database management, and Docker deployment out of the box.

## ✨ Features

### Authentication & Security
- JWT-based authentication with access and refresh tokens
- Password hashing with bcrypt
- Protected routes with dependency injection
- Token expiration and refresh mechanism
- User registration and login endpoints

### Billing & Payments
- Stripe integration
- Automatic customer creation on signup
- Checkout session creation
- Customer portal access
- Webhook support ready

### Database
- PostgreSQL with async SQLAlchemy
- Alembic migrations
- User model with Stripe customer ID
- Async database sessions
- Connection pooling

### API & Documentation
- FastAPI with automatic OpenAPI docs
- Swagger UI at /docs
- ReDoc at /redoc
- CORS middleware configured
- Pydantic schemas for validation

### DevOps
- Docker and Docker Compose
- Multi-stage Dockerfile
- Health check endpoints
- Environment-based configuration
- Redis for caching/sessions

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database connection and session
│   ├── dependencies.py            # Dependency injection (auth)
│   │
│   ├── core/
│   │   ├── config.py              # Settings and configuration
│   │   └── security.py            # JWT and password utilities
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py            # Authentication endpoints
│   │       ├── users.py           # User management endpoints
│   │       └── billing.py         # Stripe billing endpoints
│   │
│   ├── models/
│   │   └── user.py                # SQLAlchemy User model
│   │
│   ├── schemas/
│   │   ├── user.py                # Pydantic User schemas
│   │   └── token.py               # Pydantic Token schemas
│   │
│   └── crud/
│       └── user.py                # User CRUD operations
│
├── alembic/
│   ├── versions/                  # Migration files
│   ├── env.py                     # Alembic environment
│   └── script.py.mako             # Migration template
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker image definition
├── alembic.ini                    # Alembic configuration
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # Backend documentation
├── setup.sh                       # Setup script
└── test_api.sh                    # API testing script
```

## 🔌 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login and get tokens | No |
| POST | `/refresh` | Refresh access token | No |

### Users (`/api/v1/users`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/me` | Get current user info | Yes |

### Billing (`/api/v1/billing`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/create-checkout-session` | Create Stripe checkout | Yes |
| GET | `/customer-portal` | Get customer portal URL | Yes |

### System

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root endpoint | No |
| GET | `/health` | Health check | No |

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    stripe_customer_id VARCHAR UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🔐 Authentication Flow

### Registration
1. User submits email, password, full_name
2. System creates Stripe customer
3. System creates user with hashed password
4. Returns user object

### Login
1. User submits email and password
2. System verifies credentials
3. System generates access token (30 min) and refresh token (7 days)
4. Returns both tokens

### Protected Routes
1. Client sends access token in Authorization header
2. System validates token
3. System loads user from database
4. Endpoint receives authenticated user

### Token Refresh
1. Client sends refresh token
2. System validates refresh token
3. System generates new access and refresh tokens
4. Returns new tokens

## 🛠️ Technology Stack

### Core
- **FastAPI** 0.104.1 - Modern Python web framework
- **Python** 3.11+ - Programming language
- **Uvicorn** - ASGI server

### Database
- **PostgreSQL** 15 - Primary database
- **SQLAlchemy** 2.0 - Async ORM
- **Asyncpg** - Async PostgreSQL driver
- **Alembic** - Database migrations

### Authentication
- **python-jose** - JWT implementation
- **passlib** - Password hashing
- **bcrypt** - Hashing algorithm

### Payments
- **Stripe** 7.8.0 - Payment processing

### Caching
- **Redis** 7 - In-memory data store
- **Celery** 5.3 - Task queue (ready to use)

### Validation
- **Pydantic** 2.5 - Data validation
- **pydantic-settings** - Settings management

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
DATABASE_URL_SYNC=postgresql://user:pass@host:port/db

# Redis
REDIS_URL=redis://host:port/db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# App
APP_NAME=FastAPI SaaS
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🚀 Deployment Options

### Docker (Recommended)
```bash
docker-compose up -d
```

### Manual
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Cloud Platforms
- **AWS**: ECS/Fargate + RDS + ElastiCache
- **Google Cloud**: Cloud Run + Cloud SQL + Memorystore
- **Azure**: Container Apps + PostgreSQL + Redis Cache
- **Heroku**: Web dyno + Heroku Postgres + Heroku Redis
- **Railway**: Deploy from GitHub
- **Render**: Deploy from GitHub

## 📊 Performance Considerations

### Database
- Async operations for non-blocking I/O
- Connection pooling via SQLAlchemy
- Indexes on email and stripe_customer_id
- Prepared statements via ORM

### Caching
- Redis for session storage
- Redis for rate limiting (implement as needed)
- Redis for Celery task queue

### Security
- Password hashing with bcrypt (slow by design)
- JWT tokens with expiration
- CORS middleware for cross-origin requests
- Environment-based secrets

## 🧪 Testing

### Manual Testing
```bash
# Run test script
cd backend
./test_api.sh
```

### Unit Tests (Add as needed)
```bash
pytest tests/
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## 📈 Scaling Strategies

### Horizontal Scaling
- Run multiple backend containers
- Use load balancer (nginx, AWS ALB)
- Stateless design allows easy scaling

### Database Scaling
- Read replicas for read-heavy workloads
- Connection pooling
- Query optimization
- Caching frequently accessed data

### Caching
- Redis for session data
- Redis for API response caching
- CDN for static assets

### Background Jobs
- Celery for async tasks
- Separate worker containers
- Redis as message broker

## 🔒 Security Best Practices

- [ ] Use strong SECRET_KEY (32+ random bytes)
- [ ] Enable HTTPS in production
- [ ] Set DEBUG=False in production
- [ ] Configure proper CORS origins
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Enable SQL injection protection (ORM handles this)
- [ ] Add CSRF protection for forms
- [ ] Implement proper error handling
- [ ] Add logging and monitoring
- [ ] Regular dependency updates
- [ ] Database backups
- [ ] Implement API versioning

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Stripe API Documentation](https://stripe.com/docs/api)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - Use freely for personal or commercial projects.

## 🆘 Support

- **Documentation**: Check SETUP.md and QUICKSTART.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open a GitHub issue
- **Discussions**: GitHub Discussions

---

**Built with ❤️ for developers who want to ship fast.**
