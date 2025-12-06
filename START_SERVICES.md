# Start All Services

## ✅ Docker Services (Already Running)

PostgreSQL and Redis are running in Docker:

```bash
# Check status
docker ps | grep -E "postgres-saas|redis-saas"

# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## ✅ Backend (Already Running)

Backend is running on http://localhost:8000

```bash
# Check if running
curl http://localhost:8000/health

# View logs
tail -f backend/backend.log

# Stop backend
pkill -f "uvicorn app.main:app"

# Restart backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 Start Frontend

Open a new terminal and run:

```bash
cd frontend
npm run dev
```

Frontend will start on http://localhost:3000

## 📊 Service Status

- ✅ PostgreSQL: Running on port 5432
- ✅ Redis: Running on port 6379  
- ✅ Backend API: Running on http://localhost:8000
- ⏳ Frontend: Start manually with `npm run dev`

## 🔧 Useful Commands

### Stop All Services
```bash
# Stop Docker containers
docker stop postgres-saas redis-saas

# Stop backend
pkill -f "uvicorn app.main:app"

# Frontend stops with Ctrl+C in its terminal
```

### Restart All Services
```bash
# Start Docker containers
docker start postgres-saas redis-saas

# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload &

# Start frontend
cd frontend && npm run dev
```

### View Logs
```bash
# Backend logs
tail -f backend/backend.log

# Frontend logs (in its terminal)

# Docker logs
docker logs postgres-saas
docker logs redis-saas
```

## 🎯 Access Your App

Once frontend is running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔐 Database Connection

```
Host: localhost
Port: 5432
Database: saas_db
User: postgres
Password: postgres
```

## 📝 Environment Variables

Make sure your `.env` files are configured:
- `backend/.env` - Backend configuration
- `frontend/.env.local` - Frontend configuration (NEXT_PUBLIC_API_URL=http://localhost:8000)

## ✨ Everything is Ready!

Your AI SaaS platform is now running locally with:
- PostgreSQL database (Docker)
- Redis cache (Docker)
- FastAPI backend (Local)
- Next.js frontend (Start manually)

Happy coding! 🚀
