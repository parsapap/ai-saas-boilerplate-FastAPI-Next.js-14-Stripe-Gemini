# 🤖 AI Integration Guide - Gemini & Multi-Model Support

## 📋 Overview

سیستم AI با قابلیت‌های:
- ✅ 4 مدل AI: Gemini 1.5 Flash/Pro, Claude 3 Haiku, GPT-4o Mini
- ✅ Rate limiting هوشمند با Redis
- ✅ Usage tracking دقیق (messages + tokens)
- ✅ Plan-based limits (Free/Pro/Team)
- ✅ Streaming support (SSE)
- ✅ Background tasks با Celery
- ✅ Cost tracking

---

## 🎯 AI Models

### Gemini 1.5 Flash (پیشنهادی)
```
Provider: Google
Speed: ⚡⚡⚡ خیلی سریع
Cost: $ (ارزان)
Max Tokens: 8,192
Best for: Chat, Q&A, سریع
```

### Gemini 1.5 Pro
```
Provider: Google
Speed: ⚡⚡ متوسط
Cost: $$ (متوسط)
Max Tokens: 8,192
Best for: تحلیل پیچیده، reasoning
```

### Claude 3 Haiku
```
Provider: Anthropic
Speed: ⚡⚡⚡ سریع
Cost: $ (ارزان)
Max Tokens: 4,096
Best for: Chat، خلاصه‌سازی
```

### GPT-4o Mini
```
Provider: OpenAI
Speed: ⚡⚡ متوسط
Cost: $ (ارزان)
Max Tokens: 16,384
Best for: همه‌کاره
```

---

## 📊 Plan-Based Limits

| Feature | Free | Pro | Team |
|---------|------|-----|------|
| **Messages/Month** | 50 | 10,000 | ∞ Unlimited |
| **Tokens/Month** | 50K | 10M | ∞ Unlimited |
| **Rate Limit** | 5/min | 60/min | 300/min |
| **Max Tokens/Request** | 1,024 | 4,096 | 8,192 |
| **Models** | Flash, GPT-4o Mini | همه | همه |

---

## 🚀 API Endpoints

### 1. Chat Completion

```bash
POST /api/v1/ai/chat
```

**Request:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "سلام! چطوری؟"}
  ],
  "model": "gemini-1.5-flash",
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false
}
```

**Response:**
```json
{
  "message": "سلام! من خوبم، ممنون! چطور می‌تونم کمکت کنم؟",
  "model": "gemini-1.5-flash",
  "usage": {
    "input_tokens": 15,
    "output_tokens": 20,
    "total_tokens": 35
  },
  "finish_reason": "stop"
}
```

---

### 2. Streaming Chat

```bash
POST /api/v1/ai/chat/stream
```

**Response (SSE):**
```
data: سلام

data: !

data:  من

data:  خوبم

data: [DONE]
```

**JavaScript Example:**
```javascript
const eventSource = new EventSource('/api/v1/ai/chat/stream');

eventSource.onmessage = (event) => {
  if (event.data === '[DONE]') {
    eventSource.close();
    return;
  }
  console.log(event.data);
};
```

---

### 3. Get Usage Stats

```bash
GET /api/v1/ai/usage
```

**Response:**
```json
{
  "total_messages": 45,
  "total_tokens": 12500,
  "messages_limit": 50,
  "tokens_limit": 50000,
  "usage_percentage": 90.0,
  "models_breakdown": {
    "gemini-1.5-flash": {
      "messages": 40,
      "tokens": 11000,
      "cost": 15
    },
    "gpt-4o-mini": {
      "messages": 5,
      "tokens": 1500,
      "cost": 3
    }
  }
}
```

---

### 4. Get Available Models

```bash
GET /api/v1/ai/models
```

**Response:**
```json
{
  "plan": "pro",
  "models": [
    {
      "id": "gemini-1.5-flash",
      "name": "Gemini 1.5 Flash",
      "provider": "google",
      "max_tokens": 8192
    },
    {
      "id": "gemini-1.5-pro",
      "name": "Gemini 1.5 Pro",
      "provider": "google",
      "max_tokens": 8192
    }
  ]
}
```

---

## 🔧 Setup

### 1. Get API Keys

#### Gemini (Google)
```
1. برو به: https://makersuite.google.com/app/apikey
2. Create API Key
3. کپی کن
```

#### OpenAI
```
1. برو به: https://platform.openai.com/api-keys
2. Create new secret key
3. کپی کن
```

#### Anthropic (Claude)
```
1. برو به: https://console.anthropic.com/
2. Get API Key
3. کپی کن
```

---

### 2. Environment Variables

```env
# backend/.env
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

### 3. Run Migrations

```bash
docker-compose exec backend alembic upgrade head
```

---

### 4. Start Celery Worker (Optional)

```bash
# For background tasks
docker-compose exec backend celery -A app.tasks.celery_app worker --loglevel=info
```

---

## 🧪 Testing

### Test Script

```bash
cd backend
./test_ai.sh
```

### Manual Test

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@test.com&password=pass123" | jq -r '.access_token')

# 2. Create org
ORG_ID=$(curl -s -X POST http://localhost:8000/api/v1/orgs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","slug":"test"}' | jq -r '.id')

# 3. Chat
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Current-Org: $ORG_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "سلام! چطوری؟"}
    ],
    "model": "gemini-1.5-flash"
  }' | jq
```

---

## 💡 Use Cases

### 1. Chatbot

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is FastAPI?"}
]

response = await ai_service.chat_completion(
    messages=messages,
    model="gemini-1.5-flash"
)
```

### 2. Content Generation

```python
messages = [
    {"role": "user", "content": "Write a blog post about AI"}
]

response = await ai_service.chat_completion(
    messages=messages,
    model="gemini-1.5-pro",
    max_tokens=2048
)
```

### 3. Code Assistant

```python
messages = [
    {"role": "user", "content": "Explain this Python code: def fib(n): ..."}
]

response = await ai_service.chat_completion(
    messages=messages,
    model="gpt-4o-mini"
)
```

### 4. Translation

```python
messages = [
    {"role": "user", "content": "Translate to Persian: Hello World"}
]

response = await ai_service.chat_completion(
    messages=messages,
    model="gemini-1.5-flash"
)
```

---

## 🛡️ Rate Limiting

### How it Works

```
1. Per-Minute Rate Limit (Redis)
   - Free: 5 requests/min
   - Pro: 60 requests/min
   - Team: 300 requests/min

2. Monthly Limits (Redis + DB)
   - Messages count
   - Tokens count
   
3. Checks before each request:
   ✓ Rate limit not exceeded?
   ✓ Monthly limit not exceeded?
   ✓ Model allowed in plan?
   ✓ Max tokens within limit?
```

### Error Responses

```json
// Rate limit exceeded
{
  "detail": "Rate limit exceeded. Max 5 requests per minute."
}
// Status: 429

// Monthly limit exceeded
{
  "detail": "Monthly limit exceeded. Upgrade your plan to continue."
}
// Status: 402

// Model not allowed
{
  "detail": "Model gemini-1.5-pro not available in your plan. Upgrade to access."
}
// Status: 403
```

---

## 📈 Usage Tracking

### Database Tables

#### ai_usage (Daily aggregates)
```sql
- organization_id
- date
- model
- message_count
- input_tokens
- output_tokens
- total_tokens
- estimated_cost (cents)
```

#### ai_requests (Individual requests)
```sql
- organization_id
- user_id
- model
- input_tokens
- output_tokens
- duration_ms
- status (success/error)
- error_message
```

### Redis Keys

```
ai_usage:{org_id}:{year-month}:messages → count
ai_usage:{org_id}:{year-month}:tokens → count
ai_rate:{org_id}:minute → rate limit counter
```

---

## ⚡ Background Tasks (Celery)

### Long-running Requests

```python
from app.tasks.ai_tasks import long_chat_completion

# Queue task
task = long_chat_completion.delay(
    messages=[{"role": "user", "content": "..."}],
    model="gemini-1.5-pro",
    org_id=1,
    user_id=1
)

# Check status
result = task.get(timeout=60)
```

### Batch Processing

```python
from app.tasks.ai_tasks import batch_process_messages

messages_batch = [
    {"id": 1, "messages": [...]},
    {"id": 2, "messages": [...]},
]

task = batch_process_messages.delay(
    messages_batch=messages_batch,
    model="gemini-1.5-flash",
    org_id=1
)
```

---

## 💰 Cost Tracking

### Pricing (per 1K tokens)

| Model | Input | Output |
|-------|-------|--------|
| Gemini Flash | $0.00035 | $0.00105 |
| Gemini Pro | $0.00125 | $0.00375 |
| Claude Haiku | $0.00025 | $0.00125 |
| GPT-4o Mini | $0.00015 | $0.00060 |

### Example Calculation

```
Request:
- Input: 100 tokens
- Output: 200 tokens
- Model: Gemini Flash

Cost:
- Input: (100/1000) * $0.00035 = $0.000035
- Output: (200/1000) * $0.00105 = $0.00021
- Total: $0.000245 = 0.0245 cents

Stored as: 0 cents (rounded)
```

---

## 🚨 Error Handling

```python
try:
    response = await ai_service.chat_completion(...)
except HTTPException as e:
    if e.status_code == 429:
        # Rate limit exceeded
        print("Too many requests, wait a minute")
    elif e.status_code == 402:
        # Monthly limit exceeded
        print("Upgrade your plan")
    elif e.status_code == 403:
        # Model not allowed
        print("Model not available in your plan")
```

---

## 📚 Files Structure

```
backend/
├── app/
│   ├── models/
│   │   └── ai_usage.py          # Usage models
│   ├── schemas/
│   │   └── ai.py                # AI schemas
│   ├── services/
│   │   └── ai_service.py        # AI service
│   ├── crud/
│   │   └── ai_usage.py          # Usage CRUD
│   ├── api/v1/
│   │   └── ai.py                # AI endpoints
│   ├── core/
│   │   ├── ai_config.py         # Models & limits
│   │   └── rate_limiter.py      # Rate limiting
│   └── tasks/
│       ├── celery_app.py        # Celery config
│       └── ai_tasks.py          # Background tasks
│
└── alembic/versions/
    └── 004_add_ai_usage.py      # Migration
```

---

سوال داری؟ 😊
