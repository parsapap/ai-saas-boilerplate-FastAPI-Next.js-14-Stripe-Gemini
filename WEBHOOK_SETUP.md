# Stripe Webhook Setup Guide

## Problem
Your subscription shows as "free" even after paying because Stripe webhooks are not reaching your local backend.

## Why This Happens
- Your backend runs on `localhost:8000` (not accessible from internet)
- Stripe needs a public URL to send webhook events
- Without webhooks, your database doesn't get updated when payments succeed

## Solution 1: Use Stripe CLI (Recommended for Local Development)

### Step 1: Start Webhook Forwarding
```bash
./start_stripe_webhooks.sh
```

Or manually:
```bash
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe
```

### Step 2: Copy the Webhook Secret
The CLI will display something like:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

### Step 3: Update Backend Environment
```bash
# Edit backend/.env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### Step 4: Restart Backend
```bash
# The backend should auto-reload if using --reload flag
# Or manually restart it
```

### Step 5: Test Payment
1. Go to your frontend billing page
2. Click "Upgrade to Pro"
3. Use test card: `4242 4242 4242 4242`
4. Complete payment
5. Check the Stripe CLI terminal - you should see webhook events
6. Your subscription should now show as "pro"

## Solution 2: Use ngrok (Alternative)

### Step 1: Install ngrok
```bash
# Download from https://ngrok.com/download
# Or use snap
sudo snap install ngrok
```

### Step 2: Start ngrok
```bash
ngrok http 8000
```

### Step 3: Configure Stripe Webhook
1. Go to https://dashboard.stripe.com/test/webhooks
2. Click "Add endpoint"
3. Enter ngrok URL: `https://xxxx.ngrok.io/api/v1/billing/webhook/stripe`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the webhook secret
6. Update `backend/.env` with the secret

## Solution 3: Manual Database Fix (Quick Fix)

If you just want to test and don't care about webhooks right now:

### Option A: Use Admin Panel
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Find your subscription
4. Change `plan_type` to `pro` or `team`
5. Save

### Option B: Run Fix Script
```bash
python3 fix_subscription.py
```
Follow the prompts and then run the SQL command it provides.

### Option C: Direct SQL
```bash
# Connect to your database
psql -U postgres -d ai_saas

# Update subscription
UPDATE subscriptions SET plan_type = 'pro' WHERE organization_id = 2;
```

## Solution 4: Deploy to Production

Once deployed to Railway/Heroku/etc:
1. Your backend will have a public URL
2. Configure Stripe webhook with that URL
3. Webhooks will work automatically

## Verify Webhooks Are Working

### Check Stripe CLI Output
You should see events like:
```
2025-12-07 20:00:00   --> checkout.session.completed [evt_xxx]
2025-12-07 20:00:01   <--  [200] POST http://localhost:8000/api/v1/billing/webhook/stripe
```

### Check Backend Logs
Look for:
```
INFO: Received Stripe webhook: checkout.session.completed
INFO: Checkout completed for org 2, plan: pro
```

### Check Database
```bash
./check_subscription.sh
```

Should show:
```json
{
    "plan_type": "pro",
    "status": "active"
}
```

## Troubleshooting

### Webhook Returns 400 "Invalid signature"
- Make sure `STRIPE_WEBHOOK_SECRET` in `.env` matches the one from Stripe CLI
- Restart your backend after updating `.env`

### Webhook Returns 500 Error
- Check backend logs for errors
- Make sure database is running
- Check if organization exists

### Plan Still Shows as Free
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check if webhook was actually received (Stripe CLI output)
- Verify database was updated

### Stripe CLI Not Forwarding
- Make sure backend is running on port 8000
- Check if another process is using the port
- Try restarting Stripe CLI

## Production Checklist

- [ ] Deploy backend to public URL
- [ ] Configure Stripe webhook with production URL
- [ ] Use production Stripe keys
- [ ] Test payment flow end-to-end
- [ ] Monitor webhook delivery in Stripe dashboard
- [ ] Set up webhook retry logic
- [ ] Add webhook event logging

## Resources

- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Testing Webhooks Locally](https://stripe.com/docs/webhooks/test)
