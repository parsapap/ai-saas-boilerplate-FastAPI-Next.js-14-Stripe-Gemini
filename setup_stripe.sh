#!/bin/bash

echo "🔧 Stripe Configuration Helper"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Current Configuration:${NC}"
echo "✅ Stripe Secret Key: Configured"
echo "✅ Stripe Publishable Key: Configured"
echo ""

echo -e "${YELLOW}⚠️  Next Steps:${NC}"
echo ""
echo "1️⃣  Create Products in Stripe Dashboard"
echo "   → Go to: https://dashboard.stripe.com/test/products"
echo "   → Create 'Pro Plan' - $29/month"
echo "   → Create 'Team Plan' - $99/month"
echo "   → Copy the Price IDs (price_...)"
echo ""

echo "2️⃣  Update Price IDs in code"
echo "   → Edit: backend/app/core/stripe_config.py"
echo "   → Replace 'price_pro_monthly' with your Pro Price ID"
echo "   → Replace 'price_team_monthly' with your Team Price ID"
echo ""

echo "3️⃣  Setup Webhook"
echo ""
echo "   Option A - Stripe CLI (Recommended):"
echo "   $ stripe login"
echo "   $ stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe"
echo "   → Copy the webhook secret (whsec_...)"
echo "   → Update STRIPE_WEBHOOK_SECRET in backend/.env"
echo ""
echo "   Option B - Manual:"
echo "   → Go to: https://dashboard.stripe.com/test/webhooks"
echo "   → Add endpoint: http://localhost:8000/api/v1/billing/webhook/stripe"
echo "   → Select events: checkout.session.completed, customer.subscription.*"
echo "   → Copy signing secret to backend/.env"
echo ""

echo "4️⃣  Test the setup"
echo "   $ ./backend/test_stripe.sh"
echo ""

echo -e "${GREEN}📚 Full guide: STRIPE_SETUP_STEPS.md${NC}"
echo ""

# Check if Stripe CLI is installed
if command -v stripe &> /dev/null; then
    echo -e "${GREEN}✅ Stripe CLI is installed${NC}"
    echo ""
    echo "Quick start webhook forwarding:"
    echo "$ stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe"
else
    echo -e "${YELLOW}⚠️  Stripe CLI not installed${NC}"
    echo ""
    echo "Install Stripe CLI:"
    echo "$ wget https://github.com/stripe/stripe-cli/releases/download/v1.19.0/stripe_1.19.0_linux_x86_64.tar.gz"
    echo "$ tar -xvf stripe_1.19.0_linux_x86_64.tar.gz"
    echo "$ sudo mv stripe /usr/local/bin/"
fi

echo ""
echo -e "${BLUE}Current Backend Status:${NC}"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running on port 8000${NC}"
    echo ""
    echo "Test plans endpoint:"
    echo "$ curl http://localhost:8000/api/v1/billing/plans | jq"
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    echo "Start backend with: ./start_backend.sh"
fi

echo ""
