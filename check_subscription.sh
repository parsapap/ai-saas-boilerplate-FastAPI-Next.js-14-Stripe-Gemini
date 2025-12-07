#!/bin/bash

# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=chattest@example.com&password=Test123%21%40%23" | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:20}..."
echo ""

# Get subscription
echo "Checking subscription for Org ID 2:"
echo "=================================="
curl -s -X GET http://localhost:8000/api/v1/billing/subscription \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 2" | python3 -m json.tool

echo ""
echo ""
echo "Checking Stripe webhook logs:"
echo "=================================="
# Check recent logs for webhook events
tail -50 backend/logs/*.log 2>/dev/null | grep -i "stripe\|webhook\|subscription" | tail -20 || echo "No logs found"
