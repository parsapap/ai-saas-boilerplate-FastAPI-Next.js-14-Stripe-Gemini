#!/bin/bash
# Test user registration and login flow

echo "========================================="
echo "Testing User Registration & Login Flow"
echo "========================================="
echo ""

# Test 1: Register a new user
echo "1. Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "DemoPassword123!",
    "full_name": "Demo User"
  }')

echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""

# Check if registration was successful
if echo "$REGISTER_RESPONSE" | grep -q '"email"'; then
    echo "✓ Registration successful!"
else
    echo "✗ Registration failed!"
    if echo "$REGISTER_RESPONSE" | grep -q "already registered"; then
        echo "  User already exists - continuing with login test..."
    else
        exit 1
    fi
fi
echo ""

# Test 2: Login with the registered user
echo "2. Logging in with registered user..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=DemoPassword123!")

echo "$LOGIN_RESPONSE" | python3 -m json.tool
echo ""

# Extract access token
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$ACCESS_TOKEN" ]; then
    echo "✓ Login successful!"
    echo "  Access Token: ${ACCESS_TOKEN:0:50}..."
else
    echo "✗ Login failed!"
    exit 1
fi
echo ""

# Test 3: Access protected endpoint with token
echo "3. Accessing protected endpoint..."
ME_RESPONSE=$(curl -s -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "$ME_RESPONSE" | python3 -m json.tool
echo ""

if echo "$ME_RESPONSE" | grep -q '"email"'; then
    echo "✓ Protected endpoint access successful!"
else
    echo "✗ Protected endpoint access failed!"
    exit 1
fi
echo ""

echo "========================================="
echo "All tests passed! ✓"
echo "========================================="
