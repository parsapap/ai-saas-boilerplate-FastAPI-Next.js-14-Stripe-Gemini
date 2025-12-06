#!/bin/bash

# Test chat API endpoint
# Usage: ./test_chat_api.sh <access_token> <org_id>

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./test_chat_api.sh <access_token> <org_id>"
    echo ""
    echo "Get your access token from localStorage in browser console:"
    echo "  localStorage.getItem('access_token')"
    echo ""
    echo "Get your org ID from localStorage:"
    echo "  localStorage.getItem('current_org_id')"
    exit 1
fi

TOKEN=$1
ORG_ID=$2
API_URL=${API_URL:-http://localhost:8000}

echo "Testing Chat API..."
echo "================================"
echo "API URL: $API_URL"
echo "Org ID: $ORG_ID"
echo ""

# Test non-streaming chat first
echo "1. Testing non-streaming chat..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$API_URL/api/v1/ai/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Current-Org: $ORG_ID" \
  -d '{
    "message": "Hello, this is a test message",
    "model": "gemini",
    "stream": false
  }')

HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS/d')

echo "Status: $HTTP_STATUS"
echo "Response:"
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
echo ""

if [ "$HTTP_STATUS" != "200" ]; then
    echo "❌ Chat API test failed!"
    echo ""
    echo "Common issues:"
    echo "1. No active subscription - Check /api/v1/billing/subscription"
    echo "2. Gemini API key not configured - Check backend/.env for GEMINI_API_KEY"
    echo "3. Invalid organization ID"
    echo "4. Rate limit exceeded"
    exit 1
fi

echo "✅ Chat API test passed!"
echo ""
echo "2. Testing streaming endpoint..."
echo "Note: Streaming test will show raw SSE output"
echo ""

curl -N -X POST "$API_URL/api/v1/ai/chat/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Current-Org: $ORG_ID" \
  -d '{
    "message": "Say hello",
    "model": "gemini",
    "stream": true
  }' 2>&1 | head -20

echo ""
echo "✅ Streaming test complete!"
