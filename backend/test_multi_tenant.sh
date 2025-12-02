#!/bin/bash

API_URL="http://localhost:8000"

echo "🧪 Testing Multi-Tenant & API Key Features..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Register Owner
echo -e "${BLUE}1️⃣ Registering owner...${NC}"
OWNER_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@test.com",
    "password": "TestPass123!",
    "full_name": "Test Owner"
  }')
echo "$OWNER_RESPONSE" | jq '.'
echo ""

# 2. Login Owner
echo -e "${BLUE}2️⃣ Logging in owner...${NC}"
OWNER_LOGIN=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=owner@test.com&password=TestPass123!")
OWNER_TOKEN=$(echo $OWNER_LOGIN | jq -r '.access_token')
echo "Token: ${OWNER_TOKEN:0:20}..."
echo ""

# 3. Create Organization
echo -e "${BLUE}3️⃣ Creating organization...${NC}"
ORG_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Company",
    "slug": "test-company",
    "description": "A test organization"
  }')
echo "$ORG_RESPONSE" | jq '.'
ORG_ID=$(echo $ORG_RESPONSE | jq -r '.id')
echo ""

# 4. List Organizations
echo -e "${BLUE}4️⃣ Listing my organizations...${NC}"
curl -s -X GET "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $OWNER_TOKEN" | jq '.'
echo ""

# 5. Register Member
echo -e "${BLUE}5️⃣ Registering member...${NC}"
MEMBER_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "member@test.com",
    "password": "TestPass123!",
    "full_name": "Test Member"
  }')
echo "$MEMBER_RESPONSE" | jq '.'
echo ""

# 6. Invite Member
echo -e "${BLUE}6️⃣ Inviting member to organization...${NC}"
INVITE_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/orgs/$ORG_ID/invite" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "member@test.com",
    "role": "member"
  }')
echo "$INVITE_RESPONSE" | jq '.'
echo ""

# 7. List Members
echo -e "${BLUE}7️⃣ Listing organization members...${NC}"
curl -s -X GET "$API_URL/api/v1/orgs/$ORG_ID/members" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'
echo ""

# 8. Create API Key
echo -e "${BLUE}8️⃣ Creating API key...${NC}"
API_KEY_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/apikeys" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test API Key"
  }')
echo "$API_KEY_RESPONSE" | jq '.'
API_KEY=$(echo $API_KEY_RESPONSE | jq -r '.key')
echo -e "${YELLOW}⚠️  API Key (save this!): $API_KEY${NC}"
echo ""

# 9. List API Keys
echo -e "${BLUE}9️⃣ Listing API keys...${NC}"
curl -s -X GET "$API_URL/api/v1/apikeys" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'
echo ""

# 10. Test API Key Authentication
echo -e "${BLUE}🔟 Testing API key authentication...${NC}"
curl -s -X GET "$API_URL/api/v1/users/me" \
  -H "X-API-Key: $API_KEY" | jq '.'
echo ""

# 11. Member Login and Check Organizations
echo -e "${BLUE}1️⃣1️⃣ Member logging in and checking organizations...${NC}"
MEMBER_LOGIN=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=member@test.com&password=TestPass123!")
MEMBER_TOKEN=$(echo $MEMBER_LOGIN | jq -r '.access_token')
echo "Member Token: ${MEMBER_TOKEN:0:20}..."

curl -s -X GET "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $MEMBER_TOKEN" | jq '.'
echo ""

echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "Summary:"
echo "- Organization ID: $ORG_ID"
echo "- Owner Token: ${OWNER_TOKEN:0:30}..."
echo "- Member Token: ${MEMBER_TOKEN:0:30}..."
echo "- API Key: ${API_KEY:0:15}..."
