#!/bin/bash

echo "🧪 Running Complete Test Suite..."
echo ""

API_URL="http://localhost:8000"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected $expected_code, got $http_code)"
        ((FAILED++))
    fi
}

echo -e "${BLUE}=== Basic Endpoints ===${NC}"
test_endpoint "Root" "$API_URL/"
test_endpoint "Health Check" "$API_URL/health"
test_endpoint "API Docs" "$API_URL/docs"
test_endpoint "ReDoc" "$API_URL/redoc"
test_endpoint "OpenAPI JSON" "$API_URL/openapi.json"
echo ""

echo -e "${BLUE}=== Authentication Endpoints ===${NC}"
test_endpoint "Register endpoint exists" "$API_URL/api/v1/auth/register" 422
test_endpoint "Login endpoint exists" "$API_URL/api/v1/auth/login" 422
echo ""

echo -e "${BLUE}=== Organization Endpoints ===${NC}"
test_endpoint "Organizations list (requires auth)" "$API_URL/api/v1/orgs" 401
echo ""

echo -e "${BLUE}=== Billing Endpoints ===${NC}"
test_endpoint "Plans list" "$API_URL/api/v1/billing/plans"
echo ""

echo -e "${BLUE}=== AI Endpoints ===${NC}"
test_endpoint "AI models (requires auth)" "$API_URL/api/v1/ai/models" 401
echo ""

echo -e "${BLUE}=== Services Status ===${NC}"
echo "Checking Docker services..."
docker-compose ps
echo ""

echo -e "${BLUE}=== Database Connection ===${NC}"
echo -n "Testing PostgreSQL... "
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Connected${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Failed${NC}"
    ((FAILED++))
fi

echo -n "Testing Redis... "
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Connected${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Failed${NC}"
    ((FAILED++))
fi
echo ""

echo -e "${BLUE}=== Summary ===${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Visit http://localhost:8000/docs"
    echo "2. Try registering a user"
    echo "3. Run detailed tests:"
    echo "   cd backend && ./test_multi_tenant.sh"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Check logs:"
    echo "  docker-compose logs backend"
    exit 1
fi
