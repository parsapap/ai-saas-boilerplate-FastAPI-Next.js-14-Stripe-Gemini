#!/bin/bash

echo "🚀 Railway Deployment Helper"
echo "=============================="
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed"
    echo "Install it with: curl -fsSL https://railway.app/install.sh | sh"
    exit 1
fi

echo "✅ Railway CLI is installed"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
    echo ""
fi

echo "👤 Logged in as: $(railway whoami)"
echo ""

# Ask user what to deploy
echo "What would you like to deploy?"
echo "1) Backend only"
echo "2) Frontend only"
echo "3) Both (recommended for first deployment)"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📦 Deploying Backend..."
        cd backend
        railway up
        echo ""
        echo "✅ Backend deployed!"
        echo "Get your backend URL with: railway domain"
        ;;
    2)
        echo ""
        echo "📦 Deploying Frontend..."
        cd frontend
        railway up
        echo ""
        echo "✅ Frontend deployed!"
        echo "Get your frontend URL with: railway domain"
        ;;
    3)
        echo ""
        echo "📦 Deploying Backend first..."
        cd backend
        railway up
        BACKEND_URL=$(railway domain 2>/dev/null | grep -o 'https://[^[:space:]]*' | head -1)
        echo "Backend URL: $BACKEND_URL"
        
        echo ""
        echo "📦 Now deploying Frontend..."
        cd ../frontend
        
        if [ ! -z "$BACKEND_URL" ]; then
            echo "Setting NEXT_PUBLIC_API_URL to $BACKEND_URL"
            railway variables set NEXT_PUBLIC_API_URL="$BACKEND_URL"
        fi
        
        railway up
        FRONTEND_URL=$(railway domain 2>/dev/null | grep -o 'https://[^[:space:]]*' | head -1)
        echo "Frontend URL: $FRONTEND_URL"
        
        echo ""
        echo "✅ Both services deployed!"
        echo ""
        echo "📝 Next steps:"
        echo "1. Update CORS in backend: railway variables set BACKEND_CORS_ORIGINS=\"$FRONTEND_URL,$BACKEND_URL\""
        echo "2. Configure Stripe webhook: $BACKEND_URL/api/v1/billing/webhook"
        echo "3. Test your application at: $FRONTEND_URL"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📚 For more details, see DEPLOYMENT.md"
