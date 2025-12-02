# 💳 Stripe Integration Setup Guide

## 📋 مراحل راه‌اندازی Stripe

### 1️⃣ **ساخت حساب Stripe**

1. برو به https://dashboard.stripe.com/register
2. حساب بساز (Test mode)
3. API Keys رو پیدا کن: https://dashboard.stripe.com/apikeys

---

### 2️⃣ **ساخت Products و Prices**

#### در Stripe Dashboard:

**Product 1: Pro Plan**
```
Name: Pro Plan
Description: Professional features for growing teams
Price: $29/month
Billing: Recurring - Monthly
```
بعد از ساخت، Price ID رو کپی کن (مثلاً: `price_1ABC123xyz`)

**Product 2: Team Plan**
```
Name: Team Plan
Description: Advanced features for large teams
Price: $99/month
Billing: Recurring - Monthly
```
Price ID رو کپی کن (مثلاً: `price_1DEF456xyz`)

---

### 3️⃣ **تنظیم Environment Variables**

در فایل `backend/.env`:

```env
# Stripe Keys (از Dashboard)
STRIPE_SECRET_KEY=sk_test_51ABC...
STRIPE_PUBLISHABLE_KEY=pk_test_51ABC...
STRIPE_WEBHOOK_SECRET=whsec_...  # بعداً تنظیم می‌کنیم
```

---

### 4️⃣ **تنظیم Price IDs در کد**

در فایل `backend/app/core/stripe_config.py`:

```python
STRIPE_PRICES = {
    PlanType.FREE: None,
    PlanType.PRO: "price_1ABC123xyz",  # ← Price ID از Stripe
    PlanType.TEAM: "price_1DEF456xyz",  # ← Price ID از Stripe
}
```

---

### 5️⃣ **تنظیم Webhooks**

#### روش 1: استفاده از Stripe CLI (برای Development)

```bash
# نصب Stripe CLI
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.0/stripe_1.19.0_linux_x86_64.tar.gz
tar -xvf stripe_1.19.0_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/

# Login
stripe login

# Forward webhooks به local
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe

# کپی کن webhook signing secret که نمایش داده میشه
# مثلاً: whsec_abc123...
```

#### روش 2: تنظیم Webhook در Dashboard (برای Production)

1. برو به: https://dashboard.stripe.com/webhooks
2. کلیک "Add endpoint"
3. URL: `https://yourdomain.com/api/v1/billing/webhook/stripe`
4. Events انتخاب کن:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Signing secret رو کپی کن

---

### 6️⃣ **اجرای Migration**

```bash
docker-compose exec backend alembic upgrade head
```

---

## 🧪 تست کردن

### 1. دریافت لیست Plans

```bash
curl http://localhost:8000/api/v1/billing/plans | jq
```

Response:
```json
[
  {
    "name": "Free",
    "type": "free",
    "price": "0",
    "currency": "usd",
    "interval": "month",
    "features": ["1 organization", "5 team members", ...]
  },
  {
    "name": "Pro",
    "type": "pro",
    "price": "29",
    "currency": "usd",
    "interval": "month",
    "features": ["3 organizations", "20 team members", ...]
  },
  {
    "name": "Team",
    "type": "team",
    "price": "99",
    "currency": "usd",
    "interval": "month",
    "features": ["Unlimited organizations", ...]
  }
]
```

---

### 2. ساخت Checkout Session

```bash
# Login و گرفتن token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@test.com&password=pass123" | jq -r '.access_token')

# ساخت سازمان
ORG_ID=$(curl -s -X POST http://localhost:8000/api/v1/orgs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Org","slug":"test-org"}' | jq -r '.id')

# ساخت checkout session
curl -X POST http://localhost:8000/api/v1/billing/checkout \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "pro",
    "success_url": "http://localhost:3000/success",
    "cancel_url": "http://localhost:3000/cancel"
  }' | jq
```

Response:
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_...",
  "session_id": "cs_test_..."
}
```

---

### 3. تست Webhook (با Stripe CLI)

```bash
# در یک terminal
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe

# در terminal دیگه، trigger کن
stripe trigger checkout.session.completed
```

---

### 4. مشاهده Subscription

```bash
curl http://localhost:8000/api/v1/billing/subscription \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" | jq
```

---

## 🎯 API Endpoints

### GET `/api/v1/billing/plans`
لیست همه plan های موجود

**Response:**
```json
[
  {
    "name": "Pro",
    "type": "pro",
    "price": "29",
    "currency": "usd",
    "interval": "month",
    "features": [...],
    "stripe_price_id": "price_..."
  }
]
```

---

### GET `/api/v1/billing/subscription`
دریافت subscription فعلی سازمان

**Headers:**
- `Authorization: Bearer <token>`
- `X-Current-Org: <org_id>`

**Response:**
```json
{
  "id": 1,
  "organization_id": 1,
  "plan_type": "pro",
  "status": "active",
  "amount": "29.00",
  "currency": "usd",
  "current_period_start": "2024-12-01T00:00:00Z",
  "current_period_end": "2025-01-01T00:00:00Z",
  "cancel_at_period_end": false,
  "created_at": "2024-12-01T00:00:00Z"
}
```

---

### POST `/api/v1/billing/checkout`
ساخت Stripe checkout session

**Headers:**
- `Authorization: Bearer <token>`
- `X-Current-Org: <org_id>`

**Body:**
```json
{
  "plan_type": "pro",
  "success_url": "http://localhost:3000/success",
  "cancel_url": "http://localhost:3000/cancel"
}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_test_..."
}
```

---

### POST `/api/v1/billing/portal`
ساخت customer portal session

**Headers:**
- `Authorization: Bearer <token>`
- `X-Current-Org: <org_id>`

**Body:**
```json
{
  "return_url": "http://localhost:3000/settings"
}
```

**Response:**
```json
{
  "portal_url": "https://billing.stripe.com/..."
}
```

---

### POST `/api/v1/billing/webhook/stripe`
Webhook endpoint برای Stripe events

**⚠️ این endpoint باید public باشه (بدون authentication)**

**Headers:**
- `stripe-signature: <signature>`

**Events:**
- `checkout.session.completed` - پرداخت موفق
- `customer.subscription.updated` - تغییر subscription
- `customer.subscription.deleted` - لغو subscription
- `invoice.paid` - پرداخت invoice
- `invoice.payment_failed` - خطا در پرداخت

---

## 🔒 محدود کردن Features بر اساس Plan

### استفاده از Dependency

```python
from fastapi import APIRouter, Depends
from app.dependencies import require_pro_plan, require_team_plan

router = APIRouter()

@router.get("/premium-feature")
async def premium_feature(
    subscription = Depends(require_pro_plan)
):
    """این feature فقط برای Pro و Team"""
    return {"message": "Welcome to premium feature!"}

@router.get("/team-only-feature")
async def team_only_feature(
    subscription = Depends(require_team_plan)
):
    """این feature فقط برای Team"""
    return {"message": "Welcome to team feature!"}
```

---

### استفاده از Decorator

```python
from app.dependencies import requires_plan
from app.models.subscription import PlanType

@router.get("/advanced-analytics")
@requires_plan(PlanType.PRO, PlanType.TEAM)
async def advanced_analytics(
    db: AsyncSession = Depends(get_db),
    current_org: Organization = Depends(get_current_organization)
):
    """فقط Pro و Team می‌تونن ببینن"""
    return {"analytics": "..."}
```

---

## 📊 Plan Limits

در `backend/app/core/stripe_config.py`:

```python
PLAN_LIMITS = {
    PlanType.FREE: {
        "max_organizations": 1,
        "max_members_per_org": 5,
        "max_api_keys": 2,
        "api_rate_limit": 100,  # per hour
    },
    PlanType.PRO: {
        "max_organizations": 3,
        "max_members_per_org": 20,
        "max_api_keys": 10,
        "api_rate_limit": 1000,
    },
    PlanType.TEAM: {
        "max_organizations": None,  # Unlimited
        "max_members_per_org": None,
        "max_api_keys": None,
        "api_rate_limit": 10000,
    }
}
```

### چک کردن Limits

```python
from app.core.stripe_config import get_plan_limit

# مثال: چک کردن تعداد اعضا
max_members = get_plan_limit(subscription.plan_type, "max_members_per_org")
if max_members and current_members >= max_members:
    raise HTTPException(
        status_code=403,
        detail=f"Upgrade to add more members (limit: {max_members})"
    )
```

---

## 🎨 جریان کامل

```
1. کاربر لیست plans رو می‌بینه
   GET /billing/plans

2. Plan انتخاب می‌کنه و checkout می‌زنه
   POST /billing/checkout
   → Redirect به Stripe

3. پرداخت می‌کنه در Stripe

4. Stripe webhook می‌فرسته
   POST /webhook/stripe
   Event: checkout.session.completed

5. Backend subscription رو update می‌کنه
   - plan_type = "pro"
   - status = "active"
   - current_period_end = ...

6. کاربر به success_url redirect میشه

7. حالا می‌تونه از premium features استفاده کنه!
```

---

## 🧪 Test Cards

برای تست در Stripe Test Mode:

```
موفق: 4242 4242 4242 4242
خطا: 4000 0000 0000 0002
نیاز به 3D Secure: 4000 0025 0000 3155

CVV: هر 3 رقمی
تاریخ: هر تاریخ آینده
```

---

## 🚨 نکات مهم

1. **Webhook Secret**: حتماً تنظیم کن وگرنه webhooks کار نمی‌کنن
2. **Test Mode**: اول همه چیز رو در test mode تست کن
3. **Error Handling**: همیشه خطاهای Stripe رو handle کن
4. **Idempotency**: Stripe خودش idempotent هست
5. **Metadata**: از metadata استفاده کن برای track کردن

---

سوال داری؟ 😊
