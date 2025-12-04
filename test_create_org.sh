#!/bin/bash

# Test create organization endpoint
# Usage: ./test_create_org.sh <access_token>

if [ -z "$1" ]; then
    echo "Usage: ./test_create_org.sh <access_token>"
    echo "Get your access token from localStorage in browser console:"
    echo "  localStorage.getItem('access_token')"
    exit 1
fi

TOKEN=$1
API_URL=${API_URL:-http://localhost:8000}

echo "Testing Create Organization..."
echo "================================"

# Create organization
echo -e "\n1. Creating organization..."
RESPONSE=$(curl -s -X POST "$API_URL/api/v1/organizations/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Organization",
    "slug": "test-org-'$(date +%s)'",
    "description": "Test organization created via script"
  }')

echo "Response:"
echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

# Extract org ID
ORG_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)

if [ "$ORG_ID" != "null" ] && [ -n "$ORG_ID" ]; then
    echo -e "\n✅ Organization created successfully! ID: $ORG_ID"
    
    # List organizations
    echo -e "\n2. Listing all organizations..."
    curl -s -X GET "$API_URL/api/v1/organizations/" \
      -H "Authorization: Bearer $TOKEN" | jq '.' 2>/dev/null
else
    echo -e "\n❌ Failed to create organization"
fi
