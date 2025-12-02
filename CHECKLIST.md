# ✅ Setup Checklist

Use this checklist to get your FastAPI SaaS backend up and running.

## 🚀 Initial Setup

### 1. Prerequisites
- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] Git installed (if cloning)
- [ ] Text editor ready

### 2. Environment Configuration
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Generate SECRET_KEY: `openssl rand -hex 32`
- [ ] Update SECRET_KEY in `backend/.env`
- [ ] (Optional) Add Stripe keys if using billing features

### 3. Start Services
- [ ] Run `./start.sh` or `docker-compose up -d`
- [ ] Wait for services to start (30 seconds)
- [ ] Check services: `docker-compose ps`
- [ ] View logs: `docker-compose logs -f backend`

### 4. Verify Installation
- [ ] Visit http://localhost:8000
- [ ] Visit http://localhost:8000/docs (Swagger UI)
- [ ] Visit http://localhost:8000/health
- [ ] Check database: `docker-compose exec db psql -U postgres -d saas_db`

## 🧪 Testing

### 5. Test API Endpoints
- [ ] Run `cd backend && ./test_api.sh`
- [ ] Or test manually with curl/Postman
- [ ] Register a test user
- [ ] Login with test user
- [ ] Get user profile with token

### 6. Test Database
- [ ] Check migrations: `docker-compose exec backend alembic current`
- [ ] View users table: `docker-compose exec db psql -U postgres -d saas_db -c "SELECT * FROM users;"`

## 🔧 Configuration

### 7. Stripe Setup (Optional)
- [ ] Create Stripe account at https://stripe.com
- [ ] Get test API keys from https://dashboard.stripe.com/apikeys
- [ ] Add STRIPE_SECRET_KEY to `backend/.env`
- [ ] Add STRIPE_PUBLISHABLE_KEY to `backend/.env`
- [ ] Test customer creation on user registration

### 8. Security Configuration
- [ ] Change SECRET_KEY to production value
- [ ] Update ALLOWED_ORIGINS for your frontend domain
- [ ] Set DEBUG=False for production
- [ ] Review CORS settings

## 📝 Customization

### 9. Customize User Model
- [ ] Edit `backend/app/models/user.py`
- [ ] Add custom fields as needed
- [ ] Create migration: `docker-compose exec backend alembic revision --autogenerate -m "Add custom fields"`
- [ ] Apply migration: `docker-compose exec backend alembic upgrade head`

### 10. Add Custom Endpoints
- [ ] Create new route file in `backend/app/api/v1/`
- [ ] Add CRUD operations in `backend/app/crud/`
- [ ] Add schemas in `backend/app/schemas/`
- [ ] Register router in `backend/app/main.py`

### 11. Add Business Logic
- [ ] Implement services in `backend/app/crud/`
- [ ] Add validation in schemas
- [ ] Add error handling
- [ ] Add logging

## 🚢 Deployment Preparation

### 12. Production Environment
- [ ] Create production `.env` file
- [ ] Use production database URL
- [ ] Use production Stripe keys
- [ ] Set DEBUG=False
- [ ] Configure proper CORS origins
- [ ] Set up SSL/HTTPS

### 13. Database Backup
- [ ] Set up automated backups
- [ ] Test restore procedure
- [ ] Document backup strategy

### 14. Monitoring & Logging
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure logging
- [ ] Set up health checks
- [ ] Configure alerts

### 15. Security Hardening
- [ ] Review all environment variables
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Set up firewall rules
- [ ] Enable HTTPS only
- [ ] Review CORS settings

## 📊 Performance Optimization

### 16. Database Optimization
- [ ] Add indexes for frequently queried fields
- [ ] Optimize slow queries
- [ ] Set up connection pooling
- [ ] Consider read replicas

### 17. Caching
- [ ] Implement Redis caching for frequent queries
- [ ] Cache API responses where appropriate
- [ ] Set up session storage in Redis

### 18. Background Jobs
- [ ] Set up Celery workers for async tasks
- [ ] Configure task queues
- [ ] Add monitoring for background jobs

## 🧪 Testing & Quality

### 19. Add Tests
- [ ] Write unit tests for CRUD operations
- [ ] Write integration tests for API endpoints
- [ ] Add authentication tests
- [ ] Test error handling

### 20. Code Quality
- [ ] Set up linting (flake8, black)
- [ ] Add type hints
- [ ] Write docstrings
- [ ] Review code for best practices

## 📚 Documentation

### 21. Update Documentation
- [ ] Update README with project-specific info
- [ ] Document custom endpoints
- [ ] Add API usage examples
- [ ] Document deployment process

### 22. Team Onboarding
- [ ] Create developer setup guide
- [ ] Document architecture decisions
- [ ] Add troubleshooting guide
- [ ] Create contribution guidelines

## 🎉 Launch

### 23. Pre-Launch
- [ ] Run full test suite
- [ ] Load test the API
- [ ] Security audit
- [ ] Backup database
- [ ] Prepare rollback plan

### 24. Launch
- [ ] Deploy to production
- [ ] Run migrations
- [ ] Verify all services running
- [ ] Test critical paths
- [ ] Monitor logs and metrics

### 25. Post-Launch
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Gather user feedback
- [ ] Plan next iteration

## 🔄 Maintenance

### 26. Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review security advisories
- [ ] Backup database regularly
- [ ] Monitor disk space
- [ ] Review logs for errors
- [ ] Update documentation

### 27. Scaling
- [ ] Monitor resource usage
- [ ] Plan for horizontal scaling
- [ ] Optimize database queries
- [ ] Implement caching strategy
- [ ] Consider CDN for static assets

---

## Quick Reference

### Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Access database
docker-compose exec db psql -U postgres -d saas_db

# Access Redis
docker-compose exec redis redis-cli

# Restart backend
docker-compose restart backend

# Rebuild backend
docker-compose up -d --build backend
```

### Useful URLs

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

**Print this checklist and check off items as you complete them!**
