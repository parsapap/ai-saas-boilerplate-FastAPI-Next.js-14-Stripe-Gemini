# 🚀 Deployment Guide

## Railway Deployment (Recommended)

### Prerequisites
- Railway account (https://railway.app)
- GitHub account
- Stripe account (for billing)
- AI API keys (Gemini, OpenAI, or Anthropic)

### Step 1: Prepare Your Repository

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/yourusername/ai-saas-boilerplate.git
   cd ai-saas-boilerplate
   ```

2. **Push to your GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

### Step 2: Create Railway Project

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### Step 3: Add Services

#### Add PostgreSQL
1. Click "New" → "Database" → "PostgreSQL"
2. Railway will automatically create and connect it

#### Add Redis
1. Click "New" → "Database" → "Redis"
2. Railway will automatically create and connect it

### Step 4: Configure Environment Variables

In your Railway backend service, add these variables:

```env
# Database (Auto-filled by Railway)
DATABASE_URL=postgresql+asyncpg://...
DATABASE_URL_SYNC=postgresql://...

# Redis (Auto-filled by Railway)
REDIS_URL=redis://...

# JWT (Generate a secure key)
SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Stripe (Get from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_live_your_production_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_production_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# AI APIs
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# App
APP_NAME=Your SaaS Name
APP_VERSION=1.0.0
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Port (Railway provides this)
PORT=${{PORT}}
```

### Step 5: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Wait for the build to complete
3. Your API will be live at: `https://your-app.up.railway.app`

### Step 6: Run Migrations

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations
railway run alembic upgrade head
```

### Step 7: Configure Stripe Webhook

1. Go to Stripe Dashboard → Webhooks
2. Add endpoint: `https://your-app.up.railway.app/api/v1/billing/webhook/stripe`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
4. Copy the webhook signing secret
5. Update `STRIPE_WEBHOOK_SECRET` in Railway

### Step 8: Test Your Deployment

```bash
# Health check
curl https://your-app.up.railway.app/health

# API docs
open https://your-app.up.railway.app/docs

# Admin panel
open https://your-app.up.railway.app/admin
```

---

## Docker Deployment

### Build and Run

```bash
# Build
docker-compose build

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs -f backend
```

### Production Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: saas_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/saas_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"

  celery_worker:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/saas_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
      - backend
    restart: unless-stopped
    command: celery -A app.tasks.celery_app worker --loglevel=info

  celery_beat:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@postgres:5432/saas_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
      - backend
    restart: unless-stopped
    command: celery -A app.tasks.celery_app beat --loglevel=info

volumes:
  postgres_data:
  redis_data:
```

---

## AWS Deployment

### Using ECS Fargate

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name ai-saas-backend
   ```

2. **Build and Push Docker Image**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   
   docker build -t ai-saas-backend ./backend
   docker tag ai-saas-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-saas-backend:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-saas-backend:latest
   ```

3. **Create RDS PostgreSQL Instance**
4. **Create ElastiCache Redis Cluster**
5. **Create ECS Task Definition**
6. **Create ECS Service**
7. **Configure Application Load Balancer**

---

## Kubernetes Deployment

### Helm Chart

```yaml
# values.yaml
replicaCount: 3

image:
  repository: your-registry/ai-saas-backend
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.yourdomain.com
      paths:
        - path: /
          pathType: Prefix

env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
  - name: REDIS_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: redis-url

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

healthCheck:
  liveness:
    path: /live
    initialDelaySeconds: 30
    periodSeconds: 10
  readiness:
    path: /ready
    initialDelaySeconds: 5
    periodSeconds: 5
```

---

## Monitoring Setup

### Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['your-app.up.railway.app:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

Import dashboard ID: `1860` (Node Exporter Full)

Create custom dashboard for:
- Request rate
- Response time
- Error rate
- Active subscriptions
- AI usage

---

## Post-Deployment Checklist

- [ ] Health checks passing (`/health`, `/ready`)
- [ ] API docs accessible (`/docs`)
- [ ] Admin panel accessible (`/admin`)
- [ ] Metrics endpoint working (`/metrics`)
- [ ] Database migrations applied
- [ ] Stripe webhook configured and tested
- [ ] SSL certificate installed
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Backup strategy in place
- [ ] Monitoring alerts configured
- [ ] Log aggregation setup
- [ ] Rate limiting configured
- [ ] Security headers set

---

## Troubleshooting

### Database Connection Issues
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
railway run python -c "from app.database import engine; print('Connected!')"
```

### Migration Issues
```bash
# Check current revision
railway run alembic current

# Show migration history
railway run alembic history

# Downgrade if needed
railway run alembic downgrade -1
```

### Celery Not Running
```bash
# Check Redis connection
railway run python -c "import redis; r=redis.from_url('$REDIS_URL'); print(r.ping())"

# Test Celery
railway run celery -A app.tasks.celery_app inspect active
```

---

## Support

Need help with deployment? Contact: [your-email@example.com]
