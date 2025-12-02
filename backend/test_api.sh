#!/bin/bash

API_URL="http://localhost:8000"

echo "🧪 Testing FastAPI SaaS API..."
echo ""

# Test health endpoint
echo "1️⃣ Testing health endpoint..."
HEALTH=$(curl -s "$API_URL/health")
echo "Response: $HEALTH"
echo ""

# Test root endpoint
echo "2️⃣ Testing root endpoint..."
ROOT=$(curl -s "$API_URL/")
echo "Response: $ROOT"
echo ""

# Test register
echo "3️⃣ Testing user registration..."
REGISTER=$(curl -s -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }')
echo "Response: $REGISTER"
echo ""

# Test login
echo "4️⃣ Testing user login..."
LOGIN=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=TestPass123!")
echo "Response: $LOGIN"
echo ""

# Extract access token
ACCESS_TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -n "$ACCESS_TOKEN" ]; then
    echo "5️⃣ Testing authenticated endpoint..."
    ME=$(curl -s -X GET "$API_URL/api/v1/users/me" \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    echo "Response: $ME"
    echo ""
    echo "✅ All tests passed!"
else
    echo "❌ Login failed - could not get access token"
fi

echo ""
echo "📚 View full API docs at: $API_URL/docs"
