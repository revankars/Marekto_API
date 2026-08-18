# Module Reference Guide

Quick reference for understanding `import_leads.py` and its dependencies.

## Module Structure

```
Marketo_API/
├── import_leads.py          # Main script (entry point)
│   ├── imports config
│   └── imports token_manager
│
├── config.py                # Configuration & credentials
│
├── token_manager.py         # Token lifecycle management
│   └── Used by import_leads.py
│
├── verify_token.py          # Token validation script
│   ├── imports config
│   └── imports token_manager
│
└── test_token.py            # Comprehensive token testing
    ├── imports config
    └── imports token_manager
```

---

## Dependency Graph

```
import_leads.py
    ├─ Standard Library:
    │  ├─ csv         (CSV parsing)
    │  ├─ json        (JSON handling)
    │  ├─ os          (File operations)
    │  ├─ sys         (Exit codes, stderr)
    │  ├─ time        (Sleep/delays)
    │  └─ pathlib     (Path handling)
    │
    ├─ Third-Party:
    │  └─ requests    (HTTP requests)
    │
    └─ Local:
       ├─ config               (Configuration)
       │  └─ Defines:
       │     ├─ MARKETO_BASE_URL
       │     ├─ CLIENT_ID
       │     ├─ CLIENT_SECRET
       │     ├─ ACCESS_TOKEN
       │     ├─ CSV_FILE
       │     └─ POLL_INTERVAL_SECONDS
       │
       └─ token_manager        (Token management)
          └─ Provides:
             └─ TokenManager class
                ├─ get_valid_token()
                ├─ generate_token()
                ├─ is_token_valid()
                └─ Token state (token, expiration_time)
```

---

## config.py - Configuration Module

### Purpose
Stores all configuration, credentials, and constants.

### Location
`/Users/sainath.revankar/Projects/Marketo_API/config.py`

### Variables

```python
MARKETO_BASE_URL = "https://235-vbq-065.mktorest.com"
```
- **Type:** str
- **Purpose:** Base URL for Marketo REST API
- **Source:** Admin > Integration > Web Services > REST API
- **Format:** `https://XXX-ABC-123.mktorest.com`

```python
CLIENT_ID = "81f0bbaa-dd24-4a4e-8014-c414d580956f"
```
- **Type:** str
- **Purpose:** OAuth client ID
- **Source:** Admin > Integration > LaunchPoint
- **Format:** UUID

```python
CLIENT_SECRET = "82EACMz6PS60LlATzLJ8ytsZtUBjEfqf"
```
- **Type:** str
- **Purpose:** OAuth client secret
- **Source:** Admin > Integration > LaunchPoint
- **Format:** Random string

```python
ACCESS_TOKEN = "f9692f20-02c1-409b-a9e7-ea5a2de8cd3f:or2"
```
- **Type:** str or empty
- **Purpose:** Pre-generated access token (optional)
- **Can be:** Empty string (auto-generates using CLIENT_ID/SECRET)
- **Lifespan:** 3600 seconds (1 hour)
- **Format:** `{UUID}:{instance}`

```python
CSV_FILE = "lead_data.csv"
```
- **Type:** str
- **Purpose:** Path to CSV file for import
- **Can be:** Relative or absolute path
- **Must exist:** Yes, before running import_leads.py

```python
POLL_INTERVAL_SECONDS = 10
```
- **Type:** int
- **Purpose:** Seconds to wait between status polls
- **Range:** 1-60 (recommended 10-30)
- **Usage:** Balances real-time feedback vs API calls

### How It's Used in import_leads.py

```python
import config

BASE_URL = config.MARKETO_BASE_URL.rstrip("/")
CSV_FILE = config.CSV_FILE
POLL_INTERVAL = config.POLL_INTERVAL_SECONDS
```

### Updating Configuration

```python
# For different Marketo instance:
MARKETO_BASE_URL = "https://888-XYZ-999.mktorest.com"

# For different CSV file:
CSV_FILE = "/path/to/different/leads.csv"

# For different polling interval:
POLL_INTERVAL_SECONDS = 30

# Regenerate tokens automatically (leave empty):
ACCESS_TOKEN = ""
```

---

## token_manager.py - Token Management Module

### Purpose
Manages OAuth access token lifecycle (generation, validation, refresh).

### Location
`/Users/sainath.revankar/Projects/Marketo_API/token_manager.py`

### Class: TokenManager

#### Attributes

```python
self.token: Optional[str]
```
- Current access token value
- `None` if not generated yet

```python
self.expiration_time: Optional[float]
```
- Unix timestamp when token expires
- `None` if not generated yet

```python
self.base_url: str
```
- Marketo base URL (from config)

#### Methods

##### `is_token_valid() → bool`

**Purpose:** Check if token is valid and not expired

**Returns:**
- `True` - Token exists and expires in > 60 seconds
- `False` - Token missing or expires in < 60 seconds

**Logic:**
```
If token exists AND expiration_time set:
  If (now + 60 sec) < expiration_time:
    Return True
Else:
  Return False
```

**Example:**
```python
manager = TokenManager()
if manager.is_token_valid():
    print("Token is still good!")
else:
    print("Token expired or not set")
```

---

##### `generate_token() → str`

**Purpose:** Request new access token from Marketo OAuth endpoint

**Returns:**
- `str` - New access token

**Raises:**
- `RuntimeError` - Token generation failed

**HTTP Request:**
```
GET {MARKETO_BASE_URL}/identity/oauth/token
  ?grant_type=client_credentials
  &client_id={CLIENT_ID}
  &client_secret={CLIENT_SECRET}
```

**Response:**
```json
{
  "access_token": "f9692f20-02c1-409b-a9e7-ea5a2de8cd3f:or2",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "user@example.com"
}
```

**Side Effects:**
- Sets `self.token` to new token
- Sets `self.expiration_time` based on `expires_in`
- Prints success message

**Example:**
```python
manager = TokenManager()
token = manager.generate_token()
print(f"New token: {token}")
print(f"Expires in: {manager.expiration_time}")
```

---

##### `get_valid_token() → str`

**Purpose:** Get a valid access token (auto-generate if needed)

**Returns:**
- `str` - Guaranteed valid token

**Raises:**
- `RuntimeError` - Failed to get token

**Logic:**
```
If ACCESS_TOKEN configured in config.py:
  Return config.ACCESS_TOKEN (use as-is)

Else if is_token_valid():
  Return self.token (use cached)

Else:
  Call generate_token()
  Return self.token (newly generated)
```

**Example:**
```python
manager = TokenManager()

# First call - generates token
token1 = manager.get_valid_token()  # NEW token

# Second call (< 60 min) - returns cached
token2 = manager.get_valid_token()  # SAME token

# Third call (> 60 min) - regenerates
token3 = manager.get_valid_token()  # NEW token
```

---

##### `refresh_if_needed() → str`

**Purpose:** Proactively refresh token if expired

**Returns:**
- `str` - Valid token

**Logic:**
```
If not is_token_valid():
  Call generate_token()

Return self.token
```

**Example:**
```python
manager = TokenManager()
token = manager.refresh_if_needed()
# Token is guaranteed fresh
```

---

### How TokenManager is Used in import_leads.py

```python
# 1. Initialize (global)
token_manager = TokenManager()

# 2. Get token before import
access_token = token_manager.get_valid_token()

# 3. Auto-refresh during polling
access_token = token_manager.get_valid_token()

# 4. Handle 401 error
if response.status_code == 401:
    access_token = token_manager.generate_token()
```

---

## Imports in import_leads.py

### Standard Library Imports

```python
import csv
```
- **Used for:** Reading CSV files
- **Functions used:**
  - `csv.DictReader()` - Parse CSV with headers

```python
import json
```
- **Used for:** Parse API responses, format output
- **Functions used:**
  - `json.dumps()` - Pretty-print JSON
  - `.json()` method on requests

```python
import os
```
- **Used for:** File operations
- **Functions used:**
  - `os.path.basename()` - Get filename without path

```python
import sys
```
- **Used for:** Exit codes and error output
- **Functions used:**
  - `sys.exit(1)` - Exit with error code
  - `sys.stderr` - Print to stderr

```python
import time
```
- **Used for:** Delays and timing
- **Functions used:**
  - `time.sleep()` - Pause between polls

```python
from pathlib import Path
```
- **Used for:** Path manipulation
- **Functions used:**
  - `Path()` - Create path object
  - `.exists()` - Check if file exists
  - `.stat().st_size` - Get file size

---

### Third-Party Imports

```python
import requests
```
- **Used for:** HTTP requests to Marketo API
- **Functions used:**
  - `requests.get()` - GET requests
  - `requests.post()` - POST requests
  - `.raise_for_status()` - Check HTTP status
  - `.json()` - Parse JSON response
  - Exception handling

---

### Local Imports

```python
import config
```
- **Imported from:** `config.py` (same directory)
- **Provides:** Marketo credentials and settings
- **Usage:**
  ```python
  config.MARKETO_BASE_URL
  config.CLIENT_ID
  config.CLIENT_SECRET
  config.ACCESS_TOKEN
  config.CSV_FILE
  config.POLL_INTERVAL_SECONDS
  ```

```python
from token_manager import TokenManager
```
- **Imported from:** `token_manager.py` (same directory)
- **Provides:** TokenManager class
- **Usage:**
  ```python
  token_manager = TokenManager()
  token_manager.get_valid_token()
  token_manager.generate_token()
  ```

---

## Import Resolution

When Python encounters `import config` or `from token_manager import TokenManager`:

1. **Check sys.path** - includes current directory
2. **Look in current directory** - finds `config.py` and `token_manager.py`
3. **Load module** - executes module code
4. **Return reference** - to module or specific class

### Directory Structure Required

```
/Users/sainath.revankar/Projects/Marketo_API/
├── config.py                      ← Must exist
├── token_manager.py               ← Must exist
├── import_leads.py                ← Imports both
├── verify_token.py
├── test_token.py
└── lead_data.csv
```

### Common Import Errors

```
ModuleNotFoundError: No module named 'config'
```
→ `config.py` not in same directory

```
ModuleNotFoundError: No module named 'requests'
```
→ Install: `pip install requests`

```
ImportError: cannot import name 'TokenManager' from 'token_manager'
```
→ `TokenManager` class not defined in `token_manager.py`

---

## Data Flow

### Token Data Flow

```
config.CLIENT_ID ─┐
config.CLIENT_SECRET ─┤
                  └──→ TokenManager.generate_token()
                           │
                           ├─→ HTTP GET to Marketo
                           │
                           ├─→ Parse response
                           │
                           ├─→ Store self.token
                           │
                           └─→ Store self.expiration_time
                                │
                                └──→ get_valid_token()
                                     │
                                     └──→ import_leads.py
                                          (each API call)
```

### CSV Data Flow

```
config.CSV_FILE ─┐
                 └──→ validate_csv()
                      │
                      ├─→ Check file exists
                      ├─→ Check file size
                      ├─→ Parse headers
                      ├─→ Verify columns
                      └─→ Count rows
                           │
                           └──→ start_import()
                                │
                                ├─→ Read CSV file (binary)
                                │
                                ├─→ POST to Marketo API
                                │
                                └─→ Get batch ID
                                     │
                                     └──→ get_import_status()
                                          (polling loop)
```

### API Response Data Flow

```
Marketo API ─→ HTTP Response
                 │
                 ├─→ response.status_code (int)
                 │   ├─→ 200: Success
                 │   ├─→ 401: Token expired (retry)
                 │   └─→ 4xx/5xx: Error
                 │
                 ├─→ response.json() (dict)
                 │   ├─→ "success": bool
                 │   ├─→ "result": list
                 │   ├─→ "errors": list
                 │   └─→ "batchId": str
                 │
                 └──→ import_leads.py
                      (process results)
```

---

## Execution Flow

### Call Stack During Import

```
main()
├─→ validate_csv()
│   └─→ CSV operations
│
├─→ get_access_token()
│   └─→ token_manager.get_valid_token()
│       └─→ token_manager.generate_token()
│           └─→ requests.get() [Marketo API]
│
├─→ start_import()
│   ├─→ Read CSV file
│   ├─→ requests.post() [Marketo API]
│   ├─→ If 401:
│   │   └─→ token_manager.generate_token()
│   │       └─→ requests.get() [Marketo API]
│   │   └─→ requests.post() [RETRY]
│   └─→ Parse response
│
├─→ get_import_status()
│   ├─→ While loop:
│   │   ├─→ token_manager.get_valid_token()
│   │   ├─→ requests.get() [Marketo API]
│   │   ├─→ If 401:
│   │   │   └─→ token_manager.generate_token()
│   │   │       └─→ Retry request
│   │   └─→ time.sleep()
│   └─→ Return final status
│
├─→ get_failures()
│   ├─→ token_manager.get_valid_token()
│   ├─→ requests.get() [Marketo API]
│   ├─→ If 401: Regenerate & retry
│   └─→ Write CSV file
│
├─→ get_warnings()
│   ├─→ token_manager.get_valid_token()
│   ├─→ requests.get() [Marketo API]
│   ├─→ If 401: Regenerate & retry
│   └─→ Write CSV file
│
└─→ Exit (0 or 1)
```

---

## Summary Table

| Component | Type | Purpose | Location |
|-----------|------|---------|----------|
| config.py | Module | Configuration & credentials | Same dir |
| token_manager.py | Module | Token management | Same dir |
| MARKETO_BASE_URL | Variable | Marketo instance URL | config.py |
| CLIENT_ID | Variable | OAuth client ID | config.py |
| CLIENT_SECRET | Variable | OAuth secret | config.py |
| ACCESS_TOKEN | Variable | Optional token | config.py |
| CSV_FILE | Variable | Input file path | config.py |
| TokenManager | Class | Token lifecycle | token_manager.py |
| get_valid_token() | Method | Get/generate token | TokenManager |
| generate_token() | Method | Request new token | TokenManager |
| is_token_valid() | Method | Check expiration | TokenManager |
| validate_csv() | Function | Validate CSV | import_leads.py |
| get_access_token() | Function | Get token wrapper | import_leads.py |
| start_import() | Function | Submit import | import_leads.py |
| get_import_status() | Function | Poll status | import_leads.py |
| get_failures() | Function | Download failures | import_leads.py |
| get_warnings() | Function | Download warnings | import_leads.py |
| main() | Function | Entry point | import_leads.py |

---

## Next Steps

1. **Review import_leads.py** - Main script
2. **Review config.py** - Update credentials
3. **Review token_manager.py** - Token logic
4. **Run:** `python3 import_leads.py`
5. **Monitor:** Check output and CSV results

All modules work together seamlessly! ✓
