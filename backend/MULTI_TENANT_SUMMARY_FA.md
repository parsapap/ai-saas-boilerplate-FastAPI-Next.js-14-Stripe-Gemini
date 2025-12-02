# 🏢 خلاصه قابلیت Multi-Tenant

## چی اضافه شد؟

### 1️⃣ **مدل‌های جدید**

#### Organization (سازمان)
```python
- id
- name: "شرکت من"
- slug: "my-company" (یونیک)
- description
- stripe_customer_id
```
**کاربرد**: هر مشتری/شرکت یه Organization هست

#### Membership (عضویت)
```python
- user_id → کاربر
- organization_id → سازمان
- role: owner | admin | member
- invited_by → چه کسی دعوت کرده
```
**کاربرد**: رابطه بین User و Organization

#### ApiKey (کلید API)
```python
- name: "Production API"
- key_prefix: "sk-abc12" (برای نمایش)
- key_hash: "..." (هش شده)
- organization_id → متعلق به کدام سازمان
- expires_at: تاریخ انقضا (اختیاری)
```
**کاربرد**: احراز هویت بدون JWT برای سرویس‌ها

---

## 2️⃣ **API Endpoints جدید**

### Organizations (`/api/v1/orgs`)

```bash
POST   /orgs                    # ساخت سازمان
GET    /orgs                    # لیست سازمان‌های من
GET    /orgs/{id}               # جزئیات سازمان
PATCH  /orgs/{id}               # ویرایش سازمان
POST   /orgs/{id}/invite        # دعوت عضو
GET    /orgs/{id}/members       # لیست اعضا
PATCH  /orgs/{id}/members/{uid} # تغییر نقش
DELETE /orgs/{id}/members/{uid} # حذف عضو
```

### API Keys (`/api/v1/apikeys`)

```bash
POST   /apikeys              # ساخت API key
GET    /apikeys              # لیست API keys
DELETE /apikeys/{id}         # غیرفعال کردن
DELETE /apikeys/{id}/permanent # حذف دائمی
```

---

## 3️⃣ **نقش‌ها (Roles)**

### 👑 Owner (مالک)
- همه کارها رو می‌تونه انجام بده
- تنها کسی که می‌تونه نقش‌ها رو تغییر بده
- نمی‌تونه خودش رو حذف کنه اگه تنها owner باشه

### 🛡️ Admin (ادمین)
- می‌تونه عضو دعوت کنه
- می‌تونه عضو حذف کنه (به جز owner)
- می‌تونه سازمان رو ویرایش کنه
- نمی‌تونه نقش owner رو تغییر بده

### 👤 Member (عضو)
- فقط می‌تونه ببینه
- نمی‌تونه تغییری بده

---

## 4️⃣ **دو روش احراز هویت**

### روش 1: JWT Token (برای کاربران)
```bash
# لاگین
POST /api/v1/auth/login
→ access_token

# استفاده
GET /api/v1/orgs
Header: Authorization: Bearer <token>
Header: X-Current-Org: my-company  # باید سازمان رو مشخص کنی
```

### روش 2: API Key (برای سرویس‌ها)
```bash
# ساخت
POST /api/v1/apikeys
Header: X-Current-Org: my-company
→ key: "sk-abc123..."  # فقط یک بار نشون داده میشه!

# استفاده
GET /api/v1/users/me
Header: X-API-Key: sk-abc123...
# نیازی به X-Current-Org نیست!
```

---

## 5️⃣ **جریان کار**

### سناریو: ساخت تیم

```
1. کاربر ثبت‌نام می‌کنه
   POST /auth/register

2. سازمان می‌سازه (خودکار owner میشه)
   POST /orgs
   {
     "name": "شرکت من",
     "slug": "my-company"
   }

3. همکارش رو دعوت می‌کنه
   POST /orgs/1/invite
   {
     "email": "colleague@test.com",
     "role": "admin"
   }

4. API key می‌سازه برای backend
   POST /apikeys
   {
     "name": "Production API"
   }
   → sk-abc123...

5. Backend با API key کار می‌کنه
   GET /users/me
   Header: X-API-Key: sk-abc123...
```

---

## 6️⃣ **امنیت**

### API Key Security
- ✅ هش SHA256 ذخیره میشه (نه خود کلید)
- ✅ فقط یک بار نمایش داده میشه
- ✅ Prefix برای شناسایی (sk-abc12)
- ✅ تاریخ انقضا (اختیاری)
- ✅ ردیابی آخرین استفاده

### Permission Checks
```python
# هر endpoint چک می‌کنه:
✓ آیا کاربر عضو سازمان هست؟
✓ آیا نقش کافی داره؟
✓ آیا سازمان فعال هست؟
✓ آیا API key معتبر هست؟
```

---

## 7️⃣ **ساختار دیتابیس**

```
users (کاربران)
  ↓ 1:N
memberships (عضویت‌ها)
  ↓ N:1
organizations (سازمان‌ها)
  ↓ 1:N
api_keys (کلیدهای API)
```

**مثال:**
```
User: علی احمدی
  ├─ Membership: شرکت A (owner)
  │   └─ API Keys: Production, Staging
  └─ Membership: شرکت B (member)
      └─ API Keys: Development
```

---

## 8️⃣ **Migration**

دو migration جدید:
- `001_initial_users.py` - جدول users
- `002_add_multi_tenant.py` - جداول organizations, memberships, api_keys

```bash
# اجرای migrations
docker-compose exec backend alembic upgrade head
```

---

## 9️⃣ **تست**

```bash
# تست خودکار
cd backend
./test_multi_tenant.sh

# یا دستی
curl -X POST http://localhost:8000/api/v1/orgs \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Test","slug":"test"}'
```

---

## 🎯 **Use Cases**

### 1. SaaS با چند تیم
```
کاربر: محمد
├─ سازمان: استارتاپ A (owner)
│  ├─ اعضا: 5 نفر
│  └─ API Keys: 3 تا
└─ سازمان: فریلنس B (member)
   ├─ اعضا: 2 نفر
   └─ API Keys: 1 تا
```

### 2. Agency با مشتری‌های مختلف
```
آژانس
├─ مشتری 1 (Organization)
│  ├─ تیم مشتری (members)
│  └─ تیم آژانس (admins)
└─ مشتری 2 (Organization)
   └─ ...
```

### 3. API-First Product
```
هر مشتری:
├─ یک Organization
├─ چند API Key برای محیط‌های مختلف
│  ├─ Production (sk-prod...)
│  ├─ Staging (sk-stag...)
│  └─ Development (sk-dev...)
└─ تیم توسعه (members)
```

---

## 📝 **نکات مهم**

1. **X-Current-Org header**: 
   - با JWT باید بفرستی
   - با API Key نیازی نیست

2. **API Key فقط یک بار نمایش داده میشه**:
   - وقتی می‌سازی ذخیره کن
   - بعداً فقط prefix رو می‌بینی

3. **Owner protection**:
   - آخرین owner رو نمی‌تونی حذف کنی
   - اول باید owner جدید تعیین کنی

4. **Cascade delete**:
   - وقتی سازمان حذف میشه
   - همه memberships و API keys هم حذف میشن

5. **Invite فقط کاربرهای موجود**:
   - کاربر باید قبلاً ثبت‌نام کرده باشه
   - نمی‌تونی ایمیل دعوت بفرستی (فعلاً)

---

## 🚀 **شروع سریع**

```bash
# 1. Run migrations
docker-compose exec backend alembic upgrade head

# 2. Test
cd backend && ./test_multi_tenant.sh

# 3. Check docs
http://localhost:8000/docs
```

---

سوال داری؟ فایل `MULTI_TENANT_GUIDE.md` رو ببین! 😊
