# 🚀 AI SaaS Boilerplate - The Insanely Complete Starter Kit

**Stop wasting weeks on boilerplate. Start building your AI SaaS in minutes.**

This is the most complete, production-ready AI SaaS boilerplate you'll find. FastAPI backend + Next.js 14 frontend + Docker + Authentication + Payments + AI Integration. Everything you need, nothing you don't.

## 🔥 What's Inside

- **Backend**: FastAPI with async/await, SQLAlchemy ORM, Alembic migrations
- **Frontend**: Next.js 14 App Router, TypeScript, Tailwind CSS, shadcn/ui
- **Auth**: JWT-based authentication with refresh tokens
- **Database**: PostgreSQL with async support
- **Payments**: Stripe integration ready to go
- **AI Ready**: OpenAI API integration examples
- **Docker**: Full containerization with docker-compose
- **Production Ready**: Environment configs, error handling, logging

## 🎯 Quick Start

```bash
# Clone and setup
git clone <your-repo>
cd ai-saas-boilerplate

# Copy environment files
cp .env.example .env

# Start everything with Docker
docker-compose up -d

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it. You're running.

## 📁 Project Structure

```
ai-saas-boilerplate/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, security, dependencies
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── main.py      # Application entry
│   ├── alembic/         # Database migrations
│   ├── tests/           # Backend tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/            # Next.js 14 application
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities, API client
│   │   └── types/       # TypeScript types
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml   # Orchestration
├── .env.example         # Environment template
└── README.md           # You are here
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - Async ORM
- **PostgreSQL** - Production database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Secure authentication
- **OpenAI** - AI integration

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful components
- **Axios** - HTTP client
- **Zustand** - State management

## 🔧 Configuration

Edit `.env` file with your credentials:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/dbname

# JWT
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-your-key

# Stripe
STRIPE_SECRET_KEY=sk_test_your-key
STRIPE_WEBHOOK_SECRET=whsec_your-secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚢 Deployment

### Docker (Recommended)
```bash
docker-compose up -d --build
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 Features

### Authentication
- User registration and login
- JWT access and refresh tokens
- Password hashing with bcrypt
- Protected routes

### AI Integration
- OpenAI API wrapper
- Streaming responses
- Token usage tracking
- Error handling

### Payments
- Stripe checkout
- Subscription management
- Webhook handling
- Payment history

### Database
- Async PostgreSQL
- Automatic migrations
- Relationship management
- Query optimization

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT - Do whatever you want with this.

## 💪 Contributing

PRs welcome. Keep it clean, keep it simple.

## 🤝 Support

Found a bug? Open an issue.
Want a feature? Open an issue.
Want to say thanks? Star the repo.

---

**Now stop reading and start building.** 🚀
