# import_leads.py - Marketo Bulk Lead Import

Complete documentation for the Marketo Bulk Lead Import script and its dependencies.

## Table of Contents

1. [Overview](#overview)
2. [Module Dependencies](#module-dependencies)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Functions](#functions)
6. [Error Handling](#error-handling)
7. [Token Management](#token-management)
8. [Workflow](#workflow)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

---

## Overview

`import_leads.py` is a production-ready script that:

- ✅ Validates CSV files before import
- ✅ Authenticates with Marketo API using OAuth tokens
- ✅ Submits bulk lead imports to Marketo
- ✅ Polls for import status until completion
- ✅ Downloads failure and warning reports
- ✅ Automatically handles token expiration
- ✅ Provides detailed error reporting

**File Location:** `/Users/sainath.revankar/Projects/Marketo_API/import_leads.py`

**Python Version:** Python 3.6+

---

## Module Dependencies

### External Dependencies

#### `requests` (HTTP library)
- **Purpose:** Makes HTTP requests to Marketo API
- **Version:** 2.25+ recommended
- **Install:** `pip install requests`
- **Usage in script:**
  - `requests.get()` - Poll import status, retrieve failures/warnings
  - `requests.post()` - Submit CSV for import

#### `config` (Local module)
- **Purpose:** Stores Marketo credentials and settings
- **Location:** `config.py`
- **Provides:**
  ```python
  MARKETO_BASE_URL          # Marketo instance URL
  CLIENT_ID                 # OAuth client ID
  CLIENT_SECRET             # OAuth client secret
  ACCESS_TOKEN              # Pre-generated token (optional)
  CSV_FILE                  # Path to CSV file
  POLL_INTERVAL_SECONDS     # Polling interval
  ```

#### `token_manager` (Local module)
- **Purpose:** Manages OAuth token lifecycle
- **Location:** `token_manager.py`
- **Provides:**
  ```python
  TokenManager              # Main token management class
  ```
- **Key Methods:**
  - `get_valid_token()` - Get or regenerate valid token
  - `generate_token()` - Request new token from Marketo
  - `is_token_valid()` - Check token expiration status

### Standard Library Modules

| Module | Usage |
|--------|-------|
| `csv` | Parse and read CSV file |
| `json` | Parse API responses and format output |
| `os` | File path operations |
| `sys` | System exit codes and stderr output |
| `time` | Sleep between polling iterations |
| `pathlib` | Path validation and file operations |

---

## Configuration

### Required Settings (in `config.py`)

```python
# Marketo instance URL (from Admin > Integration > Web Services)
MARKETO_BASE_URL = "https://235-vbq-065.mktorest.com"

# OAuth credentials (from Admin > Integration > LaunchPoint)
CLIENT_ID = "81f0bbaa-dd24-4a4e-8014-c414d580956f"
CLIENT_SECRET = "82EACMz6PS60LlATzLJ8ytsZtUBjEfqf"

# Pre-generated token (optional - can be left empty)
ACCESS_TOKEN = "f9692f20-02c1-409b-a9e7-ea5a2de8cd3f:or2"

# Path to CSV file to import
CSV_FILE = "lead_data.csv"

# Poll interval in seconds
POLL_INTERVAL_SECONDS = 10
```

### CSV File Requirements

**Format:** CSV (comma-separated values)

**Required Columns:** Must match Marketo REST API field names
```
Email
mktoadobeCmpn
mktolastTouchChannel
mktoECID
```

**File Size:** < 10 MB (Marketo API limit)

**Example:**
```csv
Email,mktoadobeCmpn,mktolastTouchChannel,mktoECID
john@example.com,campaign1,Email,12345
jane@example.com,campaign2,Web,67890
```

---

## Usage

### Basic Usage

```bash
# Simple execution
python3 import_leads.py

# With output to file
python3 import_leads.py > import.log

# With error output
python3 import_leads.py 2>&1 | tee import.log
```

### Expected Output

```
======================================
Marketo Bulk Lead Import
======================================

CSV columns:
  - Email
  - mktoadobeCmpn
  - mktolastTouchChannel
  - mktoECID
CSV validation successful. Rows: 1000

Validating access token...
Access token is valid.

Starting Marketo Bulk Lead Import...
HTTP status: 200

Marketo response:
{
  "success": true,
  "result": [
    {
      "batchId": 1234567890,
      "status": "Queued"
    }
  ]
}

Import submitted successfully.
Batch ID: 1234567890
Status: Queued

Waiting for Marketo to process the import...
Status: Queued
Status: Processing
Status: Processing
Status: Complete

======================================
Import Result
======================================
{
  "batchId": 1234567890,
  "numOfLeadsProcessed": 1000,
  "numOfRowsSucceeded": 995,
  "numOfRowsFailed": 5,
  "numOfRowsWithWarning": 10,
  "status": "Complete"
}

5 row(s) failed.
Failure file saved to: marketo_import_failures_1234567890.csv

10 row(s) have warnings.
Warning file saved to: marketo_import_warnings_1234567890.csv

Import process finished.
```

---

## Functions

### Main Functions

#### `main()`
**Purpose:** Main entry point of the script

**Flow:**
1. Validate CSV file
2. Authenticate and validate token
3. Submit import
4. Poll until completion
5. Retrieve failures/warnings
6. Display results

**Exit Codes:**
- `0` - Success
- `1` - Error (HTTP/API/Validation)

**Error Handling:**
- Catches `requests.exceptions.RequestException`
- Catches all other exceptions
- Prints to stderr
- Exits with code 1

---

### CSV Validation

#### `validate_csv(csv_file)`
**Parameters:**
- `csv_file` (str): Path to CSV file

**Returns:** None

**Raises:**
- `FileNotFoundError` - File doesn't exist
- `ValueError` - File validation failed (size, columns, rows)

**Checks:**
1. File exists
2. File size < 10 MB
3. Contains header row
4. Has all required columns
5. Contains at least 1 data row

**Example:**
```python
try:
    validate_csv("lead_data.csv")
    print("CSV is valid!")
except FileNotFoundError:
    print("CSV file not found")
except ValueError as e:
    print(f"CSV validation failed: {e}")
```

---

### Authentication

#### `get_access_token()`
**Purpose:** Get a valid access token

**Returns:** 
- `str` - Valid access token

**Raises:**
- `RuntimeError` - Failed to obtain token

**Behavior:**
1. If `ACCESS_TOKEN` configured in config.py, use it
2. Otherwise, request new token via `TokenManager`
3. TokenManager auto-refreshes if expired

**Example:**
```python
token = get_access_token()
print(f"Using token: {token}")
```

---

### Import Operations

#### `start_import(access_token)`
**Purpose:** Submit CSV to Marketo for bulk import

**Parameters:**
- `access_token` (str): Valid OAuth token

**Returns:**
- `str` - Batch ID for import tracking

**Raises:**
- `RuntimeError` - Import submission failed

**Features:**
- Reads CSV file in binary mode
- Sends as multipart/form-data
- Handles 401 errors (auto-retry with new token)
- Validates Marketo response

**HTTP Details:**
- **Method:** POST
- **URL:** `{BASE_URL}/bulk/v1/leads.json`
- **Timeout:** 120 seconds
- **Content-Type:** multipart/form-data

**Example:**
```python
batch_id = start_import(access_token)
print(f"Import batch ID: {batch_id}")
```

---

#### `get_import_status(access_token, batch_id)`
**Purpose:** Poll Marketo until import completes

**Parameters:**
- `access_token` (str): Valid OAuth token
- `batch_id` (str): Import batch ID

**Returns:**
- `dict` - Final import status

**Polling:**
- Interval: Configured in `POLL_INTERVAL_SECONDS`
- Continues until status is "Complete" or "Failed"
- Auto-refreshes token each iteration if needed
- Handles 401 errors (auto-retry)

**HTTP Details:**
- **Method:** GET
- **URL:** `{BASE_URL}/bulk/v1/leads/batch/{batch_id}.json`
- **Timeout:** 30 seconds

**Status Values:**
- `Queued` - Waiting to process
- `Processing` - Currently importing
- `Complete` - Import finished successfully
- `Failed` - Import failed

**Example:**
```python
status = get_import_status(token, "1234567890")
print(f"Processed: {status['numOfLeadsProcessed']}")
print(f"Succeeded: {status['numOfRowsSucceeded']}")
print(f"Failed: {status['numOfRowsFailed']}")
```

---

#### `get_failures(access_token, batch_id)`
**Purpose:** Download CSV of failed records

**Parameters:**
- `access_token` (str): Valid OAuth token
- `batch_id` (str): Import batch ID

**Returns:** None

**Output:**
- Creates file: `marketo_import_failures_{batch_id}.csv`
- Contains all failed records with error reasons

**Features:**
- Auto-refreshes token if needed
- Handles 401 errors (auto-retry)
- Gracefully handles missing failures file

**HTTP Details:**
- **Method:** GET
- **URL:** `{BASE_URL}/bulk/v1/leads/batch/{batch_id}/failures.json`
- **Timeout:** 60 seconds

**Example:**
```python
get_failures(token, "1234567890")
# Creates: marketo_import_failures_1234567890.csv
```

---

#### `get_warnings(access_token, batch_id)`
**Purpose:** Download CSV of records with warnings

**Parameters:**
- `access_token` (str): Valid OAuth token
- `batch_id` (str): Import batch ID

**Returns:** None

**Output:**
- Creates file: `marketo_import_warnings_{batch_id}.csv`
- Contains all records with non-critical issues

**Features:**
- Auto-refreshes token if needed
- Handles 401 errors (auto-retry)
- Gracefully handles missing warnings file

**HTTP Details:**
- **Method:** GET
- **URL:** `{BASE_URL}/bulk/v1/leads/batch/{batch_id}/warnings.json`
- **Timeout:** 60 seconds

**Example:**
```python
get_warnings(token, "1234567890")
# Creates: marketo_import_warnings_1234567890.csv
```

---

## Error Handling

### HTTP Status Codes

| Status | Meaning | Script Behavior |
|--------|---------|-----------------|
| 200 OK | Success | Continues processing |
| 401 Unauthorized | Token expired | Auto-regenerates token, retries |
| 403 Forbidden | Permission denied | Raises RuntimeError |
| 500 Server Error | Marketo issue | Raises RuntimeError |

### Marketo Error Codes

| Code | Message | Action |
|------|---------|--------|
| 601 | Access token invalid | Check LaunchPoint permissions |
| 618 | Invalid file format | Validate CSV columns |
| 1001 | Invalid request | Check API parameters |

### Common Exceptions

```python
FileNotFoundError
  ├─ CSV file doesn't exist
  └─ Solution: Check CSV_FILE path in config.py

ValueError
  ├─ CSV validation failed
  │  ├─ File too large (> 10 MB)
  │  ├─ Missing columns
  │  ├─ No data rows
  │  └─ No header row
  └─ Solution: Fix CSV file, rerun

RuntimeError
  ├─ API errors (401, 403, 500, etc)
  ├─ Invalid token
  ├─ Marketo rejected import
  └─ Solution: Check credentials, check permissions

requests.exceptions.RequestException
  ├─ Network connectivity issues
  ├─ Timeout errors
  ├─ DNS resolution failure
  └─ Solution: Check internet, check Marketo status
```

### Error Recovery

**Automatic Recovery:**
- 401 errors → Auto-retry with regenerated token
- Network timeouts → Retry after POLL_INTERVAL

**Manual Recovery:**
- Fix CSV and rerun script
- Update credentials in config.py
- Check LaunchPoint permissions
- Verify Marketo status

---

## Token Management

### Token Lifecycle

```
Token Generation → Validation → Usage → Refresh (if needed) → Success
    ↓
    └─→ TokenManager.generate_token()
        ├─ Requests new token via OAuth
        ├─ Tracks expiration time
        └─ Returns token
```

### Auto-Refresh Triggers

1. **Proactive Refresh** (60-second buffer)
   - When `get_valid_token()` called and token near expiration
   - Prevents 401 errors

2. **Reactive Refresh** (401 error)
   - When API returns 401 Unauthorized
   - Auto-regenerates and retries request

3. **Per-Iteration Refresh**
   - Each polling loop calls `get_valid_token()`
   - Ensures long imports don't timeout

### Token Expiration

- **Lifespan:** 3600 seconds (1 hour)
- **Buffer:** 60 seconds before expiration
- **Refresh:** Automatic before expiration
- **Manual check:** `python3 verify_token.py`

---

## Workflow

### Complete Import Workflow

```
Start
  ↓
[1] Validate CSV File
    ├─ Check file exists
    ├─ Check file size < 10 MB
    ├─ Verify columns present
    ├─ Count data rows
    └─ Exit if validation fails
  ↓
[2] Authenticate
    ├─ Get access token
    ├─ Validate token
    └─ Exit if authentication fails
  ↓
[3] Submit Import
    ├─ Read CSV file
    ├─ POST to Marketo API
    ├─ If 401: Regenerate token & retry
    ├─ Parse response
    ├─ Extract batch ID
    └─ Exit if submission fails
  ↓
[4] Poll Status
    ├─ While status not "Complete" or "Failed":
    │  ├─ Refresh token if needed
    │  ├─ GET status from Marketo
    │  ├─ If 401: Regenerate token & retry
    │  ├─ Print status
    │  └─ Sleep (POLL_INTERVAL seconds)
    └─ Return final status
  ↓
[5] Retrieve Failures (if any)
    ├─ Refresh token if needed
    ├─ GET failures from Marketo
    ├─ Save to CSV file
    └─ Print results
  ↓
[6] Retrieve Warnings (if any)
    ├─ Refresh token if needed
    ├─ GET warnings from Marketo
    ├─ Save to CSV file
    └─ Print results
  ↓
Success
  └─ Exit with code 0
```

### Timing

For a 1000-record import:

```
Time        Event
────        ─────
T+0s        Start
T+2s        CSV validation complete
T+5s        Token validated
T+8s        Import submitted, Batch ID received
T+10s       Poll #1: Queued
T+20s       Poll #2: Processing
T+30s       Poll #3: Processing
T+40s       Poll #4: Complete
T+45s       Failures downloaded (if any)
T+50s       Warnings downloaded (if any)
T+52s       Finished
────────────────
~50 seconds total
```

---

## Examples

### Example 1: Basic Import

```bash
# Prepare CSV with leads
$ cat lead_data.csv
Email,mktoadobeCmpn,mktolastTouchChannel,mktoECID
john@example.com,Q3-Campaign,Email,ABC123
jane@example.com,Q3-Campaign,Web,XYZ789

# Run import
$ python3 import_leads.py

# Output will show:
# ✓ CSV validated
# ✓ Token valid
# ✓ Import submitted (Batch ID: 1234567890)
# ✓ Polling for completion...
# ✓ Import completed successfully
```

### Example 2: Long-Running Import (> 1 hour)

```bash
# Large CSV file (8 MB, 100k records)
$ python3 import_leads.py

# Script will:
# [1] Validate CSV (large file, takes ~5s)
# [2] Get token (expires in 1 hour)
# [3] Submit import (gets batch ID)
# [4] Poll for ~2 hours
#     ├─ Token auto-refreshes at 59-minute mark
#     ├─ Script continues seamlessly
#     └─ Import completes
# [5] Download results
# [6] Exit successfully (exit code 0)

# No manual intervention needed!
```

### Example 3: Handling Import Errors

```bash
$ python3 import_leads.py

# If 5 records fail:
# ✓ Import completed
# 5 row(s) failed.
# Failure file saved to: marketo_import_failures_1234567890.csv

# Check failures
$ cat marketo_import_failures_1234567890.csv
Email,mktoadobeCmpn,mktolastTouchChannel,mktoECID,error
bad@example.com,Q3-Campaign,Email,ABC123,Invalid email format
...

# Fix issues and rerun
```

### Example 4: Monitoring in Real-Time

```bash
# Save output to file for monitoring
$ python3 import_leads.py > import.log &

# Monitor progress in another terminal
$ tail -f import.log

# Output:
# Status: Queued
# Status: Processing
# Status: Processing
# Status: Complete
```

---

## Troubleshooting

### Issue: "CSV file does not exist"

**Error:**
```
FileNotFoundError: CSV file does not exist: lead_data.csv
```

**Solutions:**
1. Check CSV path in `config.py`:
   ```python
   CSV_FILE = "lead_data.csv"  # Must be correct path
   ```

2. Verify file exists:
   ```bash
   ls -la lead_data.csv
   ```

3. Use absolute path:
   ```python
   CSV_FILE = "/Users/sainath.revankar/Projects/Marketo_API/lead_data.csv"
   ```

---

### Issue: "Access token invalid"

**Error:**
```
Marketo rejected the import:
{
  "code": "601",
  "message": "Access token invalid"
}
```

**Solutions:**
1. Generate fresh token:
   ```bash
   python3 verify_token.py
   ```

2. Copy new token to `config.py`:
   ```python
   ACCESS_TOKEN = "new-token-from-verify-token.py"
   ```

3. Check LaunchPoint permissions:
   - Admin > Integration > LaunchPoint
   - Verify "API access" enabled
   - Verify Admin role assigned

4. Try with admin credentials:
   ```python
   CLIENT_ID = "admin-client-id"
   CLIENT_SECRET = "admin-client-secret"
   ACCESS_TOKEN = ""  # Will auto-generate
   ```

---

### Issue: "CSV is missing required columns"

**Error:**
```
ValueError: CSV is missing the following expected columns: Email, mktoadobeCmpn
```

**Solutions:**
1. Check CSV header row:
   ```bash
   head -1 lead_data.csv
   ```

2. Verify column names match exactly:
   - `Email` (not `email`)
   - `mktoadobeCmpn` (exact spelling)
   - `mktolastTouchChannel` (exact spelling)
   - `mktoECID` (exact spelling)

3. Update CSV columns or expected columns in script

---

### Issue: "CSV file is too large"

**Error:**
```
ValueError: CSV file is 12.50 MB. Marketo Bulk Lead Import requires the file to be less than 10 MB.
```

**Solutions:**
1. Split CSV into smaller files:
   ```bash
   # Split 12 MB file into 5 MB chunks
   split -l 50000 lead_data.csv lead_data_part_
   # Upload each file separately
   ```

2. Reduce columns if possible

3. Use different import method for large files

---

### Issue: "Connection refused" or "timeout"

**Error:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solutions:**
1. Check internet connection:
   ```bash
   ping google.com
   ```

2. Verify Marketo status:
   - Check https://status.marketo.com

3. Verify Marketo URL in `config.py`:
   ```python
   MARKETO_BASE_URL = "https://235-vbq-065.mktorest.com"
   # Get correct URL from Admin > Integration > Web Services
   ```

4. Check firewall/proxy settings

---

### Issue: "Import still processing after long wait"

**Behavior:**
- Import stuck in "Processing" state
- Poll continues indefinitely

**Solutions:**
1. Check Marketo status page
2. Check import size (> 1 GB might take longer)
3. Increase `POLL_INTERVAL_SECONDS`:
   ```python
   POLL_INTERVAL_SECONDS = 30  # Check every 30 seconds instead of 10
   ```

4. Check Marketo logs (if admin access)

---

## Limits & Constraints

| Constraint | Value | Note |
|-----------|-------|------|
| CSV file size | < 10 MB | Marketo API limit |
| Records per import | Unlimited | But recommend < 100k |
| Token lifespan | 3600 sec (1 hr) | Auto-refreshed before expiry |
| API timeout | 120s (upload), 30s (poll) | Configurable in code |
| Polling interval | 10s (default) | Configurable in config.py |
| Concurrent imports | 1 per instance | Queue imports sequentially |

---

## Performance Tips

1. **Batch Size:**
   - Optimal: 50,000 - 100,000 records per file
   - Larger files take longer to upload/process

2. **Polling Interval:**
   - Default: 10 seconds (recommended)
   - Increase to 30s for large imports (reduces API calls)

3. **Network:**
   - Upload during off-peak hours
   - Stable connection recommended for large files

4. **Error Checking:**
   - Always check failure reports
   - Fix and re-import failed records

---

## Security Considerations

### Credential Handling

✅ **Safe:**
- Store credentials in `config.py` (not in script)
- Use environment variables (for production):
  ```python
  import os
  CLIENT_ID = os.getenv("MARKETO_CLIENT_ID")
  CLIENT_SECRET = os.getenv("MARKETO_CLIENT_SECRET")
  ```

❌ **Unsafe:**
- Hardcoding secrets in script
- Committing credentials to git
- Sharing credentials via email
- Storing secrets in plain text files

### Token Security

- Tokens expire automatically (1 hour)
- Auto-refresh within 60-second buffer
- Regenerated on 401 errors
- Never logged or cached beyond session

### Data Security

- HTTPS used for all API calls
- SSL/TLS certificate verification enabled
- CSV data sent in multipart format
- Failure reports downloaded securely

---

## Related Files

| File | Purpose |
|------|---------|
| `config.py` | Configuration and credentials |
| `token_manager.py` | OAuth token lifecycle management |
| `verify_token.py` | Quick token validation test |
| `test_token.py` | Comprehensive token testing |
| `lead_data.csv` | Input CSV file |
| `marketo_import_failures_{id}.csv` | Output: failed records |
| `marketo_import_warnings_{id}.csv` | Output: records with warnings |

---

## Support & Documentation

- **Token Issues:** See `TOKEN_MANAGEMENT.md`
- **Testing:** See `TEST_TOKEN_GUIDE.md`
- **Quick Start:** See `README.md`
- **Commands:** See `COMMAND_REFERENCE.md`
- **Marketo API:** https://developers.marketo.com/rest-api/

---

## Summary

`import_leads.py` provides a robust, production-ready solution for importing leads into Marketo with:

✅ Automatic token management  
✅ Comprehensive error handling  
✅ Long-running operation support  
✅ Detailed status reporting  
✅ Failure/warning tracking  
✅ CSV validation  
✅ Secure credential handling  

**Ready to use:** `python3 import_leads.py`
