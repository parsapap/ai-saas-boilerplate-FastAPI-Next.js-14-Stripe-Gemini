# 💳 خلاصه Stripe Integration

## چی اضافه شد؟

### 1️⃣ **مدل Subscription**

```python
Subscription:
├── organization_id → متعلق به کدام سازمان
├── plan_type → free | pro | team
├── status → active | canceled | past_due | ...
├── stripe_subscription_id → ID در Stripe
├── amount → مبلغ ماهانه
├── current_period_end → تاریخ تمدید
└── cancel_at_period_end → آیا لغو شده؟
```

---

### 2️⃣ **3 Plan**

| Plan | قیمت | ویژگی‌ها |
|------|------|----------|
| **Free** | $0 | 1 سازمان، 5 عضو، ویژگی‌های پایه |
| **Pro** | $29/mo | 3 سازمان، 20 عضو، API access |
| **Team** | $99/mo | نامحدود، همه ویژگی‌ها، SLA |

---

### 3️⃣ **API Endpoints**

```bash
GET  /billing/plans              # لیست plans
GET  /billing/subscription       # subscription فعلی
POST /billing/checkout           # ساخت checkout session
POST /billing/portal             # customer portal
POST /billing/webhook/stripe     # webhook از Stripe
```

---

### 4️⃣ **Premium Features**

```bash
GET /premium/analytics      # نیاز به Pro یا Team
GET /premium/white-label    # نیاز به Team
GET /premium/free-feature   # برای همه
```

---

## 🔄 جریان کار

### سناریو: کاربر می‌خواد upgrade کنه

```
1. کاربر لیست plans رو می‌بینه
   GET /billing/plans
   → Free, Pro ($29), Team ($99)

2. Pro رو انتخاب می‌کنه
   POST /billing/checkout
   {
     "plan_type": "pro",
     "success_url": "...",
     "cancel_url": "..."
   }
   → checkout_url: "https://checkout.stripe.com/..."

3. به Stripe redirect میشه و پرداخت می‌کنه
   کارت تست: 4242 4242 4242 4242

4. Stripe webhook می‌فرسته
   POST /webhook/stripe
   Event: checkout.session.completed

5. Backend subscription رو update می‌کنه
   - plan_type = "pro"
   - status = "active"
   - amount = 29.00
   - current_period_end = ...

6. کاربر به success_url redirect میشه

7. حالا می‌تونه از Pro features استفاده کنه!
   GET /premium/analytics
   → ✅ موفق!
```

---

## 🛡️ محدود کردن Features

### روش 1: با Dependency

```python
from app.dependencies import require_pro_plan

@router.get("/analytics")
async def analytics(
    subscription = Depends(require_pro_plan)
):
    # فقط Pro و Team می‌تونن ببینن
    return {"data": "..."}
```

### روش 2: با Decorator

```python
from app.dependencies import requires_plan
from app.models.subscription import PlanType

@router.get("/white-label")
@requires_plan(PlanType.TEAM)
async def white_label(...):
    # فقط Team می‌تونه ببینه
    return {"settings": "..."}
```

---

## 📊 Plan Limits

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
        "max_organizations": None,  # نامحدود
        "max_members_per_org": None,
        "max_api_keys": None,
        "api_rate_limit": 10000,
    }
}
```

### استفاده:

```python
from app.core.stripe_config import get_plan_limit

max_members = get_plan_limit(subscription.plan_type, "max_members_per_org")
if max_members and current_members >= max_members:
    raise HTTPException(
        status_code=403,
        detail=f"Upgrade to add more members (limit: {max_members})"
    )
```

---

## 🎯 Webhook Events

### checkout.session.completed
```python
# وقتی پرداخت موفق شد
- Subscription رو بساز/update کن
- Plan رو تغییر بده
- کاربر رو notify کن
```

### customer.subscription.updated
```python
# وقتی subscription تغییر کرد
- Status رو update کن
- Period dates رو update کن
```

### customer.subscription.deleted
```python
# وقتی subscription لغو شد
- Plan رو به Free تغییر بده
- Status رو canceled کن
```

### invoice.paid
```python
# وقتی invoice پرداخت شد
- Log کن
- Receipt بفرست
```

### invoice.payment_failed
```python
# وقتی پرداخت fail شد
- Status رو past_due کن
- کاربر رو notify کن
```

---

## 🔧 تنظیمات

### 1. Stripe Dashboard

```
1. Products بساز:
   - Pro Plan: $29/month
   - Team Plan: $99/month

2. Price IDs رو کپی کن:
   - price_1ABC123xyz (Pro)
   - price_1DEF456xyz (Team)

3. Webhook بساز:
   URL: https://yourdomain.com/api/v1/billing/webhook/stripe
   Events: checkout.session.completed, ...
```

### 2. Environment Variables

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. کد

```python
# backend/app/core/stripe_config.py
STRIPE_PRICES = {
    PlanType.PRO: "price_1ABC123xyz",
    PlanType.TEAM: "price_1DEF456xyz",
}
```

---

## 🧪 تست

### 1. با اسکریپت

```bash
cd backend
./test_stripe.sh
```

### 2. دستی

```bash
# لیست plans
curl http://localhost:8000/api/v1/billing/plans

# ساخت checkout
curl -X POST http://localhost:8000/api/v1/billing/checkout \
  -H "Authorization: Bearer <token>" \
  -H "X-Current-Org: 1" \
  -d '{"plan_type":"pro","success_url":"...","cancel_url":"..."}'

# تست webhook (با Stripe CLI)
stripe listen --forward-to localhost:8000/api/v1/billing/webhook/stripe
stripe trigger checkout.session.completed
```

### 3. کارت‌های تست

```
موفق: 4242 4242 4242 4242
خطا: 4000 0000 0000 0002
3D Secure: 4000 0025 0000 3155
```

---

## 💡 Use Cases

### 1. SaaS با Freemium Model

```
Free → محدودیت دارد
Pro → ویژگی‌های بیشتر
Team → نامحدود + support
```

### 2. API Platform

```
Free → 100 requests/hour
Pro → 1000 requests/hour
Team → 10000 requests/hour
```

### 3. Collaboration Tool

```
Free → 5 team members
Pro → 20 team members
Team → Unlimited
```

---

## 🚨 نکات مهم

1. **Webhook Secret**: حتماً تنظیم کن
2. **Test Mode**: اول همه چیز رو تست کن
3. **Error Handling**: خطاهای Stripe رو handle کن
4. **Idempotency**: Stripe خودش idempotent هست
5. **Metadata**: برای track کردن استفاده کن
6. **Customer Portal**: به کاربر بده برای مدیریت subscription

---

## 📚 فایل‌های مرتبط

- `backend/app/models/subscription.py` - مدل
- `backend/app/api/v1/billing.py` - endpoints
- `backend/app/core/stripe_config.py` - تنظیمات
- `backend/app/dependencies.py` - plan requirements
- `backend/STRIPE_SETUP_GUIDE.md` - راهنمای کامل

---

سوال داری؟ فایل `STRIPE_SETUP_GUIDE.md` رو ببین! 😊
