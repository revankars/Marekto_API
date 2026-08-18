# Marketo API - Access Token Management & Testing

## 🚀 Quick Start

### Test Your Token Right Now (5 seconds)
```bash
python verify_token.py
```

You'll see:
- ✅ **TOKEN IS VALID** → Ready to use
- ❌ **TOKEN IS EXPIRED** → New token provided
- ⚠️ **ERROR** → Check credentials

---

## 📚 Documentation Files

### For Users (Read These First)
1. **`TOKEN_TESTING_SUMMARY.md`** ← START HERE
   - Overview of token testing
   - When to use which script
   - Common scenarios

2. **`COMMAND_REFERENCE.md`**
   - Exact commands to run
   - Expected outputs
   - How to interpret results

3. **`TEST_TOKEN_GUIDE.md`**
   - Detailed testing guide
   - Troubleshooting
   - Advanced monitoring

### For Technical Details
4. **`TOKEN_MANAGEMENT.md`**
   - Implementation details
   - Token lifecycle
   - Architecture

5. **`QUICK_REFERENCE.md`**
   - One-page summary
   - Feature overview
   - Protection against errors

---

## 🔧 Test Scripts

### `verify_token.py` - Quick Test (Recommended)
```bash
python verify_token.py
```

**Takes:** < 5 seconds  
**Purpose:** Quick status check  
**Output:** Valid/Expired + solution

---

### `test_token.py` - Full Test Suite
```bash
python test_token.py
```

**Takes:** 10-15 seconds  
**Purpose:** Deep dive into token behavior  
**Tests:** 4 comprehensive test scenarios

---

### `import_leads.py` - Main Script (Updated)
```bash
python import_leads.py
```

**Updated with:**
- ✓ Token validation before each API call
- ✓ Auto-refresh if token expires
- ✓ 401 error handling with retry
- ✓ Works for long-running imports (> 1 hour)

---

## 🔑 Core Module

### `token_manager.py`
Handles all token lifecycle management:
- Generate tokens via Marketo OAuth
- Track expiration time
- Validate before use
- Auto-refresh when needed

---

## 📋 What Changed

### Before
```python
# Old way - single token, no expiration tracking
access_token = get_access_token()
start_import(access_token)
# If token expires during import → 401 error, script fails ❌
```

### After
```python
# New way - auto-validating, auto-refreshing
access_token = get_access_token()  # Via TokenManager
start_import(access_token)         # Validates & auto-refreshes
# Long imports work even if token expires ✓
```

---

## ✅ Testing in 3 Steps

### Step 1: Quick Check
```bash
python verify_token.py
```

### Step 2: Understand Output
```
✅ VALID       → Proceed to Step 3
❌ EXPIRED     → Use provided new token
⚠️ ERROR       → Check credentials
```

### Step 3: Run Import
```bash
python import_leads.py
```

---

## 🛡️ What's Protected

| Scenario | Status |
|----------|--------|
| Token expires during import | ✅ Auto-refreshed |
| Long imports (> 1 hour) | ✅ Supported |
| 401 errors from API | ✅ Auto-retry |
| Polling phase | ✅ Token validated each iteration |
| Multiple concurrent calls | ✅ Each gets valid token |

---

## 📊 Token Information

### Lifespan
```
Generated → Valid for → Auto-Refresh → Expires
(t=0)      (3600 sec)   (60 sec before)
├─ 0-59 min: VALID ✓
├─ 59-60 min: Valid but refresh queued
└─ After 60 min: EXPIRED ❌
```

### Format
```
UUID format: a1b2c3d4-e5f6-7890-abcd-ef1234567890:instance
             └─ UUID ─────────────────────────────┘  └─ ID ─┘
```

### How to Tell if Expired
- **Method 1:** Run `python verify_token.py` (auto-checks)
- **Method 2:** If created > 1 hour ago → likely expired
- **Method 3:** API returns HTTP 401 → definitely expired

---

## 🔄 Auto-Refresh Mechanism

### When it Triggers
1. 60 seconds before expiration (proactive)
2. When API returns 401 (reactive)
3. When `get_valid_token()` is called and token invalid

### How it Works
1. Detects token is expired (or near expiration)
2. Calls Marketo OAuth endpoint
3. Gets new token + expiration time
4. Caches it for future use
5. Continues operation with new token

### You Don't Need to Do Anything
- ✓ Automatic
- ✓ Transparent
- ✓ No manual intervention required

---

## 📝 Configuration

### What You Need (Already in `config.py`)
```python
MARKETO_BASE_URL = "https://XXX-XXX-XXX.mktorest.com"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
ACCESS_TOKEN = "your-token"  # Optional
```

### No Changes Required
- ✓ Existing config works as-is
- ✓ No new settings needed
- ✓ Backward compatible

---

## 🎯 Common Tasks

### "Is my token valid?"
```bash
python verify_token.py
```

### "When does it expire?"
```bash
python test_token.py
# Look for: "Expires at: 2026-08-17 14:35:22"
```

### "I need a new token"
```bash
python verify_token.py
# New token shown in output
# Copy and paste into config.py
```

### "Run my import"
```bash
python import_leads.py
# Token auto-validated and refreshed as needed
```

### "Monitor token during import"
```bash
python import_leads.py 2>&1 | grep -i token
```

---

## ⚠️ Troubleshooting

### Token shows EXPIRED
**Solution:** 
```bash
python verify_token.py
# Copy new token from output
# Update config.py
```

### 401 Unauthorized during import
**Solution:** Already handled! Script auto-regenerates. But:
```bash
python verify_token.py  # Get fresh token
# Update config.py
# Run import again
```

### Connection refused / DNS error
**Solution:**
```bash
# Check internet
ping google.com

# Check Marketo status
curl https://status.marketo.com

# Verify URL in config.py
python -c "import config; print(config.MARKETO_BASE_URL)"
```

### 403 Forbidden
**Solution:** Check LaunchPoint permissions in Marketo Admin

---

## 📖 Which Document to Read

| Question | Read |
|----------|------|
| How do I test my token? | `TOKEN_TESTING_SUMMARY.md` |
| What commands do I run? | `COMMAND_REFERENCE.md` |
| How does it work? | `TOKEN_MANAGEMENT.md` |
| I need troubleshooting | `TEST_TOKEN_GUIDE.md` |
| Quick overview | `QUICK_REFERENCE.md` |

---

## 🔍 File Structure

```
Marketo_API/
├── config.py                      Your credentials
├── import_leads.py                Main script (UPDATED)
├── token_manager.py               Token lifecycle (NEW)
├── verify_token.py                Quick test (NEW)
├── test_token.py                  Full test (NEW)
│
├── Documentation/
│   ├── TOKEN_TESTING_SUMMARY.md   START HERE
│   ├── COMMAND_REFERENCE.md       Command guide
│   ├── TEST_TOKEN_GUIDE.md        Testing guide
│   ├── TOKEN_MANAGEMENT.md        Technical docs
│   ├── QUICK_REFERENCE.md         One-pager
│   ├── README.md                  This file
│   └── QUICK_START.md             Quick start
│
└── lead_data.csv                  Your import file
```

---

## 🚀 One-Minute Getting Started

1. **Test your token:**
   ```bash
   python verify_token.py
   ```

2. **Read the output:**
   - ✅ Valid? → Go to step 3
   - ❌ Expired? → Copy new token, update config.py, go to step 1

3. **Run your import:**
   ```bash
   python import_leads.py
   ```

4. **Done!**
   Token auto-validates and refreshes as needed ✓

---

## ✨ Key Features

✓ **Automatic Token Refresh** - No manual intervention  
✓ **Expiration Tracking** - Knows when to refresh  
✓ **401 Error Handling** - Auto-retry with new token  
✓ **Long-Running Support** - Works for imports > 1 hour  
✓ **Backward Compatible** - Existing code still works  
✓ **No Configuration** - Works with existing config.py  

---

## 📞 Need Help?

- **Token not working?** → Run `python verify_token.py`
- **Import failing?** → Check `TEST_TOKEN_GUIDE.md` troubleshooting
- **Understand lifecycle?** → Read `TOKEN_MANAGEMENT.md`
- **Quick reminder?** → Check `QUICK_REFERENCE.md`

---

## Summary

Your Marketo API integration now:
- ✅ Validates access tokens before use
- ✅ Automatically regenerates expired tokens
- ✅ Handles 401 errors transparently
- ✅ Supports long-running imports (> 1 hour)
- ✅ Requires no manual token management

**Test it:** `python verify_token.py`  
**Use it:** `python import_leads.py`  
**Done!** ✓
