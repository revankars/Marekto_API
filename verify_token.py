#!/usr/bin/env python3
"""
Quick token verification script.

Fast way to check:
1. Is my token valid?
2. Will it expire soon?
3. What should I do?

Usage:
    python verify_token.py
"""

import requests
from datetime import datetime
import config
from token_manager import TokenManager


def check_configured_token():
    """Quick check of the configured token."""
    print("🔍 Checking configured token...")
    print(f"   Token: {config.ACCESS_TOKEN[:30]}...\n")

    base_url = config.MARKETO_BASE_URL.rstrip("/")
    headers = {"Authorization": f"Bearer {config.ACCESS_TOKEN}"}

    try:
        response = requests.get(
            f"{base_url}/bulk/v1/leads.json",
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200:
            print("✅ TOKEN IS VALID")
            print("   The access token works and is not expired.\n")
            return True
        elif response.status_code == 401:
            print("❌ TOKEN IS EXPIRED OR INVALID")
            print("   API returned 401 Unauthorized.\n")
            print("   ➜ Solution: Run generate new token (see below)\n")
            return False
        else:
            print(f"⚠️  UNEXPECTED RESPONSE: {response.status_code}\n")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {e}\n")
        return False


def show_token_expiration():
    """Show when current token will expire."""
    print("⏱️  Token Expiration:")
    print("   Marketo tokens expire after: 3600 seconds (1 hour)\n")

    print("⚠️  If your configured token was generated more than 1 hour ago,")
    print("   it may have expired.\n")


def generate_new_token():
    """Generate and display a new token."""
    print("🔄 Generating new token...\n")

    manager = TokenManager()
    try:
        token = manager.generate_token()
        exp_time = datetime.fromtimestamp(manager.expiration_time)

        print(f"✅ NEW TOKEN GENERATED:\n")
        print(f"   Token: {token}\n")
        print(f"   Expires: {exp_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        print("📝 Update config.py:")
        print(f"   ACCESS_TOKEN = \"{token}\"\n")

        return token

    except Exception as e:
        print(f"❌ Failed to generate token: {e}\n")
        return None


def main():
    print("=" * 60)
    print("MARKETO TOKEN VERIFICATION")
    print("=" * 60 + "\n")

    # Check configured token
    if config.ACCESS_TOKEN:
        is_valid = check_configured_token()

        if is_valid is True:
            print("✅ You're all set! Your token is working.\n")
        else:
            print("💡 Generate a new token:\n")
            new_token = generate_new_token()
            print("   Then update config.py and run your import again.\n")
    else:
        print("⚠️  No ACCESS_TOKEN configured.\n")
        print("   The script will auto-generate tokens using:")
        print(f"   CLIENT_ID: {config.CLIENT_ID}\n")
        print("   Generating test token...\n")
        generate_new_token()

    print("=" * 60)
    print("QUICK REFERENCE")
    print("=" * 60)
    print("""
Token Status Indicators:

✅ 200 OK          → Token is valid
❌ 401 Unauthorized → Token is expired/invalid
⚠️  Other status   → Network or permission issue

Automatic Refresh:

Your import_leads.py now automatically:
  • Validates token before use
  • Refreshes if expired
  • Handles 401 errors with retry
  • Works for long-running imports

You don't need to do anything! But if you want to be safe:

1. Check token status:
   python verify_token.py

2. See detailed info:
   python test_token.py

3. Run full test suite:
   python test_token.py

Questions? Check TOKEN_MANAGEMENT.md
""")


if __name__ == "__main__":
    main()
