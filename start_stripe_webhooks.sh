#!/bin/bash

echo "🔗 Starting Stripe webhook forwarding..."
echo "========================================"
echo ""
echo "This will forward Stripe webhooks to your local backend"
echo "Make sure your backend is running on http://localhost:8000"
echo ""

# Forward webhooks to local backend
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe

# The webhook signing secret will be displayed
# Copy it and update your backend/.env file:
# STRIPE_WEBHOOK_SECRET=whsec_xxxxx
