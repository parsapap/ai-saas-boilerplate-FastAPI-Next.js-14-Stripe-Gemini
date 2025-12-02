#!/bin/bash

API_URL="http://localhost:8000"

echo "💳 Testing Stripe Integration..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Register and Login
echo -e "${BLUE}1️⃣ Registering user...${NC}"
curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "stripe-test@example.com",
    "password": "TestPass123!",
    "full_name": "Stripe Test User"
  }' | jq '.'

echo ""
echo -e "${BLUE}2️⃣ Logging in...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=stripe-test@example.com&password=TestPass123!")
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "Token: ${TOKEN:0:20}..."

# 2. Create Organization
echo ""
echo -e "${BLUE}3️⃣ Creating organization...${NC}"
ORG_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Stripe Test Org",
    "slug": "stripe-test-org"
  }')
echo "$ORG_RESPONSE" | jq '.'
ORG_ID=$(echo $ORG_RESPONSE | jq -r '.id')

# 3. Get Available Plans
echo ""
echo -e "${BLUE}4️⃣ Getting available plans...${NC}"
curl -s "$API_URL/api/v1/billing/plans" | jq '.'

# 4. Get Current Subscription (should be Free)
echo ""
echo -e "${BLUE}5️⃣ Getting current subscription...${NC}"
curl -s "$API_URL/api/v1/billing/subscription" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'

# 5. Try to access Pro feature (should fail)
echo ""
echo -e "${BLUE}6️⃣ Trying to access Pro feature (should fail)...${NC}"
ANALYTICS_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
  "$API_URL/api/v1/premium/analytics" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$ANALYTICS_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$ANALYTICS_RESPONSE" | sed '/HTTP_CODE/d')

if [ "$HTTP_CODE" = "403" ]; then
    echo -e "${RED}❌ Access denied (as expected)${NC}"
    echo "$BODY" | jq '.'
else
    echo -e "${GREEN}✅ Unexpected success${NC}"
    echo "$BODY" | jq '.'
fi

# 6. Try free feature (should work)
echo ""
echo -e "${BLUE}7️⃣ Trying free feature (should work)...${NC}"
curl -s "$API_URL/api/v1/premium/free-feature" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'

# 7. Create Checkout Session
echo ""
echo -e "${BLUE}8️⃣ Creating checkout session for Pro plan...${NC}"
CHECKOUT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/billing/checkout" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "pro",
    "success_url": "http://localhost:3000/success",
    "cancel_url": "http://localhost:3000/cancel"
  }')
echo "$CHECKOUT_RESPONSE" | jq '.'
CHECKOUT_URL=$(echo $CHECKOUT_RESPONSE | jq -r '.checkout_url')

if [ "$CHECKOUT_URL" != "null" ]; then
    echo ""
    echo -e "${YELLOW}🔗 Checkout URL:${NC}"
    echo "$CHECKOUT_URL"
    echo ""
    echo -e "${YELLOW}⚠️  Open this URL in browser to complete payment${NC}"
fi

# 8. Create Customer Portal Session
echo ""
echo -e "${BLUE}9️⃣ Creating customer portal session...${NC}"
PORTAL_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/billing/portal" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "return_url": "http://localhost:3000/settings"
  }')
echo "$PORTAL_RESPONSE" | jq '.'
PORTAL_URL=$(echo $PORTAL_RESPONSE | jq -r '.portal_url')

if [ "$PORTAL_URL" != "null" ]; then
    echo ""
    echo -e "${YELLOW}🔗 Portal URL:${NC}"
    echo "$PORTAL_URL"
fi

echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "Summary:"
echo "- Organization ID: $ORG_ID"
echo "- Current Plan: Free"
echo "- Checkout URL: ${CHECKOUT_URL:0:50}..."
echo ""
echo "Next steps:"
echo "1. Open checkout URL to upgrade"
echo "2. Use Stripe test card: 4242 4242 4242 4242"
echo "3. After payment, webhook will update subscription"
echo "4. Try accessing /premium/analytics again"
