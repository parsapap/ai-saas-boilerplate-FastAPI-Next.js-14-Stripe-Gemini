#!/bin/bash

API_URL="http://localhost:8000"

echo "🤖 Testing AI Integration..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Register and Login
echo -e "${BLUE}1️⃣ Setting up user and organization...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Test123!")

if [ -z "$LOGIN_RESPONSE" ] || [ "$LOGIN_RESPONSE" == "null" ]; then
    echo "Creating new user..."
    curl -s -X POST "$API_URL/api/v1/auth/register" \
      -H "Content-Type: application/json" \
      -d '{
        "email": "test@example.com",
        "password": "Test123!",
        "full_name": "Test User"
      }' > /dev/null
    
    LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=test@example.com&password=Test123!")
fi

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "Token: ${TOKEN:0:20}..."

# Create org if needed
ORG_RESPONSE=$(curl -s "$API_URL/api/v1/orgs" \
  -H "Authorization: Bearer $TOKEN")
ORG_ID=$(echo $ORG_RESPONSE | jq -r '.[0].id')

if [ "$ORG_ID" == "null" ]; then
    echo "Creating organization..."
    ORG_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/orgs" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name":"Test Org","slug":"test-org"}')
    ORG_ID=$(echo $ORG_RESPONSE | jq -r '.id')
fi

echo "Organization ID: $ORG_ID"
echo ""

# 2. Get Available Models
echo -e "${BLUE}2️⃣ Getting available AI models...${NC}"
curl -s "$API_URL/api/v1/ai/models" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'
echo ""

# 3. Check Usage (before)
echo -e "${BLUE}3️⃣ Checking current usage...${NC}"
curl -s "$API_URL/api/v1/ai/usage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'
echo ""

# 4. Simple Chat Request
echo -e "${BLUE}4️⃣ Testing simple chat...${NC}"
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Say hello in Persian"}
    ],
    "model": "gemini-1.5-flash",
    "max_tokens": 100
  }')

echo "$CHAT_RESPONSE" | jq '.'
echo ""

# 5. Multi-turn Conversation
echo -e "${BLUE}5️⃣ Testing multi-turn conversation...${NC}"
curl -s -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "What is 2+2?"},
      {"role": "assistant", "content": "2+2 equals 4"},
      {"role": "user", "content": "What about 3+3?"}
    ],
    "model": "gemini-1.5-flash"
  }' | jq '.'
echo ""

# 6. Test with Different Model (if Pro/Team)
echo -e "${BLUE}6️⃣ Testing with different parameters...${NC}"
curl -s -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a haiku about coding"}
    ],
    "model": "gemini-1.5-flash",
    "temperature": 0.9,
    "max_tokens": 150
  }' | jq '.'
echo ""

# 7. Check Usage (after)
echo -e "${BLUE}7️⃣ Checking updated usage...${NC}"
curl -s "$API_URL/api/v1/ai/usage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq '.'
echo ""

# 8. Test Rate Limiting
echo -e "${BLUE}8️⃣ Testing rate limiting (sending 6 requests quickly)...${NC}"
for i in {1..6}; do
    echo -n "Request $i: "
    RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
      -X POST "$API_URL/api/v1/ai/chat" \
      -H "Authorization: Bearer $TOKEN" \
      -H "X-Current-Org: $ORG_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [{"role": "user", "content": "Hi"}],
        "model": "gemini-1.5-flash",
        "max_tokens": 10
      }')
    
    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
    
    if [ "$HTTP_CODE" = "429" ]; then
        echo -e "${YELLOW}Rate limited ✓${NC}"
    elif [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}Success ✓${NC}"
    else
        echo -e "Status: $HTTP_CODE"
    fi
    
    sleep 0.5
done
echo ""

# 9. Test Streaming (if supported)
echo -e "${BLUE}9️⃣ Testing streaming response...${NC}"
echo "Streaming output:"
curl -N -X POST "$API_URL/api/v1/ai/chat/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Count from 1 to 5"}
    ],
    "model": "gemini-1.5-flash",
    "max_tokens": 50
  }' 2>/dev/null | while read line; do
    if [[ $line == data:* ]]; then
        echo -n "${line#data: }"
    fi
done
echo ""
echo ""

echo -e "${GREEN}✅ All AI tests completed!${NC}"
echo ""
echo "Summary:"
echo "- Organization ID: $ORG_ID"
echo "- Model: gemini-1.5-flash"
echo "- Requests sent: 3+ chat requests"
echo ""
echo "Next steps:"
echo "1. Check usage at: $API_URL/api/v1/ai/usage"
echo "2. Try different models (if Pro/Team plan)"
echo "3. Test streaming in browser"
echo "4. Monitor rate limits"
