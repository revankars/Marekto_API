# Quick Commands - Token Testing

## Run This First (5 seconds)

```bash
python verify_token.py
```

### Possible Outputs:

#### ✅ Good News - Token is Valid
```
🔍 Checking configured token...
   Token: b20c8f9c-eab1-4c19-ae7...

✅ TOKEN IS VALID
   The access token works and is not expired.

You're all set! Your token is working.
```

**What to do:** Run your import!
```bash
python import_leads.py
```

---

#### ❌ Token Expired
```
🔍 Checking configured token...
   Token: b20c8f9c-eab1-4c19-ae7...

❌ TOKEN IS EXPIRED OR INVALID
   API returned 401 Unauthorized.

   ➜ Solution: Run generate new token (see below)

💡 Generate a new token:

✅ NEW TOKEN GENERATED:

   Token: cdf01657-110d-4155-99a7-f986b2ff13a0:int

   Expires: 2026-08-17 14:35:22

📝 Update config.py:
   ACCESS_TOKEN = "cdf01657-110d-4155-99a7-f986b2ff13a0:int"
```

**What to do:**
1. Copy the new token: `cdf01657-110d-4155-99a7-f986b2ff13a0:int`
2. Edit `config.py`
3. Paste it: `ACCESS_TOKEN = "cdf01657-110d-4155-99a7-f986b2ff13a0:int"`
4. Save and test again: `python verify_token.py`

---

## Detailed Analysis (10-15 seconds)

```bash
python test_token.py
```

### Example Output (Condensed)

```
============================================================
MARKETO ACCESS TOKEN VERIFICATION TEST
============================================================

Marketo Base URL: https://235-vbq-065.mktorest.com
Client ID: 81f0bbaa-dd24-4a4e...

============================================================
TEST 1: Checking Configured Token
============================================================

Found configured token: b20c8f9c-eab1-4c19-ae7...
HTTP Status: 200
✓ Token is VALID and accepted by Marketo

============================================================
TEST 2: Generating New Token
============================================================

Generating new token from Marketo...
✓ Successfully obtained access token.
Token expires in 3600 seconds.

✓ Successfully generated new token
Token: cdf01657-110d-4155-99a7-f986b2ff13a0:int
Expires at: 2026-08-17 14:35:22
Time until expiry: 3600 seconds (60.0 minutes)

============================================================
TEST 3: Token Validation Logic
============================================================

Scenario 1: No token loaded
is_token_valid() = False ✓
Expected: False ✓

Scenario 2: After generating token
is_token_valid() = True ✓
Expected: True ✓

Scenario 3: Simulating token expiration
is_token_valid() = False ✓
Expected: False ✓

Scenario 4: Near expiration (within 60-sec buffer)
is_token_valid() = False ✓
Expected: False ✓

Scenario 5: Valid token (well before expiration)
is_token_valid() = True ✓
Expected: True ✓

============================================================
TEST 4: API Call with Auto-Refresh
============================================================

Getting valid token...
✓ Token obtained: cdf01657-110d-4155-99a7...
Making test API call to Marketo...
HTTP Status: 200
✓ API call succeeded with auto-refreshed token

============================================================
Token Expiration Info
============================================================

Current time:     2026-08-17 13:35:22
Token expires at: 2026-08-17 14:35:22
Time remaining:   3600 seconds = 60.0 minutes

60-second buffer (auto-refresh happens at):
  2026-08-17 14:34:22

Token will auto-refresh if:
  - get_valid_token() called after 14:34:22
  - API call receives 401 response at any time

============================================================
SUMMARY
============================================================

✓ Configured token is VALID
✓ Successfully generated new token

✓ Auto-refresh will happen:
  - 60 seconds before token expires
  - When API returns 401 (Unauthorized)
  - On next get_valid_token() call after expiration
```

**What this tells you:**
- ✓ TEST 1: Current token works
- ✓ TEST 2: Can generate new tokens
- ✓ TEST 3: Validation logic is correct
- ✓ TEST 4: Auto-refresh mechanism works
- Token expires in exactly 60 minutes

---

## Monitor Token During Import

```bash
python import_leads.py 2>&1 | grep -i token
```

### Example Output During Execution

```
Using configured access token.
Access token is valid.
Status: Queued
Status: Processing
Status: Processing
Status: Processing
...continues...
```

If import takes more than 1 hour:
```
Using configured access token.
Access token is valid.
Status: Queued
...after 50 minutes...
Status: Processing
Token is expired or invalid. Regenerating...
Successfully obtained access token.
Status: Processing
...continues and completes...
```

---

## Understanding the Output

### HTTP Status Codes

| Code | Meaning | Next Step |
|------|---------|-----------|
| **200 OK** | ✅ Token valid | Use it - proceed with import |
| **401 Unauthorized** | ❌ Token expired | Generate new token |
| **403 Forbidden** | ⚠️ Permissions | Check LaunchPoint roles |
| **500 Server Error** | ⚠️ Marketo issue | Wait and retry |

### Validation Status

| Message | Meaning | Status |
|---------|---------|--------|
| ✓ Token is VALID | Token accepted by API | ✅ Ready |
| ❌ TOKEN IS EXPIRED | API rejected token | ❌ Need new one |
| ⚠️ UNEXPECTED RESPONSE | Unknown status | ⚠️ Check error |

### Token Expiration

```
Generated:  2026-08-17 13:35:22
Expires at: 2026-08-17 14:35:22
Remaining:  60.0 minutes
```

If you see "Time remaining: 60.0 minutes" → Token is fresh ✓

---

## Decision Tree

```
Run: python verify_token.py
        ↓
    ┌───┴───────────────┐
    ↓                   ↓
✅ VALID          ❌ EXPIRED
    ↓                   ↓
Run import          Copy new token
python              from output
import_leads.py         ↓
    ↓               Update config.py
    ↓               (paste token)
  Done ✓                ↓
                    Test again
                    python
                    verify_token.py
                        ↓
                    ✅ VALID
                        ↓
                    Run import ✓
```

---

## Common Command Patterns

### Just Test Token Status
```bash
python verify_token.py
```

### Get New Token (If Expired)
```bash
python verify_token.py
# Copy new token from output
# Paste into config.py
```

### Run Full Test Suite
```bash
python test_token.py
```

### Run Import with Token Monitoring
```bash
python import_leads.py 2>&1 | tee import.log
grep -i "token\|error" import.log
```

### Check Multiple Times (Track Expiration)
```bash
# Run first time
python verify_token.py > token_test_1.txt

# Wait a few minutes

# Run second time
python verify_token.py > token_test_2.txt

# Compare
diff token_test_1.txt token_test_2.txt
```

---

## Output Interpretation Guide

### Scenario 1: Fresh Token

**You see:**
```
✅ TOKEN IS VALID
Time remaining: 3600 seconds (60.0 minutes)
```

**Meaning:** Token just created, fully fresh  
**Action:** Use it, it will last the full hour ✓

---

### Scenario 2: Token Near Expiration

**You see:**
```
✅ TOKEN IS VALID
Time remaining: 120 seconds (2.0 minutes)
```

**Meaning:** Token about to expire  
**Action:** It will auto-refresh, but you could manually get new one

---

### Scenario 3: Token Expired

**You see:**
```
❌ TOKEN IS EXPIRED OR INVALID
API returned 401 Unauthorized
```

**Meaning:** Token no longer works  
**Action:** Follow script's instructions to get new token

---

### Scenario 4: Multiple Tests Show Decreasing Time

**You see (5 minutes apart):**
```
First test:  Time remaining: 2400 seconds (40.0 minutes)
Second test: Time remaining: 1800 seconds (30.0 minutes)
Third test:  Time remaining: 1200 seconds (20.0 minutes)
```

**Meaning:** Token is aging normally, countdown working ✓  
**Action:** None - working as expected

---

## Troubleshooting Commands

### If Connection Error
```bash
# Test internet
ping -c 1 google.com

# Test Marketo connectivity
curl -v https://235-vbq-065.mktorest.com

# Verify URL in config.py
python -c "import config; print(config.MARKETO_BASE_URL)"
```

### If Token Keeps Expiring
```bash
# Generate new token and save it
python verify_token.py > new_token.txt

# View the output
cat new_token.txt | grep "ACCESS_TOKEN ="

# Note: You'll need to manually update config.py
```

### If Import Fails Despite Token Test Passing
```bash
# Run full test suite
python test_token.py

# Run import with full output
python import_leads.py 2>&1 | head -50

# Check if 401 error occurs
python import_leads.py 2>&1 | grep "401"
```

---

## Summary Table

| Task | Command | Time | Result |
|------|---------|------|--------|
| Quick token check | `python verify_token.py` | < 5s | Valid/Expired |
| Detailed analysis | `python test_token.py` | 10-15s | Full report |
| New token | `python verify_token.py` | < 10s | New token |
| Run import | `python import_leads.py` | Variable | Import result |
| Monitor token | `python import_leads.py 2>&1 \| grep token` | Live | Token events |

---

## Quick Reference

**Is my token valid?**
```bash
python verify_token.py
```

**When does it expire?**
```bash
python test_token.py  # Look for "Expires at:"
```

**Need new token?**
```bash
python verify_token.py  # New token shown automatically
```

**Run import safely?**
```bash
python import_leads.py  # Auto-handles token expiration
```

**All automated now!** ✓
