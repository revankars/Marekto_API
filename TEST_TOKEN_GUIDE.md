# Testing Access Token Validity

## Quick Test (Recommended)

### 1. Quick Status Check
```bash
python verify_token.py
```

This gives you a quick answer:
```
✅ TOKEN IS VALID
   The access token works and is not expired.
```

### 2. Detailed Test Suite
```bash
python test_token.py
```

This runs comprehensive tests including:
- Token validation
- Auto-refresh logic
- API connectivity
- Expiration calculations

---

## What Each Script Does

### `verify_token.py` - Quick Check (< 5 seconds)
**Best for:** "Is my token working right now?"

```bash
$ python verify_token.py

✅ TOKEN IS VALID
   The access token works and is not expired.
```

**Checks:**
- Is the configured token accepted by Marketo? (HTTP 200 = YES)
- Would the token be rejected? (HTTP 401 = EXPIRED)

**Output:**
- ✅ TOKEN IS VALID - Safe to use
- ❌ TOKEN IS EXPIRED OR INVALID - Need new token
- ⚠️ UNEXPECTED RESPONSE - Network or permission issue

---

### `test_token.py` - Full Test Suite (10-15 seconds)
**Best for:** "I want to understand my token's lifecycle"

```bash
$ python test_token.py

============================================================
MARKETO ACCESS TOKEN VERIFICATION TEST
============================================================

TEST 1: Checking Configured Token
✓ Token is VALID and accepted by Marketo

TEST 2: Generating New Token
✓ Successfully generated new token
Token: b20c8f9c-eab1-4c19-ae7...
Expires at: 2026-08-17 14:35:22
Time until expiry: 3600 seconds (60.0 minutes)

TEST 3: Token Validation Logic
Scenario 1: No token loaded
is_token_valid() = False ✓

Scenario 2: After generating token
is_token_valid() = True ✓

Scenario 3: Simulating token expiration
is_token_valid() = False ✓

Scenario 4: Near expiration (within 60-sec buffer)
is_token_valid() = False ✓

Scenario 5: Valid token (well before expiration)
is_token_valid() = True ✓

TEST 4: API Call with Auto-Refresh
✓ API call succeeded with auto-refreshed token

============================================================
SUMMARY
✓ Configured token is VALID
✓ Successfully generated new token
```

**Checks:**
- TEST 1: Is configured token working?
- TEST 2: Can we generate a new token?
- TEST 3: Does validation logic work correctly?
- TEST 4: Does auto-refresh work?

---

## How to Understand Token Status

### Token Status Codes

When testing a token against Marketo API:

| Status | Meaning | Action |
|--------|---------|--------|
| **200 OK** | ✅ Token is valid | Use it - no action needed |
| **401 Unauthorized** | ❌ Token is expired/invalid | Generate new token |
| **403 Forbidden** | ⚠️ Permission issue | Check LaunchPoint permissions |
| **500 Server Error** | ⚠️ Marketo issue | Wait and retry |

### Example Test Output

```bash
$ python verify_token.py

🔍 Checking configured token...
   Token: b20c8f9c-eab1-4c19-ae7...

✅ TOKEN IS VALID
   The access token works and is not expired.

You're all set! Your token is working.
```

---

## How to Check Token Expiration

### Method 1: Using test_token.py (Shows Exact Time)
```bash
python test_token.py
```

Look for:
```
Expires at: 2026-08-17 14:35:22
Time remaining: 3600 seconds (60.0 minutes)
```

### Method 2: Check When Token Was Created
Tokens last exactly **1 hour** (3600 seconds)

If your token was created at **2:00 PM**, it expires at **3:00 PM**

### Method 3: Manual Calculation
```
Token creation time + 3600 seconds = Expiration time

Example:
Created: 2026-08-17 13:35:22
Expires: 2026-08-17 14:35:22
```

### Method 4: Look for These Log Messages

When running `import_leads.py`, watch for:

```
✓ "Using configured access token."     → Token will be used
✓ "Using valid cached token."          → Token still valid
⚠️ "Token is expired or invalid"        → Auto-generating new one
✓ "Successfully obtained access token" → New token ready
```

---

## Scenarios & Solutions

### Scenario 1: "I want to test my current token"
```bash
python verify_token.py
```
**Takes:** < 5 seconds  
**Shows:** Valid or Expired

---

### Scenario 2: "I want to understand token lifecycle"
```bash
python test_token.py
```
**Takes:** 10-15 seconds  
**Shows:** Complete token journey

---

### Scenario 3: "My token is expired, get a new one"
```bash
python verify_token.py
```
Output will show:
```
❌ TOKEN IS EXPIRED OR INVALID

💡 Generate a new token:
   ✅ NEW TOKEN GENERATED:
      Token: cdf01657-110d-4155-99a7-f986b2ff13a0:int
      Expires: 2026-08-17 14:35:22
   
   📝 Update config.py:
      ACCESS_TOKEN = "cdf01657-110d-4155-99a7-f986b2ff13a0:int"
```

Then update `config.py`:
```python
ACCESS_TOKEN = "cdf01657-110d-4155-99a7-f986b2ff13a0:int"
```

---

### Scenario 4: "I'm running a long import and worried about token expiration"
✅ You don't need to worry!

The updated `import_leads.py`:
- Checks token validity before each API call
- Auto-refreshes if approaching expiration
- Handles 401 errors automatically
- Works for imports > 1 hour

---

## Token Information

### Token Format
```
Your token looks like:
b20c8f9c-eab1-4c19-ae7e-e6c3b271d20e:or2

Parts:
- UUID: b20c8f9c-eab1-4c19-ae7e-e6c3b271d20e
- Suffix: or2 (identifies your instance)
```

### Token Lifespan
```
┌─ Generated ──────────────────────┬─ Auto-Refresh Buffer ──┬─ Expires
t=0                           t=3540 sec (59 min)      t=3600 sec (60 min)

Token is valid from t=0 to t=3540 (without auto-refresh)
After t=3540, system will auto-refresh before using
```

### Token Storage
```
Configured (config.py):     ACCESS_TOKEN = "..."
Cached (in-memory):         TokenManager.token = "..."
Expiration tracked:         TokenManager.expiration_time = unix_timestamp
```

---

## Troubleshooting

### Problem: "401 Unauthorized when testing"
```bash
python verify_token.py
❌ TOKEN IS EXPIRED OR INVALID
```

**Solution:**
1. Generate new token: `python verify_token.py` (auto-generates)
2. Copy new token to `config.py`
3. Test again: `python verify_token.py`

---

### Problem: "Can't connect to Marketo"
```bash
❌ CONNECTION ERROR: Connection refused
```

**Solution:**
- Check internet connection
- Verify MARKETO_BASE_URL in config.py is correct
- Check if Marketo is down: https://status.marketo.com

---

### Problem: "403 Forbidden when testing"
```bash
⚠️ UNEXPECTED RESPONSE: 403
```

**Solution:**
- Token format is correct
- But LaunchPoint user doesn't have permission
- Check in Marketo: Admin > Integration > Web Services > LaunchPoint permissions

---

### Problem: "Test passes but import still fails"
```bash
python verify_token.py
✅ TOKEN IS VALID

# But import_leads.py still gets 401...
```

**Reason:** Token was valid when tested, but expired during long import

**Solution:** This is already handled! The updated script auto-refreshes. But you can:
1. Generate fresh token: `python verify_token.py`
2. Update config.py
3. Run import again

---

## Advanced: Monitor Token During Import

To watch token refresh in real-time during import:

```bash
# See all token-related messages
python import_leads.py 2>&1 | grep -i token

# Example output:
# Using configured access token.
# Access token is valid.
# Status: Queued
# Status: Processing
# (if import takes > 1 hour)
# Token is expired or invalid. Regenerating...
# Successfully obtained access token.
# Status: Complete
```

---

## Quick Reference Table

| Need | Command | Time | Output |
|------|---------|------|--------|
| Quick status | `python verify_token.py` | < 5s | Valid/Expired |
| Full details | `python test_token.py` | 10-15s | Complete report |
| New token | `python verify_token.py` | < 10s | New token + update code |
| Monitor import | `python import_leads.py 2>&1 \| grep -i token` | Live | Token events |

---

## Token Validation During Import

Your `import_leads.py` now validates tokens:

```python
# Before starting
✓ Check token validity

# Before each API call
✓ Refresh if needed

# If API returns 401
✓ Generate new token
✓ Retry request

# During long polling
✓ Validate token each iteration
✓ Auto-refresh if needed
```

**Result:** You can safely run imports that take > 1 hour!

---

## Summary

### To Test Your Token:
1. **Quick:** `python verify_token.py`
2. **Detailed:** `python test_token.py`
3. **Generate new:** `python verify_token.py` (auto-generates)

### Token Validity Indicators:
- ✅ 200 response = Valid
- ❌ 401 response = Expired
- ⏰ Expires after 3600 seconds (1 hour)
- 🔄 Auto-refresh at 60-second buffer

### You're Protected From:
- Token expiring during import ✓
- 401 errors mid-operation ✓
- Long polling (> 1 hour) ✓
