#!/bin/bash
# Test pricing page and Stripe integration

echo "========================================="
echo "Testing Pricing Page & Stripe Integration"
echo "========================================="
echo ""

# Test 1: Check if pricing page is accessible
echo "1. Testing pricing page accessibility..."
PRICING_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/pricing)

if [ "$PRICING_RESPONSE" = "200" ]; then
    echo "✓ Pricing page is accessible"
else
    echo "✗ Pricing page returned status: $PRICING_RESPONSE"
fi
echo ""

# Test 2: Check billing API endpoint
echo "2. Testing billing API endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✓ Backend is healthy"
else
    echo "✗ Backend is not responding"
fi
echo ""

# Test 3: Test checkout endpoint (requires auth)
echo "3. Testing checkout endpoint..."
echo "   (Requires authentication - login first)"

# Login
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=DemoPassword123!")

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo "✓ Successfully authenticated"
    
    # Test checkout endpoint
    CHECKOUT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/billing/checkout \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -H "X-Current-Org: 1" \
      -d '{
        "plan_type": "PRO",
        "success_url": "http://localhost:3000/pricing?status=success",
        "cancel_url": "http://localhost:3000/pricing?status=cancel"
      }' 2>&1)
    
    if echo "$CHECKOUT_RESPONSE" | grep -q "checkout_url"; then
        echo "✓ Checkout endpoint works"
        echo "   Checkout URL created successfully"
    else
        echo "✗ Checkout endpoint failed"
        echo "   Response: $CHECKOUT_RESPONSE"
    fi
else
    echo "✗ Authentication failed"
fi
echo ""

# Test 4: Check Stripe configuration
echo "4. Checking Stripe configuration..."
if grep -q "STRIPE_SECRET_KEY" backend/.env; then
    echo "✓ Stripe secret key configured"
else
    echo "✗ Stripe secret key not found"
fi

if grep -q "STRIPE_PUBLISHABLE_KEY" backend/.env; then
    echo "✓ Stripe publishable key configured"
else
    echo "✗ Stripe publishable key not found"
fi
echo ""

echo "========================================="
echo "Test Summary"
echo "========================================="
echo ""
echo "Frontend: http://localhost:3000/pricing"
echo "Backend: http://localhost:8000"
echo ""
echo "To test the full flow:"
echo "1. Visit http://localhost:3000/pricing"
echo "2. Click 'Subscribe Now' on Pro or Team plan"
echo "3. Login if not authenticated"
echo "4. Complete Stripe checkout"
echo ""
echo "Test Cards:"
echo "  Success: 4242 4242 4242 4242"
echo "  Decline: 4000 0000 0000 0002"
echo ""
