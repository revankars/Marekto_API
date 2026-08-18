# Token Testing Guide - Summary

## Files Created

### 1. **token_manager.py** (Core Module)
Handles token lifecycle management
- Generates new tokens
- Tracks expiration time
- Validates token before use
- Auto-refreshes when needed

### 2. **verify_token.py** (Quick Test - USE THIS FIRST)
⭐ **Recommended for quick verification**

```bash
python verify_token.py
```

**Takes:** < 5 seconds  
**Shows:** 
- ✅ Token is VALID
- ❌ Token is EXPIRED
- Auto-generates new token if needed

---

### 3. **test_token.py** (Comprehensive Test Suite)
Deep dive into token behavior

```bash
python test_token.py
```

**Takes:** 10-15 seconds  
**Tests:**
- TEST 1: Configured token validity
- TEST 2: Generate new token
- TEST 3: Validation logic (5 scenarios)
- TEST 4: API call with auto-refresh
- Expiration calculations

---

### 4. **import_leads.py** (Updated)
Your main script now has:
- ✓ Token validation before use
- ✓ Auto-refresh for expired tokens
- ✓ 401 error handling with retry
- ✓ Works for long imports (> 1 hour)

---

## How to Test Your Token

### Step 1: Quick Status Check
```bash
$ python verify_token.py

🔍 Checking configured token...
   Token: b20c8f9c-eab1-4c19-ae7...

✅ TOKEN IS VALID
   The access token works and is not expired.

You're all set! Your token is working.
```

### What Each Response Means

| Response | Status | Next Step |
|----------|--------|-----------|
| ✅ TOKEN IS VALID | ✅ Good | Use it! Nothing needed |
| ❌ TOKEN IS EXPIRED | ❌ Bad | Script will show new token |
| ⚠️ UNEXPECTED RESPONSE | ⚠️ Check | Verify credentials/permissions |
| ❌ CONNECTION ERROR | ❌ Network | Check internet/Marketo status |

---

### Step 2: If Token is Valid
```bash
$ python verify_token.py
✅ TOKEN IS VALID

# You're all set! Run your import:
$ python import_leads.py
```

---

### Step 3: If Token is Expired
```bash
$ python verify_token.py
❌ TOKEN IS EXPIRED OR INVALID

💡 Generate a new token:

✅ NEW TOKEN GENERATED:

   Token: cdf01657-110d-4155-99a7-f986b2ff13a0:int
   
   Expires: 2026-08-17 14:35:22

📝 Update config.py:
   ACCESS_TOKEN = "cdf01657-110d-4155-99a7-f986b2ff13a0:int"
```

Then:
1. Copy the new token
2. Open `config.py`
3. Replace `ACCESS_TOKEN = "..."` with the new token
4. Save and test again: `python verify_token.py`

---

## Understanding Token Status

### Token Expiration Timeline
```
Token Generated (t=0)
    ↓
    ├─ 0-59 minutes: VALID ✓
    │
    ├─ At 59 minutes: AUTO-REFRESH kicks in
    │  (60-second buffer)
    │
    ├─ 59-60 minutes: Still VALID
    │  (but will auto-refresh if used)
    │
    └─ After 60 minutes: EXPIRED ❌
       (will return 401)
```

### Quick Reference
- **Token lifespan:** 3600 seconds (1 hour)
- **Auto-refresh buffer:** 60 seconds before expiration
- **When expires:** HTTP 401 response

---

## Test Scenarios

### Scenario A: Token Working Fine
```bash
$ python verify_token.py
✅ TOKEN IS VALID

$ python import_leads.py
# Your import runs successfully
```

### Scenario B: Token Expired
```bash
$ python verify_token.py
❌ TOKEN IS EXPIRED OR INVALID

# Follow the auto-generated solution
# New token is displayed and ready to copy
```

### Scenario C: Testing Validation Logic
```bash
$ python test_token.py
# See all 5 validation scenarios
# Understand when token is considered valid/invalid
```

---

## Interpreting Test Output

### From `verify_token.py`

```
✅ TOKEN IS VALID
   The access token works and is not expired.
```
→ Token works right now, safe to use

```
❌ TOKEN IS EXPIRED OR INVALID
   API returned 401 Unauthorized.
```
→ Token is rejected, need new one

```
⚠️  UNEXPECTED RESPONSE: 403
```
→ Permission or connectivity issue

---

### From `test_token.py`

```
TEST 1: Checking Configured Token
✓ Token is VALID and accepted by Marketo
```
→ Your `config.py` token works

```
TEST 2: Generating New Token
✓ Successfully obtained access token
Token: cdf01657...
Expires at: 2026-08-17 14:35:22
Time until expiry: 3600 seconds (60.0 minutes)
```
→ New token generated, good for 1 hour

```
TEST 3: Token Validation Logic
Scenario 1: No token loaded
is_token_valid() = False ✓

Scenario 5: Valid token (well before expiration)
is_token_valid() = True ✓
```
→ Validation logic works correctly

```
TEST 4: API Call with Auto-Refresh
✓ API call succeeded with auto-refreshed token
```
→ Auto-refresh mechanism is working

---

## Checking Token Without Running Scripts

### Method 1: Manual API Call
```bash
curl -s "https://YOUR-INSTANCE.mktorest.com/bulk/v1/leads.json" \
  -H "Authorization: Bearer YOUR_TOKEN" | head -c 200
```

**Response:**
- Contains `"success": true` or `"success": false` → **Valid** ✓
- Contains `"error": "..."` → Check error message
- HTTP 401 → **Expired** ❌

### Method 2: Check Token Age
```
If you know when token was created:
  Created: 2:00 PM
  Expires: 3:00 PM (add 1 hour)
  Current: 2:45 PM
  
Status: Valid ✓ (15 minutes remaining)
```

### Method 3: Read Token from Marketo Logs
Log into Marketo Admin:
1. Go Admin > Integration > Web Services
2. Look at LaunchPoint
3. Check "Last Used" timestamp
4. If < 1 hour ago → Likely still valid

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Token test shows EXPIRED | Run `verify_token.py` to get new token |
| 403 Forbidden error | Check LaunchPoint permissions in Marketo |
| Connection refused | Verify MARKETO_BASE_URL is correct |
| 401 during import | Already handled! Script auto-refreshes |
| Token works in test but fails in import | Let script auto-refresh - no action needed |

---

## What's Protected Now

✅ **Token expires during import** → Auto-refreshes  
✅ **Long imports (> 1 hour)** → Works fine  
✅ **Polling phase** → Token validated each iteration  
✅ **401 errors** → Auto-retry with new token  
✅ **Concurrent API calls** → Each gets valid token  

---

## Files Overview

```
Marketo_API/
├── config.py                    (Your credentials)
├── import_leads.py              (Main script - UPDATED)
├── token_manager.py             (Token lifecycle - NEW)
├── verify_token.py              (Quick test - NEW)
├── test_token.py                (Full test suite - NEW)
├── TOKEN_MANAGEMENT.md          (Technical details)
├── QUICK_REFERENCE.md           (Quick lookup)
├── TEST_TOKEN_GUIDE.md          (This guide)
└── lead_data.csv                (Your data file)
```

---

## How to Use These Files

### For Quick Verification:
```bash
python verify_token.py
```

### For Understanding Token Lifecycle:
```bash
python test_token.py
```

### For Running Your Import:
```bash
python import_leads.py
```
(It now handles token validation automatically)

### To Read Technical Details:
```bash
cat TOKEN_MANAGEMENT.md
```

---

## Next Steps

1. **Test your token:**
   ```bash
   python verify_token.py
   ```

2. **If valid:** Run your import
   ```bash
   python import_leads.py
   ```

3. **If expired:** Get new token from verify_token.py output and update config.py

4. **No more worries:** Token auto-refreshes during long imports!

---

## Questions?

- **"Is my token working?"** → Run `verify_token.py`
- **"When does it expire?"** → Run `test_token.py` (shows exact time)
- **"How long is token valid?"** → 1 hour (3600 seconds)
- **"What if it expires during import?"** → Auto-handled! No action needed.
- **"How auto-refresh works?"** → See `token_manager.py` or `TOKEN_MANAGEMENT.md`

---

## Quick Test Commands

```bash
# Check if token is valid RIGHT NOW
python verify_token.py

# See detailed token info and timeline
python test_token.py

# Monitor token during import
python import_leads.py 2>&1 | grep -i token

# Get a new token
python verify_token.py  # Shows new token in output
```

That's it! Your token management is now fully automated. ✓
