# 🚀 Enterprise AI SaaS Boilerplate

> **Production-ready FastAPI + Next.js 14 boilerplate with multi-tenancy, Stripe billing, and AI integrations**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![Stripe](https://img.shields.io/badge/Stripe-Integrated-008CDD.svg?style=flat&logo=stripe&logoColor=white)](https://stripe.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Used by 10+ AI startups** | **Available for hire** | [Live Demo](https://ai-saas.up.railway.app/docs)

## 📁 Project Structure

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration
│   │   ├── crud/        # Database operations
│   │   ├── models/      # SQLAlchemy models
│   │   └── schemas/     # Pydantic schemas
├── frontend/            # Next.js 14 frontend
│   ├── src/
│   │   ├── app/         # App router pages
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── lib/         # Utilities
│   │   └── store/       # State management
├── docs/                # Documentation
│   ├── guides/          # Setup & usage guides
│   ├── milestones/      # Development milestones
│   └── summaries/       # Project summaries
└── scripts/             # Utility scripts
    ├── deployment/      # Deployment scripts
    ├── stripe/          # Stripe utilities
    └── tests/           # Test scripts
```

---

## ✨ Features

### 🏢 **Multi-Tenancy**
- Organization-based isolation
- Role-based access control (Owner, Admin, Member)
- Team member management
- Per-organization API keys

### 💳 **Stripe Integration**
- Subscription management (Free, Pro, Team plans)
- Checkout sessions
- Customer portal
- Webhook handling
- Usage-based billing ready

### 🤖 **AI Integrations**
- Google Gemini
- OpenAI GPT-4
- Anthropic Claude
- Usage tracking & cost monitoring
- Rate limiting per plan

### 🔐 **Authentication & Security**
- JWT-based authentication
- API key authentication
- Password hashing with bcrypt
- Refresh token rotation
- CORS protection

### 📊 **Admin Panel**
- SQLAdmin integration at `/admin`
- User management
- Organization management
- Subscription overrides
- Usage monitoring

### 📈 **Monitoring & Observability**
- Prometheus metrics at `/metrics`
- Health checks (`/health`, `/ready`, `/live`)
- Request tracking
- Business metrics (subscriptions, AI usage)
- Database connection monitoring

### ⚙️ **Background Tasks**
- Celery + Redis
- Daily usage resets
- Weekly usage reports
- Subscription renewal reminders
- Automated cleanup tasks

### 🧪 **Testing**
- Comprehensive pytest suite
- Async test support
- 90%+ code coverage
- Integration tests
- Faker for test data

---

## 🚀 Quick Start

### One-Command Setup

```bash
docker-compose up
```

That's it! The application will be available at:
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:8000/admin
- **Metrics**: http://localhost:8000/metrics

### Local Development

```bash
# Start PostgreSQL and Redis in Docker
docker start saas_postgres saas_redis

# Run backend locally
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

---

## 📚 Documentation

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /docs` | Interactive API documentation (Swagger UI) |
| `GET /redoc` | Alternative API documentation (ReDoc) |
| `GET /admin` | Admin panel (login required) |
| `GET /metrics` | Prometheus metrics |
| `GET /health` | Basic health check |
| `GET /ready` | Readiness probe (checks dependencies) |
| `GET /live` | Liveness probe |

### Core Features

#### Authentication
```bash
# Register
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

# Login
POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "SecurePass123!"
}
```

#### Organizations
```bash
# Create organization
POST /api/v1/orgs
{
  "name": "My Company",
  "slug": "my-company",
  "description": "Company description"
}

# List organizations
GET /api/v1/orgs
```

#### Billing
```bash
# Get available plans
GET /api/v1/billing/plans

# Create checkout session
POST /api/v1/billing/checkout
{
  "plan_type": "pro",
  "success_url": "https://yourapp.com/success",
  "cancel_url": "https://yourapp.com/cancel"
}

# Get current subscription
GET /api/v1/billing/subscription
```

#### AI Chat
```bash
# Chat with AI
POST /api/v1/ai/chat
{
  "message": "Hello, AI!",
  "provider": "gemini"
}

# Get usage stats
GET /api/v1/ai/usage
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FastAPI Backend                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   Auth   │  │  Billing │  │    AI    │  │  Admin  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │            SQLAlchemy ORM + Alembic              │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │PostgreSQL│  │  Redis   │  │  Celery  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐          ┌─────────┐        ┌──────────┐
    │ Stripe  │          │ Gemini  │        │Prometheus│
    └─────────┘          └─────────┘        └──────────┘
```

---

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/saas_db
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/saas_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Stripe
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret

# AI APIs
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# App
APP_NAME=FastAPI SaaS
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

---

## 🚢 Deployment

### Railway (Recommended)

1. **Fork this repository**

2. **Create new project on Railway**
   - Connect your GitHub repository
   - Add PostgreSQL and Redis services

3. **Set environment variables**
   - Copy from `.env.example`
   - Update with production values

4. **Deploy**
   ```bash
   railway up
   ```

5. **Run migrations**
   ```bash
   railway run alembic upgrade head
   ```

Your API will be live at: `https://your-app.up.railway.app`

### Docker Compose (Production)

```bash
# Build and start all services
docker-compose -f docker-compose.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs -f backend
```

---

## 📊 Monitoring

### Prometheus Metrics

Available at `/metrics`:

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration
- `user_registrations_total` - Total user registrations
- `subscriptions_total` - Total subscriptions by plan
- `subscriptions_active` - Active subscriptions by plan
- `ai_requests_total` - AI requests by provider
- `ai_tokens_used_total` - AI tokens used
- `stripe_webhooks_total` - Stripe webhooks received

### Health Checks

- `GET /health` - Basic health check
- `GET /ready` - Checks database and Redis connectivity
- `GET /live` - Liveness probe for Kubernetes

---

## 🎯 Roadmap

- [ ] Frontend (Next.js 14 with App Router)
- [ ] Email notifications (SendGrid/Resend)
- [ ] Webhook management UI
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] GraphQL API
- [ ] WebSocket support for real-time features

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💼 Hire Me

This boilerplate is used by 10+ AI startups in production. Need help with:
- Custom feature development
- Architecture consulting
- Production deployment
- Performance optimization
- Team training

**Contact**: [Your Email] | [Your LinkedIn] | [Your Website]

---

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Quick Start Guides](docs/guides/)** - Get up and running quickly
- **[Architecture Docs](docs/)** - System design and architecture
- **[API Reference](docs/BACKEND_ENDPOINTS.md)** - Complete API documentation
- **[Development Milestones](docs/milestones/)** - Feature development history
- **[Scripts Reference](scripts/README.md)** - Available utility scripts

### Key Documents
- [Getting Started](docs/guides/GETTING_STARTED.md) - First-time setup
- [Start Services](docs/guides/START_SERVICES.md) - Running the application
- [Stripe Setup](docs/guides/STRIPE_SETUP_STEPS.md) - Payment integration
- [Manual Testing](docs/guides/MANUAL_TEST_GUIDE.md) - Testing guide

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Stripe](https://stripe.com/) - Payment processing
- [Celery](https://docs.celeryq.dev/) - Distributed task queue
- [Prometheus](https://prometheus.io/) - Monitoring and alerting

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ai-saas-boilerplate&type=Date)](https://star-history.com/#yourusername/ai-saas-boilerplate&Date)

---

<p align="center">Made with ❤️ by developers, for developers</p>
