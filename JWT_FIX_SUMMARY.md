# JWT Token Fix - Subject Must Be String

## Problem
After logging in, users were immediately redirected back to the login page. The `/api/v1/users/me` endpoint was returning "Could not validate credentials" even with a valid token.

## Root Cause
The JWT library (`python-jose`) requires the `sub` (subject) claim to be a **string**, but we were passing an **integer** (user ID).

### Error Message
```
JWTError: Subject must be a string.
```

### Token Payload (Before Fix)
```json
{
  "sub": 3,           // ❌ Integer
  "exp": 1764849944,
  "type": "access"
}
```

### Token Payload (After Fix)
```json
{
  "sub": "3",         // ✅ String
  "exp": 1764849944,
  "type": "access"
}
```

## Solution

### 1. Fixed Token Creation (`backend/app/core/security.py`)

#### create_access_token
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    # Convert sub to string if it's an integer
    if "sub" in to_encode and isinstance(to_encode["sub"], int):
        to_encode["sub"] = str(to_encode["sub"])
    # ... rest of function
```

#### create_refresh_token
```python
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    # Convert sub to string if it's an integer
    if "sub" in to_encode and isinstance(to_encode["sub"], int):
        to_encode["sub"] = str(to_encode["sub"])
    # ... rest of function
```

### 2. Fixed Token Parsing (`backend/app/dependencies.py`)

```python
payload = decode_token(token)
if payload is None or payload.get("type") != "access":
    raise credentials_exception

user_id_str = payload.get("sub")
if user_id_str is None:
    raise credentials_exception

try:
    user_id = int(user_id_str)  # Convert back to int for database query
except (ValueError, TypeError):
    raise credentials_exception
```

### 3. Fixed Refresh Token Endpoint (`backend/app/api/v1/auth.py`)

```python
payload = decode_token(refresh_token)
if payload is None or payload.get("type") != "refresh":
    raise credentials_exception

user_id_str = payload.get("sub")
if user_id_str is None:
    raise credentials_exception

try:
    user_id = int(user_id_str)  # Convert back to int
except (ValueError, TypeError):
    raise credentials_exception
```

## Testing

### Test 1: Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=DemoPassword123!"
```

**Result:** ✅ Returns access_token and refresh_token

### Test 2: Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <token>"
```

**Result:** ✅ Returns user data
```json
{
  "email": "demo@example.com",
  "full_name": "Demo User",
  "id": 3,
  "is_active": true,
  "is_superuser": false
}
```

### Test 3: Frontend Login
1. Go to http://localhost:3000/login
2. Enter credentials
3. Click "Sign in"

**Result:** ✅ Redirects to /dashboard and stays there

### Test 4: Page Refresh
1. Login successfully
2. Navigate to /dashboard
3. Refresh page (F5)

**Result:** ✅ Stays on /dashboard (doesn't redirect to login)

## Files Modified

1. **backend/app/core/security.py**
   - `create_access_token()` - Convert sub to string
   - `create_refresh_token()` - Convert sub to string

2. **backend/app/dependencies.py**
   - `get_current_user()` - Parse sub as string, convert to int

3. **backend/app/api/v1/auth.py**
   - `refresh_token()` - Parse sub as string, convert to int

## Why This Matters

### JWT Standard (RFC 7519)
The JWT specification states that the `sub` claim should be a **StringOrURI** value:
> "The "sub" (subject) claim identifies the principal that is the subject of the JWT. The Claims in a JWT are normally statements about the subject. The subject value MUST either be scoped to be locally unique in the context of the issuer or be globally unique. The processing of this claim is generally application specific. The "sub" value is a case-sensitive string containing a StringOrURI value."

### Library Enforcement
The `python-jose` library strictly enforces this requirement and will raise an error if `sub` is not a string.

## Prevention

To prevent this issue in the future:
1. Always pass user IDs as strings in JWT claims
2. Convert back to integers when querying the database
3. Add type hints to make this explicit
4. Add tests for token creation and validation

## Status
✅ **FIXED** - JWT tokens now work correctly with string subjects!
