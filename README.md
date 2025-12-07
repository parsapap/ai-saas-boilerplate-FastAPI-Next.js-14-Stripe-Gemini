# 🚀 Enterprise AI SaaS Boilerplate

Production-ready **FastAPI + Next.js 14** boilerplate with multi-tenancy, Stripe billing, and AI integrations.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Stripe](https://img.shields.io/badge/Stripe-Integrated-008CDD.svg?style=flat&logo=stripe&logoColor=white)](https://stripe.com)

## 📸 Screenshots

| Dashboard | AI Chat |
|-----------|---------|
| ![Dashboard](screenshots/dashboard.png) | ![Chat](screenshots/chat.png) |

| Billing | Admin Panel |
|---------|-------------|
| ![Billing](screenshots/billing.png) | ![Admin](screenshots/admin.png) |

| Login | API Docs |
|-------|----------|
| ![Login](screenshots/login.png) | ![API Docs](screenshots/api-docs.png) |

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multi-Tenancy** | Organization-based isolation with RBAC (Owner, Admin, Member) |
| **Stripe Billing** | Subscriptions (Free/Pro/Team), checkout, customer portal, webhooks |
| **AI Integration** | Gemini, GPT-4, Claude via OpenRouter with usage tracking |
| **Auth** | JWT + API key authentication, refresh tokens, bcrypt |
| **Admin Panel** | SQLAdmin at `/admin` for user/org/subscription management |
| **Monitoring** | Prometheus metrics, health checks |
| **Background Tasks** | Celery + Redis for async jobs |

## 📁 Structure

```
├── backend/           # FastAPI (Python)
│   ├── app/api/       # API routes
│   ├── app/models/    # SQLAlchemy models
│   ├── app/crud/      # Database operations
│   └── app/services/  # Business logic
├── frontend/          # Next.js 14 (TypeScript)
│   ├── src/app/       # App router pages
│   ├── src/components/# React components
│   └── src/lib/       # Utilities
└── docker-compose.yml # Docker setup
```

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up
```

### Local Development
```bash
# Start databases
docker-compose up postgres redis -d

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install && npm run dev
```

**URLs:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Admin: http://localhost:8000/admin

## ⚙️ Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/saas_db
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/saas_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-min-32-chars
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
OPENROUTER_API_KEY=sk-or-xxx
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/orgs/` | List organizations |
| POST | `/api/v1/billing/checkout` | Create Stripe checkout |
| GET | `/api/v1/billing/subscription` | Get subscription |
| POST | `/api/v1/ai/chat` | AI chat completion |
| POST | `/api/v1/ai/chat/stream` | AI streaming chat |

## 💳 Stripe Webhooks (Local)

```bash
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe
# Copy the webhook secret to .env
```

## 🧪 Testing

```bash
cd backend
pytest
pytest --cov=app  # with coverage
```

## 🚢 Deployment

**Railway:**
1. Connect GitHub repo
2. Add PostgreSQL & Redis services
3. Set environment variables
4. Deploy

## 📄 License

MIT License

---

Built with FastAPI, Next.js 14, Stripe, and AI ❤️
