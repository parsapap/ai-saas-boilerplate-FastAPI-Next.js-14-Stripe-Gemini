# Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- Stripe account with API keys
- OpenRouter API key with credits

## Deploy to Railway

### 1. Login to Railway
```bash
railway login
```
This will open your browser for authentication.

### 2. Initialize Railway Project
```bash
railway init
```
Choose "Create new project" and give it a name.

### 3. Add PostgreSQL Database
```bash
railway add --database postgresql
```

### 4. Add Redis (Optional but recommended)
```bash
railway add --database redis
```

### 5. Set Environment Variables

#### Backend Environment Variables
```bash
# Database (automatically set by Railway)
# DATABASE_URL is auto-configured

# Security
railway variables set SECRET_KEY="your-super-secret-key-min-32-chars-change-this"
railway variables set ALGORITHM="HS256"
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set REFRESH_TOKEN_EXPIRE_DAYS="7"

# CORS (update with your frontend URL after deployment)
railway variables set BACKEND_CORS_ORIGINS="https://your-frontend-url.railway.app,https://your-backend-url.railway.app"

# OpenRouter API
railway variables set OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Stripe
railway variables set STRIPE_SECRET_KEY="sk_live_your-stripe-secret-key"
railway variables set STRIPE_PUBLISHABLE_KEY="pk_live_your-stripe-publishable-key"
railway variables set STRIPE_WEBHOOK_SECRET="whsec_your-webhook-secret"

# Environment
railway variables set ENVIRONMENT="production"
```

### 6. Deploy Backend
```bash
railway up
```

### 7. Get Backend URL
```bash
railway domain
```
Note the URL (e.g., `https://your-app.railway.app`)

### 8. Deploy Frontend (Separate Service)

Create a new Railway service for frontend:
```bash
cd frontend
railway init
```

Set frontend environment variables:
```bash
railway variables set NEXT_PUBLIC_API_URL="https://your-backend-url.railway.app"
railway variables set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_live_your-stripe-key"
```

Deploy frontend:
```bash
railway up
```

### 9. Update CORS Origins
Go back to backend and update CORS with actual frontend URL:
```bash
cd ../backend
railway variables set BACKEND_CORS_ORIGINS="https://your-frontend-url.railway.app,https://your-backend-url.railway.app"
```

### 10. Configure Stripe Webhooks
1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-backend-url.railway.app/api/v1/billing/webhook`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy the webhook secret and update:
```bash
railway variables set STRIPE_WEBHOOK_SECRET="whsec_new-webhook-secret"
```

## Alternative: Deploy with Docker Compose

### 1. Update docker-compose.yml
Make sure environment variables are set in your `.env` file.

### 2. Build and Deploy
```bash
docker-compose up -d --build
```

### 3. Check Logs
```bash
docker-compose logs -f
```

## Post-Deployment Checklist

- [ ] Backend is accessible at the Railway URL
- [ ] Frontend is accessible and can connect to backend
- [ ] Database migrations ran successfully
- [ ] Stripe webhooks are configured
- [ ] Test user registration
- [ ] Test subscription creation
- [ ] Test chat functionality
- [ ] Monitor logs for errors

## Troubleshooting

### Database Connection Issues
Check if DATABASE_URL is set correctly:
```bash
railway variables
```

### Migration Issues
Run migrations manually:
```bash
railway run alembic upgrade head
```

### View Logs
```bash
railway logs
```

### Restart Service
```bash
railway restart
```

## Environment Variables Reference

### Required Backend Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-set by Railway)
- `SECRET_KEY` - JWT secret key (min 32 characters)
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret
- `OPENROUTER_API_KEY` - OpenRouter API key
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins

### Required Frontend Variables
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key

### Optional Variables
- `REDIS_URL` - Redis connection string
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - Email configuration
- `ENVIRONMENT` - Set to "production"

## Monitoring

### Check Service Health
```bash
curl https://your-backend-url.railway.app/health
```

### View Metrics
Go to Railway dashboard to view:
- CPU usage
- Memory usage
- Request logs
- Error logs

## Scaling

Railway automatically scales based on usage. For manual scaling:
1. Go to Railway dashboard
2. Select your service
3. Adjust resources in Settings

## Cost Optimization

- Use Railway's free tier for development
- Upgrade to Pro plan for production ($5/month + usage)
- Monitor resource usage in dashboard
- Set up usage alerts

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: Create an issue in your repository
