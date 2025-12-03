# 🚀 Stripe Configuration Guide

## ✅ Current Status
- ✅ Stripe API keys configured in `.env`
- ⚠️ Need to create products and get Price IDs
- ⚠️ Need to configure webhook

---

## 📝 Step-by-Step Setup

### Step 1: Create Products in Stripe Dashboard

1. **Go to Stripe Dashboard**: https://dashboard.stripe.com/test/products

2. **Create Pro Plan Product**:
   - Click "Add product"
   - Name: `Pro Plan`
   - Description: `Professional features for growing teams`
   - Pricing:
     - Price: `$29.00`
     - Billing period: `Monthly`
     - Currency: `USD`
   - Click "Save product"
   - **Copy the Price ID** (starts with `price_...`)

3. **Create Team Plan Product**:
   - Click "Add product"
   - Name: `Team Plan`
   - Description: `Advanced features for large teams`
   - Pricing:
     - Price: `$99.00`
     - Billing period: `Monthly`
     - Currency: `USD`
   - Click "Save product"
   - **Copy the Price ID** (starts with `price_...`)

---

### Step 2: Update Price IDs in Code

Edit `backend/app/core/stripe_config.py` and replace:

```python
STRIPE_PRICES = {
    PlanType.FREE: None,
    PlanType.PRO: "price_YOUR_PRO_PRICE_ID",    # ← Paste your Pro price ID here
    PlanType.TEAM: "price_YOUR_TEAM_PRICE_ID",  # ← Paste your Team price ID here
}
```

---

### Step 3: Setup Webhook (Choose One Method)

#### Option A: Using Stripe CLI (Recommended for Development)

1. **Install Stripe CLI**:
   ```bash
   # Download and install
   wget https://github.com/stripe/stripe-cli/releases/download/v1.19.0/stripe_1.19.0_linux_x86_64.tar.gz
   tar -xvf stripe_1.19.0_linux_x86_64.tar.gz
   sudo mv stripe /usr/local/bin/
   ```

2. **Login to Stripe**:
   ```bash
   stripe login
   ```

3. **Forward webhooks to local backend**:
   ```bash
   stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe
   ```

4. **Copy the webhook signing secret** (starts with `whsec_...`) and update `.env`:
   ```env
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   ```

#### Option B: Manual Webhook Setup (For Production)

1. Go to: https://dashboard.stripe.com/test/webhooks
2. Click "Add endpoint"
3. Endpoint URL: `http://localhost:8000/api/v1/billing/webhook/stripe` (or your domain)
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Click "Add endpoint"
6. Copy the "Signing secret" and update `.env`

---

### Step 4: Restart Backend

After updating the configuration, restart your backend:

```bash
# Stop the current backend process
# Then restart it
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Testing Your Setup

### 1. Test API Connection
```bash
curl http://localhost:8000/api/v1/billing/plans | jq
```

Expected: List of 3 plans (Free, Pro, Team)

### 2. Run Full Test Suite
```bash
chmod +x backend/test_stripe.sh
./backend/test_stripe.sh
```

### 3. Test Checkout Flow

1. The test script will output a checkout URL
2. Open it in your browser
3. Use Stripe test card: `4242 4242 4242 4242`
4. Complete the payment
5. Check if webhook updates the subscription

---

## 🎯 Quick Commands

```bash
# View available plans
curl http://localhost:8000/api/v1/billing/plans | jq

# Check Stripe CLI webhook forwarding
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe

# Trigger test webhook
stripe trigger checkout.session.completed

# View Stripe logs
stripe logs tail
```

---

## 🔑 Test Cards

Use these cards in Stripe test mode:

- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **3D Secure**: `4000 0025 0000 3155`

CVV: Any 3 digits  
Expiry: Any future date

---

## 📊 What You Have Now

✅ Stripe API keys configured  
✅ Backend running on port 8000  
✅ PostgreSQL and Redis running in Docker  
⏳ Need to create products and get Price IDs  
⏳ Need to setup webhook  

---

## 🆘 Need Help?

Run the test script to see detailed output:
```bash
./backend/test_stripe.sh
```

Check backend logs for errors:
```bash
# Backend is running in background, check process output
```

Check Stripe Dashboard:
- Products: https://dashboard.stripe.com/test/products
- Webhooks: https://dashboard.stripe.com/test/webhooks
- Logs: https://dashboard.stripe.com/test/logs
