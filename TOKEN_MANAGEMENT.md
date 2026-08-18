# Token Management Implementation

## Overview

I've implemented a comprehensive token management system to handle access token validation and automatic regeneration when expired. This ensures your Marketo API integration continues to work reliably, even when operations take longer than the token's 1-hour lifespan.

## Key Changes

### 1. New Token Manager Module (`token_manager.py`)

A dedicated `TokenManager` class that handles:

- **Token generation**: Creates new OAuth tokens via Marketo's identity endpoint
- **Expiration tracking**: Tracks when tokens expire (default 3600 seconds / 1 hour)
- **Proactive validation**: Checks token validity before use with a 60-second buffer to prevent race conditions
- **Automatic regeneration**: Regenerates expired tokens on-demand

#### Core Methods:

```python
is_token_valid()        # Check if current token is still valid
generate_token()        # Request a new token from Marketo
get_valid_token()       # Get a valid token (use cached if valid, else generate)
refresh_if_needed()     # Proactively refresh before API calls
```

### 2. Enhanced `import_leads.py`

Updated all API functions to:

- **Validate tokens before requests**: Uses `token_manager.get_valid_token()` to ensure fresh tokens
- **Handle 401 responses**: Automatically regenerates tokens and retries if Marketo returns 401 (Unauthorized)
- **Support long-running operations**: Tokens are refreshed during polling phases

#### Updated Functions:

1. **`get_access_token()`**
   - Simplified wrapper around TokenManager
   - Validates token before proceeding

2. **`start_import()`**
   - Validates token before POST
   - If 401 response received, regenerates token and retries automatically

3. **`get_import_status()`**
   - Proactively validates token each polling iteration
   - Handles 401 responses during long-running imports

4. **`get_failures()` & `get_warnings()`**
   - Validate tokens before making API calls
   - Handle token expiration gracefully

5. **`main()`**
   - Explicitly validates token before starting import process
   - Provides clear feedback about token status

## How It Works

### Scenario 1: Token Already Valid
```
start_import() 
  → get_valid_token() 
    → is_token_valid() returns True (cached token is fresh)
    → Uses existing token ✓
```

### Scenario 2: Token Expired During Long-Running Import
```
get_import_status() during polling
  → Loop iteration N
    → get_valid_token()
      → is_token_valid() returns False (expired)
      → generate_token() (auto-refresh)
    → Continue polling with new token ✓
```

### Scenario 3: Token Rejected by API
```
start_import()
  → POST request returns 401 (Unauthorized)
  → generate_token() (regenerate)
  → Retry POST with new token ✓
```

## Configuration

No configuration changes needed in `config.py`, but understand:

- **`ACCESS_TOKEN`** (configured token): Used as-is without expiration tracking
  - Useful for short-lived operations
  - No automatic refresh

- **`CLIENT_ID` & `CLIENT_SECRET`**: Used to generate tokens when needed
  - Required if `ACCESS_TOKEN` is empty
  - Allows automatic token regeneration

## Token Lifecycle

```
Token Generated          Cached for             60-Second Buffer      Actual Expiration
      ↓                     Use                      Before                    ↓
      ├─────────────────────────────────────────────────────────────────────────┤
   t=0                                          t=3540                       t=3600

TokenManager refreshes when:
- get_valid_token() called AND token age > 3540 seconds
- 401 (Unauthorized) response received from API
```

## Error Handling

The implementation handles:

- ✓ Expired tokens during polling (long-running imports)
- ✓ Expired tokens during failure/warning retrieval
- ✓ API rejection with 401 Unauthorized
- ✓ Missing access token (requests new one)
- ✓ Failed token generation (raises clear error)

## Best Practices

1. **Let it auto-refresh**: Don't manually call generate_token() unless needed
2. **Configured token vs. auto-generated**: 
   - Use configured token for short operations
   - Use client credentials for long-running operations
3. **Monitor logs**: Watch for "Access token expired" messages to understand refresh patterns
4. **Error handling**: 401 responses trigger automatic retry - no manual intervention needed

## Example: Long-Running Import

If an import takes 45 minutes:

```
t=0:00   get_access_token()           → New token (expires at 1:00)
t=0:15   start_import() POST           → Uses fresh token
t=10:00  Poll iteration 1              → Token still valid (50 min remaining)
t=30:00  Poll iteration 4              → Token still valid (30 min remaining)
t=50:00  Poll iteration 7              → Token EXPIRED!
         get_valid_token()             → Detects expiration, generates new token
         Continue polling              → Uses new token (expires at 51:00)
t=55:00  Poll iteration 8              → Complete with new token ✓
```

## Testing Token Expiration

To test the regeneration without waiting 1 hour:

```python
# In token_manager.py, temporarily set expires_in to 30 seconds:
# expires_in = 30  # Instead of 3600

# Then run a long-polling operation - token will auto-refresh after 30 sec
```

## Summary

Your Marketo import process now:
- ✓ Validates tokens before use
- ✓ Automatically regenerates expired tokens
- ✓ Handles 401 errors with transparent retry
- ✓ Works reliably for operations longer than 1 hour
- ✓ Maintains backward compatibility with configured tokens
