#!/bin/bash
# Comprehensive Feature Test Script

echo "========================================="
echo "AI SaaS Platform - Complete Feature Test"
echo "========================================="
echo ""

API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local headers=$5
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" $headers "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method $headers -H "Content-Type: application/json" -d "$data" "$API_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
        echo "  Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "========================================="
echo "1. HEALTH CHECKS"
echo "========================================="

test_endpoint "Health Check" "GET" "/health"
test_endpoint "Readiness Check" "GET" "/ready"
test_endpoint "Liveness Check" "GET" "/live"
echo ""

echo "========================================="
echo "2. AUTHENTICATION"
echo "========================================="

# Register new user
EMAIL="test_$(date +%s)@example.com"
PASSWORD="TestPass123!"

echo "Registering user: $EMAIL"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"full_name\":\"Test User\"}")

if echo "$REGISTER_RESPONSE" | grep -q "email"; then
    echo -e "${GREEN}✓ Registration successful${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ Registration failed${NC}"
    echo "  Response: $REGISTER_RESPONSE"
    FAILED=$((FAILED + 1))
fi

# Login
echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD")

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful${NC}"
    echo "  Token: ${TOKEN:0:20}..."
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ Login failed${NC}"
    echo "  Response: $LOGIN_RESPONSE"
    FAILED=$((FAILED + 1))
    echo ""
    echo "Cannot continue without authentication token"
    exit 1
fi
echo ""

echo "========================================="
echo "3. USER PROFILE"
echo "========================================="

test_endpoint "Get Current User" "GET" "/api/v1/users/me" "" "-H \"Authorization: Bearer $TOKEN\""
echo ""

echo "========================================="
echo "4. BILLING"
echo "========================================="

test_endpoint "Get Plans" "GET" "/api/v1/billing/plans"
test_endpoint "Get Subscription" "GET" "/api/v1/billing/subscription" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
echo ""

echo "========================================="
echo "5. API KEYS"
echo "========================================="

# Create API Key
echo "Creating API key..."
API_KEY_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/apikeys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Key"}')

if echo "$API_KEY_RESPONSE" | grep -q "key"; then
    echo -e "${GREEN}✓ API Key created${NC}"
    API_KEY_ID=$(echo "$API_KEY_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}✗ API Key creation failed${NC}"
    echo "  Response: $API_KEY_RESPONSE"
    FAILED=$((FAILED + 1))
fi

# List API Keys
test_endpoint "List API Keys" "GET" "/api/v1/apikeys" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""

# Delete API Key
if [ -n "$API_KEY_ID" ]; then
    test_endpoint "Delete API Key" "DELETE" "/api/v1/apikeys/$API_KEY_ID" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
fi
echo ""

echo "========================================="
echo "6. ORGANIZATIONS"
echo "========================================="

test_endpoint "List Organizations" "GET" "/api/v1/orgs" "" "-H \"Authorization: Bearer $TOKEN\""
test_endpoint "Get Organization" "GET" "/api/v1/orgs/1" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
test_endpoint "List Members" "GET" "/api/v1/orgs/1/members" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
echo ""

echo "========================================="
echo "7. AI & CHAT"
echo "========================================="

# Test non-streaming chat
echo "Testing AI chat (non-streaming)..."
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 1" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!","model":"gemini","stream":false}')

if echo "$CHAT_RESPONSE" | grep -q "response\|content\|message"; then
    echo -e "${GREEN}✓ AI Chat works${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${YELLOW}⚠ AI Chat response unexpected${NC}"
    echo "  Response: $CHAT_RESPONSE"
    FAILED=$((FAILED + 1))
fi

test_endpoint "Get AI Models" "GET" "/api/v1/ai/models" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
test_endpoint "Get AI Usage" "GET" "/api/v1/ai/usage" "" "-H \"Authorization: Bearer $TOKEN\" -H \"X-Current-Org: 1\""
echo ""

echo "========================================="
echo "8. PREMIUM FEATURES"
echo "========================================="

test_endpoint "Free Feature" "GET" "/api/v1/premium/free-feature" "" "-H \"Authorization: Bearer $TOKEN\""
echo ""

echo "========================================="
echo "FRONTEND PAGES"
echo "========================================="

echo "Checking frontend pages..."
for page in "" "login" "register" "pricing" "dashboard" "chat" "team" "billing" "api-keys" "settings"; do
    if [ -z "$page" ]; then
        url="$FRONTEND_URL/"
        name="Home"
    else
        url="$FRONTEND_URL/$page"
        name="$page"
    fi
    
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$http_code" = "200" ]; then
        echo -e "  $name: ${GREEN}✓ $http_code${NC}"
    else
        echo -e "  $name: ${YELLOW}⚠ $http_code${NC}"
    fi
done
echo ""

echo "========================================="
echo "TEST SUMMARY"
echo "========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed${NC}"
    exit 1
fi
