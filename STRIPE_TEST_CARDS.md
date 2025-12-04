# Stripe Test Payment Guide

## Test Card Numbers

When testing Stripe payments in test mode, use these card numbers:

### ✅ Successful Payment
- **Card Number**: `4242 4242 4242 4242`
- **Expiry**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### ❌ Card Declined
- **Card Number**: `4000 0000 0000 0002`
- Use this to test payment failures

### 🔐 Requires Authentication (3D Secure)
- **Card Number**: `4000 0025 0000 3155`
- Use this to test 3D Secure authentication flow

### 💳 Other Test Cards
- **Insufficient Funds**: `4000 0000 0000 9995`
- **Expired Card**: `4000 0000 0000 0069`
- **Incorrect CVC**: `4000 0000 0000 0127`

## How to Test Payment Flow

1. **Start your backend and frontend**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Make sure Stripe is configured**:
   - Check `.env` has `STRIPE_SECRET_KEY` (test key starting with `sk_test_`)
   - Check `.env` has `STRIPE_WEBHOOK_SECRET`

3. **Test the flow**:
   - Login to your app
   - Create an organization (if you haven't)
   - Go to `/pricing`
   - Click "Subscribe Now" on Pro or Team plan
   - Use test card: `4242 4242 4242 4242`
   - Complete the checkout
   - You'll be redirected back with success message

4. **Verify subscription**:
   - Go to `/billing` page
   - You should see your active subscription
   - Check Stripe Dashboard: https://dashboard.stripe.com/test/subscriptions

## Testing Webhooks Locally

To test webhooks on localhost, use Stripe CLI:

```bash
# Install Stripe CLI
# Mac: brew install stripe/stripe-cli/stripe
# Linux: Download from https://github.com/stripe/stripe-cli/releases

# Login to Stripe
stripe login

# Forward webhooks to your local server
stripe listen --forward-to localhost:8000/api/v1/billing/webhook

# This will give you a webhook secret starting with whsec_
# Add it to your .env file as STRIPE_WEBHOOK_SECRET
```

## Checking Test Mode

Make sure you're in test mode:
- Stripe Dashboard should show "TEST MODE" toggle in top right
- API keys should start with `sk_test_` and `pk_test_`
- Test data won't affect real customers or charges

## Common Issues

1. **"No such price"** - Make sure you've created products/prices in Stripe Dashboard
2. **"Invalid API key"** - Check your `.env` has the correct test key
3. **Webhook not working** - Use Stripe CLI to forward webhooks locally
4. **Payment succeeds but subscription not created** - Check webhook is configured correctly

## Next Steps After Testing

Once testing works:
1. Get production API keys from Stripe
2. Update `.env` with production keys
3. Configure production webhook endpoint
4. Test with real card (small amount)
5. Go live! 🚀
