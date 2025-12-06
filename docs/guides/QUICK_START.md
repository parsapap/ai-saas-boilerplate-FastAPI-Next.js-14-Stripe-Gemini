# ⚡ Quick Start - Get Running in 2 Minutes!

## 🎯 One Command Setup

```bash
./start.sh
```

That's it! Your FastAPI AI SaaS is now running! 🎉

---

## 📍 Access Your Application

| Service | URL | Description |
|---------|-----|-------------|
| **API** | http://localhost:8000 | Main API |
| **Swagger Docs** | http://localhost:8000/docs | Interactive API docs |
| **ReDoc** | http://localhost:8000/redoc | Alternative docs |
| **Flower** | http://localhost:5555 | Celery task monitor |

---

## 🧪 Quick Test

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "FastAPI SaaS",
  "version": "1.0.0"
}
```

### 2. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "Demo123!",
    "full_name": "Demo User"
  }'
```

### 3. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=Demo123!"
```

### 4. Explore API

Open http://localhost:8000/docs in your browser and try the endpoints!

---

## 🔧 Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just Celery worker
docker-compose logs -f celery_worker
```

### Restart Services

```bash
docker-compose restart backend
```

### Stop Everything

```bash
docker-compose down
```

### Clean Restart

```bash
docker-compose down -v  # ⚠️ Deletes all data!
docker-compose up --build
```

---

## 📊 What's Running?

```bash
docker-compose ps
```

You should see:
- ✅ saas_postgres (PostgreSQL database)
- ✅ saas_redis (Redis cache)
- ✅ saas_backend (FastAPI app)
- ✅ saas_celery_worker (Background tasks)
- ✅ saas_celery_beat (Scheduled tasks)
- ✅ saas_flower (Task monitoring)

---

## 🎨 Features Available

### ✅ Authentication
- User registration
- JWT login
- Refresh tokens

### ✅ Multi-Tenant
- Organizations
- Team members
- Role-based access (owner/admin/member)

### ✅ API Keys
- Generate API keys
- Use instead of JWT
- Per-organization keys

### ✅ Billing (Stripe)
- 3 plans: Free, Pro ($29), Team ($99)
- Subscription management
- Webhooks

### ✅ AI Chat
- 4 models: Gemini, Claude, GPT
- Rate limiting
- Usage tracking
- Streaming support

### ✅ Background Tasks
- Celery workers
- Scheduled tasks
- Task monitoring (Flower)

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Services Not Starting

```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose up --build --force-recreate
```

### Database Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
docker-compose up backend
```

---

## 📚 Next Steps

1. **Configure API Keys**
   - Edit `backend/.env`
   - Add real Stripe keys
   - Add real Gemini API key

2. **Test Features**
   ```bash
   cd backend
   ./test_multi_tenant.sh
   ./test_stripe.sh
   ./test_ai.sh
   ```

3. **Read Documentation**
   - DEPLOYMENT_GUIDE.md
   - MULTI_TENANT_GUIDE.md
   - STRIPE_SETUP_GUIDE.md
   - AI_INTEGRATION_GUIDE.md

4. **Customize**
   - Add your business logic
   - Customize plans
   - Add more AI models
   - Deploy to production

---

## 🆘 Need Help?

- Check logs: `docker-compose logs -f`
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

**Happy coding! 🚀**
