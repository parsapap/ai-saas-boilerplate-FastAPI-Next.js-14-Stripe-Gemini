#!/bin/bash

echo "🚀 AI SaaS Deployment Script"
echo "=============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI installed"
echo ""

# Login to Railway
echo "🔐 Logging in to Railway..."
railway login

echo ""
echo "📦 Linking to Railway project..."
railway link

echo ""
echo "🔧 Running database migrations..."
railway run alembic upgrade head

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Your application is live at:"
railway status

echo ""
echo "🔗 Quick Links:"
echo "   - API Docs: https://your-app.up.railway.app/docs"
echo "   - Admin Panel: https://your-app.up.railway.app/admin"
echo "   - Metrics: https://your-app.up.railway.app/metrics"
echo "   - Health: https://your-app.up.railway.app/health"
echo ""
echo "📝 Next Steps:"
echo "   1. Configure Stripe webhook URL in Stripe Dashboard"
echo "   2. Test the API endpoints"
echo "   3. Access admin panel and verify data"
echo "   4. Set up monitoring alerts"
echo ""
