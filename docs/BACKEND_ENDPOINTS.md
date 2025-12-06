# Backend API Endpoints - Complete List

## Base URL
```
http://localhost:8000
```

## 📚 Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## ✅ AUTHENTICATION (`/api/v1/auth`)

### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```
**Response**: User object with Stripe customer ID

### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123!
```
**Response**: Access token + Refresh token

### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGci..."
}
```
**Response**: New access token + refresh token

---

## ✅ USERS (`/api/v1/users`)

### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer {access_token}
```
**Response**: Current user information

---

## ✅ BILLING (`/api/v1/billing`)

### Get Available Plans
```http
GET /api/v1/billing/plans
```
**Response**: List of all subscription plans (Free, Pro, Team)

### Get Current Subscription
```http
GET /api/v1/billing/subscription
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: Current subscription details

### Create Checkout Session
```http
POST /api/v1/billing/checkout
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "plan_type": "PRO",
  "success_url": "http://localhost:3000/pricing?status=success",
  "cancel_url": "http://localhost:3000/pricing?status=cancel"
}
```
**Response**: Stripe checkout URL

### Create Customer Portal Session
```http
POST /api/v1/billing/portal
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "return_url": "http://localhost:3000/billing"
}
```
**Response**: Stripe customer portal URL

### Stripe Webhook
```http
POST /api/v1/billing/webhook/stripe
Stripe-Signature: {signature}
Content-Type: application/json

{...stripe event data...}
```
**Response**: 200 OK

---

## ✅ ORGANIZATIONS (`/api/v1/orgs`)

### Create Organization
```http
POST /api/v1/orgs
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "My Company",
  "slug": "my-company"
}
```
**Response**: Organization object

### List My Organizations
```http
GET /api/v1/orgs
Authorization: Bearer {access_token}
```
**Response**: List of organizations with user's role

### Get Organization
```http
GET /api/v1/orgs/{org_id}
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: Organization details

### Update Organization
```http
PATCH /api/v1/orgs/{org_id}
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "name": "Updated Name"
}
```
**Response**: Updated organization

### Invite Member
```http
POST /api/v1/orgs/{org_id}/invite
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "email": "colleague@example.com",
  "role": "member"
}
```
**Response**: Membership object

### List Members
```http
GET /api/v1/orgs/{org_id}/members
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: List of organization members

### Update Member Role
```http
PATCH /api/v1/orgs/{org_id}/members/{user_id}
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "role": "admin"
}
```
**Response**: Updated membership

### Remove Member
```http
DELETE /api/v1/orgs/{org_id}/members/{user_id}
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: 204 No Content

---

## ✅ API KEYS (`/api/v1/apikeys`)

### Create API Key
```http
POST /api/v1/apikeys
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "name": "Production API Key"
}
```
**Response**: API key with secret (only shown once!)

### List API Keys
```http
GET /api/v1/apikeys
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: List of API keys (secrets hidden)

### Revoke API Key
```http
DELETE /api/v1/apikeys/{key_id}
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: 204 No Content

### Delete API Key Permanently
```http
DELETE /api/v1/apikeys/{key_id}/permanent
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: 204 No Content

---

## ✅ AI & CHAT (`/api/v1/ai`)

### Chat Completion (Non-Streaming)
```http
POST /api/v1/ai/chat
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "message": "Hello, AI!",
  "model": "gemini",
  "stream": false
}
```
**Response**: Complete AI response

### Chat Completion (Streaming)
```http
POST /api/v1/ai/chat/stream
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json

{
  "message": "Hello, AI!",
  "model": "gemini",
  "stream": true
}
```
**Response**: Server-Sent Events (SSE) stream
```
data: {"content": "Hello"}
data: {"content": " there"}
data: {"content": "!"}
data: [DONE]
```

### Get Usage Stats
```http
GET /api/v1/ai/usage
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: AI usage statistics

### Get Available Models
```http
GET /api/v1/ai/models
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: List of available AI models

---

## ✅ PREMIUM FEATURES (`/api/v1/premium`)

### Get Analytics
```http
GET /api/v1/premium/analytics
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: Advanced analytics (Pro/Team only)

### Get White Label Settings
```http
GET /api/v1/premium/white-label
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
```
**Response**: White label configuration (Team only)

### Get Free Feature
```http
GET /api/v1/premium/free-feature
Authorization: Bearer {access_token}
```
**Response**: Feature available to all users

---

## ✅ HEALTH CHECKS

### Basic Health Check
```http
GET /health
```
**Response**: `{"status": "healthy"}`

### Readiness Check
```http
GET /ready
```
**Response**: Database connection status

### Liveness Check
```http
GET /live
```
**Response**: Application liveness status

---

## 📊 METRICS

### Prometheus Metrics
```http
GET /metrics
```
**Response**: Prometheus-formatted metrics

---

## 🔐 Authentication Headers

Most endpoints require these headers:

```http
Authorization: Bearer {access_token}
X-Current-Org: {org_id}
Content-Type: application/json
```

---

## 📝 Common Response Codes

- **200 OK**: Success
- **201 Created**: Resource created
- **204 No Content**: Success with no response body
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

---

## 🎯 Frontend Integration Status

### ✅ Working Endpoints
- Authentication (register, login, refresh)
- User profile (/me)
- Billing checkout
- Health checks

### ⚠️ Partially Working
- Billing subscription (needs org context)
- Billing portal (needs org context)
- Organizations (exists but frontend needs update)
- API Keys (exists but frontend needs update)

### ✅ Ready for Frontend
- AI Chat (streaming works!)
- Team management (all CRUD operations)
- API Keys (all CRUD operations)
- Premium features

---

## 🚀 Quick Test Commands

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Test123!"
```

### Test API Keys
```bash
TOKEN="your_access_token"

# Create key
curl -X POST http://localhost:8000/api/v1/apikeys \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Key"}'

# List keys
curl -X GET http://localhost:8000/api/v1/apikeys \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 1"
```

### Test Chat
```bash
TOKEN="your_access_token"

curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: 1" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello!","model":"gemini","stream":false}'
```

---

## 📚 Summary

**Total Endpoints**: ~30+

**Categories**:
- ✅ Authentication: 3 endpoints
- ✅ Users: 1 endpoint
- ✅ Billing: 5 endpoints
- ✅ Organizations: 8 endpoints
- ✅ API Keys: 4 endpoints
- ✅ AI & Chat: 4 endpoints
- ✅ Premium: 3 endpoints
- ✅ Health: 3 endpoints

**All endpoints are implemented and working!** 🎉

The backend is actually **more complete** than initially thought. The frontend just needs to be updated to use the correct endpoint paths (e.g., `/api/v1/apikeys` instead of `/api/v1/api-keys`).
