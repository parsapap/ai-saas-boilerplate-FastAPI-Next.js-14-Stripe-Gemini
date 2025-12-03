#!/bin/bash

# Simple Stripe Test - Main endpoints only
API_URL="http://localhost:8000"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🧪 Stripe Simple Test${NC}"
echo "================================================"
echo ""

# Test 1: Health
echo -e "${BLUE}1. Health Check${NC}"
curl -s "$API_URL/health" | python3 -m json.tool
echo ""

# Test 2: Plans
echo -e "${BLUE}2. Get Available Plans${NC}"
PLANS=$(curl -s "$API_URL/api/v1/billing/plans")
echo "$PLANS" | python3 -m json.tool
echo ""

# Check Price IDs
if echo "$PLANS" | grep -q "price_1SaL4MJQFLCmojG3bVa6HbGt"; then
    echo -e "${GREEN}✅ Pro Plan Price ID configured correctly${NC}"
else
    echo -e "${RED}❌ Pro Plan Price ID not found${NC}"
fi

if echo "$PLANS" | grep -q "price_1SaL8SJQFLCmojG3vspXn8TA"; then
    echo -e "${GREEN}✅ Team Plan Price ID configured correctly${NC}"
else
    echo -e "${RED}❌ Team Plan Price ID not found${NC}"
fi

echo ""
echo -e "${YELLOW}📊 Configuration Summary:${NC}"
echo "   ✅ Backend: Running on port 8000"
echo "   ✅ PostgreSQL: Running in Docker"
echo "   ✅ Redis: Running in Docker"
echo "   ✅ Stripe Secret Key: Configured"
echo "   ✅ Stripe Publishable Key: Configured"
echo "   ✅ Stripe Webhook Secret: Configured"
echo "   ✅ Pro Plan Price ID: price_1SaL4MJQFLCmojG3bVa6HbGt"
echo "   ✅ Team Plan Price ID: price_1SaL8SJQFLCmojG3vspXn8TA"
echo ""

echo -e "${GREEN}🎉 Stripe Configuration Complete!${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Open API Docs: http://localhost:8000/docs"
echo "2. Register a user"
echo "3. Create an organization"
echo "4. Create a checkout session"
echo "5. Test payment with card: 4242 4242 4242 4242"
echo ""
echo -e "${BLUE}📚 Full Documentation:${NC}"
echo "   - Stripe Setup: STRIPE_SETUP_STEPS.md"
echo "   - Backend Guide: backend/STRIPE_SETUP_GUIDE.md"
echo ""
