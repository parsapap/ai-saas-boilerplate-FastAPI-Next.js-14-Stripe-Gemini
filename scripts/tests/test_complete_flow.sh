#!/bin/bash

# Complete End-to-End System Test
# Tests all functionality of the system

API_URL="http://localhost:8000"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test header
print_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}TEST #$TOTAL_TESTS: $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to check response
check_response() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

echo -e "${YELLOW}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              🧪 COMPLETE SYSTEM TEST                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# SECTION 1: HEALTH & BASIC CHECKS
# ============================================================================
echo -e "${YELLOW}📋 SECTION 1: Health & Basic Checks${NC}"

print_test "Health Check"
HEALTH=$(curl -s -w "\n%{http_code}" "$API_URL/health")
HTTP_CODE=$(echo "$HEALTH" | tail -n1)
BODY=$(echo "$HEALTH" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "API Documentation"
DOCS=$(curl -s -w "\n%{http_code}" "$API_URL/docs")
HTTP_CODE=$(echo "$DOCS" | tail -n1)
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

# ============================================================================
# SECTION 2: AUTHENTICATION - احراز هویت
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 2: Authentication Tests${NC}"

# Generate random email
RANDOM_NUM=$RANDOM
TEST_EMAIL="test_user_${RANDOM_NUM}@example.com"
TEST_PASSWORD="TestPass123!"
TEST_NAME="Test User $RANDOM_NUM"

print_test "User Registration"
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"full_name\": \"$TEST_NAME\"
  }")
HTTP_CODE=$(echo "$REGISTER_RESPONSE" | tail -n1)
BODY=$(echo "$REGISTER_RESPONSE" | head -n-1)
echo "Email: $TEST_EMAIL"
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "User Login"
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_EMAIL&password=$TEST_PASSWORD")
HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
BODY=$(echo "$LOGIN_RESPONSE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
TOKEN=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
if [ ! -z "$TOKEN" ]; then
    echo "Token: ${TOKEN:0:30}..."
    check_response 0
else
    echo "Failed to get token"
    check_response 1
fi

print_test "Get Current User"
USER_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN")
HTTP_CODE=$(echo "$USER_RESPONSE" | tail -n1)
BODY=$(echo "$USER_RESPONSE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

# ============================================================================
# SECTION 3: ORGANIZATIONS - سازمان‌ها
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 3: Organization Tests${NC}"

ORG_SLUG="test-org-${RANDOM_NUM}"

print_test "Create Organization"
ORG_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Test Organization $RANDOM_NUM\",
    \"slug\": \"$ORG_SLUG\",
    \"description\": \"Test organization for complete testing\"
  }")
HTTP_CODE=$(echo "$ORG_RESPONSE" | tail -n1)
BODY=$(echo "$ORG_RESPONSE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
ORG_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
if [ ! -z "$ORG_ID" ]; then
    echo "Organization ID: $ORG_ID"
    check_response 0
else
    echo "Failed to get organization ID"
    check_response 1
fi

print_test "List Organizations"
ORGS_LIST=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $TOKEN")
HTTP_CODE=$(echo "$ORGS_LIST" | tail -n1)
BODY=$(echo "$ORGS_LIST" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Get Organization Details"
ORG_DETAILS=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/orgs/$ORG_ID" \
  -H "Authorization: Bearer $TOKEN")
HTTP_CODE=$(echo "$ORG_DETAILS" | tail -n1)
BODY=$(echo "$ORG_DETAILS" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Update Organization"
UPDATE_ORG=$(curl -s -w "\n%{http_code}" -X PUT "$API_URL/api/v1/orgs/$ORG_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Updated Test Organization\",
    \"description\": \"Updated description\"
  }")
HTTP_CODE=$(echo "$UPDATE_ORG" | tail -n1)
BODY=$(echo "$UPDATE_ORG" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

# ============================================================================
# SECTION 4: API KEYS - کلیدهای API
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 4: API Keys Tests${NC}"

print_test "Create API Key"
APIKEY_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/apikeys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Test API Key\",
    \"description\": \"API key for testing\"
  }")
HTTP_CODE=$(echo "$APIKEY_RESPONSE" | tail -n1)
BODY=$(echo "$APIKEY_RESPONSE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
API_KEY=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['key'])" 2>/dev/null)
APIKEY_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
if [ ! -z "$API_KEY" ]; then
    echo "API Key: ${API_KEY:0:20}..."
    echo "API Key ID: $APIKEY_ID"
    check_response 0
else
    echo "Failed to get API key"
    check_response 1
fi

print_test "List API Keys"
APIKEYS_LIST=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/apikeys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$APIKEYS_LIST" | tail -n1)
BODY=$(echo "$APIKEYS_LIST" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Test API Key Authentication"
APIKEY_AUTH=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/users/me" \
  -H "X-API-Key: $API_KEY")
HTTP_CODE=$(echo "$APIKEY_AUTH" | tail -n1)
BODY=$(echo "$APIKEY_AUTH" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

# ============================================================================
# SECTION 5: BILLING & STRIPE - پرداخت و Stripe
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 5: Billing & Stripe Tests${NC}"

print_test "Get Available Plans"
PLANS=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/billing/plans")
HTTP_CODE=$(echo "$PLANS" | tail -n1)
BODY=$(echo "$PLANS" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ]; then
    # Check if Pro and Team plans have price IDs
    if echo "$BODY" | grep -q "price_1SaL4MJQFLCmojG3bVa6HbGt"; then
        echo "✓ Pro Plan Price ID found"
    fi
    if echo "$BODY" | grep -q "price_1SaL8SJQFLCmojG3vspXn8TA"; then
        echo "✓ Team Plan Price ID found"
    fi
    check_response 0
else
    check_response 1
fi

print_test "Get Current Subscription"
SUBSCRIPTION=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/billing/subscription" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$SUBSCRIPTION" | tail -n1)
BODY=$(echo "$SUBSCRIPTION" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Create Checkout Session (Pro Plan)"
CHECKOUT=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/billing/checkout" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"plan_type\": \"pro\",
    \"success_url\": \"http://localhost:3000/success\",
    \"cancel_url\": \"http://localhost:3000/cancel\"
  }")
HTTP_CODE=$(echo "$CHECKOUT" | tail -n1)
BODY=$(echo "$CHECKOUT" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
CHECKOUT_URL=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['checkout_url'])" 2>/dev/null)
if [ ! -z "$CHECKOUT_URL" ]; then
    echo "Checkout URL: ${CHECKOUT_URL:0:50}..."
    check_response 0
else
    check_response 1
fi

print_test "Create Customer Portal Session"
PORTAL=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/billing/portal" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"return_url\": \"http://localhost:3000/settings\"
  }")
HTTP_CODE=$(echo "$PORTAL" | tail -n1)
BODY=$(echo "$PORTAL" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
PORTAL_URL=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['portal_url'])" 2>/dev/null)
if [ ! -z "$PORTAL_URL" ]; then
    echo "Portal URL: ${PORTAL_URL:0:50}..."
    check_response 0
else
    check_response 1
fi

# ============================================================================
# SECTION 6: PREMIUM FEATURES - ویژگی‌های پریمیوم
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 6: Premium Features Tests${NC}"

print_test "Access Free Feature"
FREE_FEATURE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/premium/free-feature" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$FREE_FEATURE" | tail -n1)
BODY=$(echo "$FREE_FEATURE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Access Pro Feature (Should Fail)"
PRO_FEATURE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/premium/analytics" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$PRO_FEATURE" | tail -n1)
BODY=$(echo "$PRO_FEATURE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
if [ "$HTTP_CODE" = "403" ]; then
    echo "✓ Correctly blocked (Free plan cannot access Pro features)"
    check_response 0
else
    echo "✗ Should have been blocked"
    check_response 1
fi

print_test "Access Team Feature (Should Fail)"
TEAM_FEATURE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/premium/team-reports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$TEAM_FEATURE" | tail -n1)
BODY=$(echo "$TEAM_FEATURE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
if [ "$HTTP_CODE" = "403" ]; then
    echo "✓ Correctly blocked (Free plan cannot access Team features)"
    check_response 0
else
    echo "✗ Should have been blocked"
    check_response 1
fi

# ============================================================================
# SECTION 7: AI FEATURES - ویژگی‌های هوش مصنوعی
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 7: AI Features Tests - تست ویژگی‌های AI${NC}"

print_test "List AI Providers"
AI_PROVIDERS=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/ai/providers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$AI_PROVIDERS" | tail -n1)
BODY=$(echo "$AI_PROVIDERS" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Chat with AI (Gemini)"
AI_CHAT=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Hello, this is a test message\",
    \"provider\": \"gemini\"
  }")
HTTP_CODE=$(echo "$AI_CHAT" | tail -n1)
BODY=$(echo "$AI_CHAT" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Get AI Usage Stats"
AI_USAGE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/ai/usage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$AI_USAGE" | tail -n1)
BODY=$(echo "$AI_USAGE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

# ============================================================================
# SECTION 8: CLEANUP - پاکسازی
# ============================================================================
echo ""
echo -e "${YELLOW}📋 SECTION 8: Cleanup Tests${NC}"

print_test "Revoke API Key"
REVOKE_KEY=$(curl -s -w "\n%{http_code}" -X DELETE "$API_URL/api/v1/apikeys/$APIKEY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID")
HTTP_CODE=$(echo "$REVOKE_KEY" | tail -n1)
BODY=$(echo "$REVOKE_KEY" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
[ "$HTTP_CODE" = "200" ] && check_response 0 || check_response 1

print_test "Verify API Key is Revoked"
VERIFY_REVOKE=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/users/me" \
  -H "X-API-Key: $API_KEY")
HTTP_CODE=$(echo "$VERIFY_REVOKE" | tail -n1)
BODY=$(echo "$VERIFY_REVOKE" | head -n-1)
echo "Response: $BODY"
echo "HTTP Code: $HTTP_CODE"
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    echo "✓ API Key correctly revoked"
    check_response 0
else
    echo "✗ API Key should be revoked"
    check_response 1
fi

# ============================================================================
# FINAL SUMMARY - خلاصه نهایی
# ============================================================================
echo ""
echo -e "${YELLOW}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    📊 TEST SUMMARY                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}Total Tests:${NC} $TOTAL_TESTS"
echo -e "${GREEN}Passed:${NC} $PASSED_TESTS"
echo -e "${RED}Failed:${NC} $FAILED_TESTS"

SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo -e "${CYAN}Success Rate:${NC} $SUCCESS_RATE%"

echo ""
echo -e "${YELLOW}📝 Test Details:${NC}"
echo "   User Email: $TEST_EMAIL"
echo "   Organization ID: $ORG_ID"
echo "   Organization Slug: $ORG_SLUG"
echo ""

if [ "$CHECKOUT_URL" != "" ]; then
    echo -e "${YELLOW}💳 Payment Test:${NC}"
    echo "   Checkout URL: $CHECKOUT_URL"
    echo ""
    echo "   To complete payment test:"
    echo "   1. Open the checkout URL in browser"
    echo "   2. Use test card: 4242 4242 4242 4242"
    echo "   3. Complete the payment"
    echo "   4. Check webhook in Stripe Dashboard"
    echo ""
fi

echo -e "${YELLOW}🔗 Useful Links:${NC}"
echo "   API Docs: http://localhost:8000/docs"
echo "   Stripe Dashboard: https://dashboard.stripe.com/test"
echo "   Stripe Payments: https://dashboard.stripe.com/test/payments"
echo "   Stripe Webhooks: https://dashboard.stripe.com/test/webhooks"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! System is working perfectly!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please check the errors above.${NC}"
    exit 1
fi
