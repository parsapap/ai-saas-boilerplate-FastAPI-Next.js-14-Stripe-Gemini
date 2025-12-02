# 🏢 Multi-Tenant & API Key Guide

## معماری Multi-Tenant

### مفاهیم کلیدی

```
User (کاربر)
  ↓ عضو در
Organization (سازمان)
  ↓ دارای
Membership (عضویت) + Role (نقش)
  ↓ می‌تواند بسازد
API Keys (کلیدهای API)
```

---

## 📊 ساختار دیتابیس

### 1. Organizations (سازمان‌ها)
```sql
organizations
├── id
├── name              # نام سازمان
├── slug              # شناسه یونیک (my-company)
├── description
├── is_active
├── stripe_customer_id
├── created_at
└── updated_at
```

### 2. Memberships (عضویت‌ها)
```sql
memberships
├── id
├── user_id           # کاربر
├── organization_id   # سازمان
├── role              # owner | admin | member
├── is_active
├── invited_by        # چه کسی دعوت کرده
└── joined_at
```

### 3. API Keys (کلیدهای API)
```sql
api_keys
├── id
├── name              # نام کلید (Production API)
├── key_prefix        # sk-xxxxx (برای نمایش)
├── key_hash          # هش کامل کلید
├── organization_id   # متعلق به کدام سازمان
├── created_by        # چه کسی ساخته
├── last_used_at      # آخرین استفاده
├── is_active
├── created_at
└── expires_at        # تاریخ انقضا (اختیاری)
```

---

## 🎭 نقش‌ها (Roles)

### Owner (مالک)
- ✅ همه دسترسی‌ها
- ✅ حذف سازمان
- ✅ تغییر نقش اعضا
- ✅ حذف اعضا
- ✅ دعوت اعضا

### Admin (ادمین)
- ✅ دعوت اعضا
- ✅ حذف اعضا (غیر از owner)
- ✅ ویرایش سازمان
- ✅ مدیریت API keys
- ❌ تغییر نقش owner

### Member (عضو)
- ✅ مشاهده اطلاعات سازمان
- ✅ مشاهده اعضا
- ✅ استفاده از API keys
- ❌ دعوت اعضا
- ❌ حذف اعضا

---

## 🔐 دو روش احراز هویت

### 1️⃣ JWT Token (برای کاربران)
```bash
# Login
POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "secret"
}

# Response
{
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi...",
  "token_type": "bearer"
}

# استفاده
GET /api/v1/orgs
Header: Authorization: Bearer eyJ0eXAi...
Header: X-Current-Org: my-company  # یا ID سازمان
```

### 2️⃣ API Key (برای برنامه‌ها)
```bash
# ساخت API Key
POST /api/v1/apikeys
Header: Authorization: Bearer eyJ0eXAi...
Header: X-Current-Org: my-company
{
  "name": "Production API",
  "expires_at": "2025-12-31T23:59:59Z"  # اختیاری
}

# Response (فقط یک بار نمایش داده میشه!)
{
  "id": 1,
  "name": "Production API",
  "key": "sk-abc123xyz...",  # ⚠️ ذخیره کن!
  "key_prefix": "sk-abc12",
  "organization_id": 1,
  "created_at": "2024-12-02T10:00:00Z"
}

# استفاده
GET /api/v1/users/me
Header: X-API-Key: sk-abc123xyz...
# نیازی به X-Current-Org نیست، از API key مشخص میشه
```

---

## 📝 API Endpoints

### Organizations

#### ساخت سازمان
```bash
POST /api/v1/orgs
Header: Authorization: Bearer <token>
{
  "name": "شرکت من",
  "slug": "my-company",
  "description": "توضیحات"
}
```

#### لیست سازمان‌های من
```bash
GET /api/v1/orgs
Header: Authorization: Bearer <token>

# Response
[
  {
    "id": 1,
    "name": "شرکت من",
    "slug": "my-company",
    "user_role": "owner",  # نقش شما
    "created_at": "..."
  }
]
```

#### دعوت عضو
```bash
POST /api/v1/orgs/1/invite
Header: Authorization: Bearer <token>
Header: X-Current-Org: 1
{
  "email": "colleague@example.com",
  "role": "admin"  # owner | admin | member
}
```

#### لیست اعضا
```bash
GET /api/v1/orgs/1/members
Header: Authorization: Bearer <token>
Header: X-Current-Org: 1

# Response
[
  {
    "id": 1,
    "user_email": "owner@example.com",
    "user_name": "علی احمدی",
    "role": "owner",
    "joined_at": "..."
  },
  {
    "id": 2,
    "user_email": "colleague@example.com",
    "user_name": "سارا رضایی",
    "role": "admin",
    "joined_at": "..."
  }
]
```

#### تغییر نقش عضو (فقط owner)
```bash
PATCH /api/v1/orgs/1/members/2
Header: Authorization: Bearer <token>
Header: X-Current-Org: 1
{
  "role": "member"
}
```

#### حذف عضو
```bash
DELETE /api/v1/orgs/1/members/2
Header: Authorization: Bearer <token>
Header: X-Current-Org: 1
```

---

### API Keys

#### ساخت API Key
```bash
POST /api/v1/apikeys
Header: Authorization: Bearer <token>
Header: X-Current-Org: my-company
{
  "name": "Production API",
  "expires_at": null  # یا تاریخ انقضا
}

# ⚠️ کلید فقط یک بار نمایش داده میشه!
```

#### لیست API Keys
```bash
GET /api/v1/apikeys
Header: Authorization: Bearer <token>
Header: X-Current-Org: my-company

# Response
[
  {
    "id": 1,
    "name": "Production API",
    "key_prefix": "sk-abc12",  # فقط پیشوند
    "last_used_at": "2024-12-02T10:30:00Z",
    "is_active": true,
    "created_at": "..."
  }
]
```

#### غیرفعال کردن API Key
```bash
DELETE /api/v1/apikeys/1
Header: Authorization: Bearer <token>
Header: X-Current-Org: my-company
```

#### حذف دائمی API Key
```bash
DELETE /api/v1/apikeys/1/permanent
Header: Authorization: Bearer <token>
Header: X-Current-Org: my-company
```

---

## 🔄 جریان کامل

### سناریو 1: ساخت سازمان و دعوت تیم

```bash
# 1. کاربر لاگین می‌کنه
POST /api/v1/auth/login
→ دریافت access_token

# 2. سازمان می‌سازه (خودکار owner میشه)
POST /api/v1/orgs
{
  "name": "استارتاپ من",
  "slug": "my-startup"
}
→ organization_id: 1

# 3. همکار رو دعوت می‌کنه
POST /api/v1/orgs/1/invite
Header: X-Current-Org: 1
{
  "email": "developer@example.com",
  "role": "admin"
}

# 4. لیست اعضا رو می‌بینه
GET /api/v1/orgs/1/members
Header: X-Current-Org: 1
```

### سناریو 2: ساخت و استفاده از API Key

```bash
# 1. API Key می‌سازه
POST /api/v1/apikeys
Header: X-Current-Org: my-startup
{
  "name": "Backend Service"
}
→ key: "sk-abc123xyz..."  # ⚠️ ذخیره کن!

# 2. از API key استفاده می‌کنه (بدون JWT)
GET /api/v1/users/me
Header: X-API-Key: sk-abc123xyz...
→ موفق! (سازمان از API key مشخص میشه)

# 3. چک می‌کنه کی استفاده شده
GET /api/v1/apikeys
Header: X-Current-Org: my-startup
→ last_used_at: "2024-12-02T11:00:00Z"
```

---

## 🛡️ امنیت

### API Key Security

1. **هش شده ذخیره میشه**: کلید کامل هرگز تو دیتابیس ذخیره نمیشه
2. **فقط یک بار نمایش**: وقتی می‌سازی فقط یک بار نشون داده میشه
3. **Prefix برای شناسایی**: `sk-abc12` برای اینکه بدونی کدوم کلیده
4. **تاریخ انقضا**: می‌تونی expiration تنظیم کنی
5. **Last used tracking**: می‌بینی آخرین بار کی استفاده شده

### Permission Checks

```python
# در کد، چک می‌کنیم:
- آیا کاربر عضو سازمان هست؟
- آیا نقش کافی داره؟
- آیا سازمان فعال هست؟
- آیا API key منقضی نشده؟
```

---

## 💡 Use Cases

### 1. SaaS با تیم‌های مختلف
```
شرکت A
├── Owner: مدیر
├── Admin: CTO
└── Members: توسعه‌دهندگان

شرکت B
├── Owner: بنیان‌گذار
└── Members: فریلنسرها
```

### 2. API Keys برای سرویس‌ها
```
سازمان: استارتاپ من
├── Production API (sk-prod...)
├── Staging API (sk-stag...)
└── Development API (sk-dev...)
```

### 3. Multi-tenant SaaS
```
هر مشتری = یک Organization
هر کارمند مشتری = یک Membership
هر سرویس مشتری = یک API Key
```

---

## 🧪 تست

```bash
# 1. ثبت‌نام دو کاربر
POST /api/v1/auth/register
{
  "email": "owner@test.com",
  "password": "pass123",
  "full_name": "Owner"
}

POST /api/v1/auth/register
{
  "email": "member@test.com",
  "password": "pass123",
  "full_name": "Member"
}

# 2. Owner لاگین و سازمان می‌سازه
POST /api/v1/auth/login
→ token_owner

POST /api/v1/orgs
Header: Authorization: Bearer <token_owner>
{
  "name": "Test Org",
  "slug": "test-org"
}

# 3. Member رو دعوت می‌کنه
POST /api/v1/orgs/1/invite
Header: Authorization: Bearer <token_owner>
Header: X-Current-Org: 1
{
  "email": "member@test.com",
  "role": "member"
}

# 4. Member لاگین و سازمان‌هاش رو می‌بینه
POST /api/v1/auth/login
→ token_member

GET /api/v1/orgs
Header: Authorization: Bearer <token_member>
→ [{"name": "Test Org", "user_role": "member"}]

# 5. API Key می‌سازه
POST /api/v1/apikeys
Header: Authorization: Bearer <token_owner>
Header: X-Current-Org: 1
{
  "name": "Test Key"
}
→ key: "sk-xyz..."

# 6. با API Key تست می‌کنه
GET /api/v1/users/me
Header: X-API-Key: sk-xyz...
→ موفق!
```

---

## 📚 نکات مهم

1. **X-Current-Org header**: برای JWT باید سازمان فعلی رو مشخص کنی
2. **API Key**: خودش سازمان رو مشخص می‌کنه، نیازی به header نیست
3. **Owner protection**: آخرین owner رو نمی‌تونی حذف کنی
4. **Cascade delete**: وقتی سازمان حذف میشه، همه memberships و API keys هم حذف میشن
5. **Invite existing users**: فقط کاربرهایی که قبلاً ثبت‌نام کردن رو می‌تونی دعوت کنی

---

سوال داری؟ 😊
