#!/usr/bin/env python3
"""
Test script to verify access token validity and expiration.

This script checks:
1. If the token format is valid
2. If the token is accepted by Marketo API
3. Token expiration status
4. When token will expire
"""

import sys
import json
import time
from datetime import datetime, timedelta

import requests

import config
from token_manager import TokenManager


def test_configured_token():
    """Test if the configured token in config.py is valid."""
    print("\n" + "=" * 60)
    print("TEST 1: Checking Configured Token")
    print("=" * 60)

    if not config.ACCESS_TOKEN:
        print("⚠️  No configured ACCESS_TOKEN in config.py")
        return False

    print(f"✓ Found configured token: {config.ACCESS_TOKEN[:20]}...")

    # Test the token by making a simple API call
    base_url = config.MARKETO_BASE_URL.rstrip("/")
    test_url = f"{base_url}/bulk/v1/leads.json"

    headers = {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
    }

    try:
        response = requests.get(
            test_url,
            headers=headers,
            timeout=10,
        )

        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ Token is VALID and accepted by Marketo")
            return True
        elif response.status_code == 401:
            print("❌ Token is EXPIRED or INVALID (401 Unauthorized)")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None

    except requests.exceptions.RequestException as exc:
        print(f"❌ Connection error: {exc}")
        return False


def test_generate_new_token():
    """Generate a new token and show its details."""
    print("\n" + "=" * 60)
    print("TEST 2: Generating New Token")
    print("=" * 60)

    token_manager = TokenManager()

    try:
        print("Requesting new token from Marketo...")
        access_token = token_manager.generate_token()

        print(f"\n✓ Successfully generated new token")
        print(f"Token: {access_token[:20]}...")
        print(f"Expiration time: {token_manager.expiration_time}")

        # Convert expiration time to readable format
        exp_datetime = datetime.fromtimestamp(token_manager.expiration_time)
        current_datetime = datetime.now()
        time_until_expiry = exp_datetime - current_datetime

        print(f"Expires at: {exp_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time until expiry: {time_until_expiry.total_seconds():.0f} seconds ({time_until_expiry.total_seconds()/60:.1f} minutes)")

        return access_token

    except Exception as exc:
        print(f"❌ Failed to generate token: {exc}")
        return None


def test_token_validation():
    """Test the TokenManager's validation logic."""
    print("\n" + "=" * 60)
    print("TEST 3: Token Validation Logic")
    print("=" * 60)

    token_manager = TokenManager()

    # Test 1: No token yet
    print("\nScenario 1: No token loaded")
    is_valid = token_manager.is_token_valid()
    print(f"is_token_valid() = {is_valid}")
    print(f"Expected: False ✓" if not is_valid else f"Expected: False ❌")

    # Test 2: Generate token
    print("\nScenario 2: After generating token")
    try:
        token = token_manager.generate_token()
        is_valid = token_manager.is_token_valid()
        print(f"is_token_valid() = {is_valid}")
        print(f"Expected: True ✓" if is_valid else f"Expected: True ❌")

        # Test 3: Simulate expiration
        print("\nScenario 3: Simulating token expiration")
        original_expiration = token_manager.expiration_time
        token_manager.expiration_time = time.time() - 60  # Set to 60 seconds ago

        is_valid = token_manager.is_token_valid()
        print(f"is_token_valid() = {is_valid}")
        print(f"Expected: False ✓" if not is_valid else f"Expected: False ❌")

        # Test 4: Near expiration (should still be invalid due to 60-sec buffer)
        print("\nScenario 4: Near expiration (within 60-sec buffer)")
        token_manager.expiration_time = time.time() + 30  # 30 seconds until expiry

        is_valid = token_manager.is_token_valid()
        print(f"is_token_valid() = {is_valid}")
        print(f"Expected: False ✓" if not is_valid else f"Expected: False ❌")

        # Test 5: Valid token
        print("\nScenario 5: Valid token (well before expiration)")
        token_manager.expiration_time = time.time() + 3000  # 50 minutes until expiry

        is_valid = token_manager.is_token_valid()
        print(f"is_token_valid() = {is_valid}")
        print(f"Expected: True ✓" if is_valid else f"Expected: True ❌")

    except Exception as exc:
        print(f"❌ Error: {exc}")


def test_api_call_with_auto_refresh():
    """Test making an API call with automatic token refresh."""
    print("\n" + "=" * 60)
    print("TEST 4: API Call with Auto-Refresh")
    print("=" * 60)

    token_manager = TokenManager()

    try:
        # Get a valid token
        print("Getting valid token...")
        access_token = token_manager.get_valid_token()

        print(f"✓ Token obtained: {access_token[:20]}...")

        # Make an API call
        print("\nMaking test API call to Marketo...")
        base_url = config.MARKETO_BASE_URL.rstrip("/")
        test_url = f"{base_url}/bulk/v1/leads.json"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(
            test_url,
            headers=headers,
            timeout=10,
        )

        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200:
            print("✓ API call succeeded with auto-refreshed token")
        elif response.status_code == 401:
            print("❌ Token rejected (expired)")
        else:
            print(f"Response: {response.text[:300]}")

    except Exception as exc:
        print(f"❌ Error: {exc}")


def show_token_expiration_info():
    """Display detailed token expiration information."""
    print("\n" + "=" * 60)
    print("Token Expiration Info")
    print("=" * 60)

    token_manager = TokenManager()

    try:
        # Generate a token
        token = token_manager.generate_token()

        exp_time = token_manager.expiration_time
        current_time = time.time()
        time_remaining = exp_time - current_time

        exp_datetime = datetime.fromtimestamp(exp_time)
        current_datetime = datetime.now()

        print(f"\nCurrent time:     {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Token expires at: {exp_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time remaining:   {time_remaining:.0f} seconds")
        print(f"                  = {time_remaining/60:.1f} minutes")
        print(f"                  = {time_remaining/3600:.2f} hours")

        print(f"\n60-second buffer (auto-refresh happens at):")
        refresh_time = exp_datetime - timedelta(seconds=60)
        print(f"  {refresh_time.strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\nToken will auto-refresh if:")
        print(f"  - get_valid_token() called after {refresh_time.strftime('%H:%M:%S')}")
        print(f"  - API call receives 401 response at any time")

    except Exception as exc:
        print(f"❌ Error: {exc}")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MARKETO ACCESS TOKEN VERIFICATION TEST")
    print("=" * 60)

    print(f"\nMarketo Base URL: {config.MARKETO_BASE_URL}")
    print(f"Client ID: {config.CLIENT_ID[:20]}...")

    # Test 1: Check configured token
    configured_valid = test_configured_token()

    # Test 2: Generate new token
    new_token = test_generate_new_token()

    # Test 3: Token validation logic
    test_token_validation()

    # Test 4: API call with auto-refresh
    if new_token:
        test_api_call_with_auto_refresh()

    # Show expiration info
    show_token_expiration_info()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if configured_valid:
        print("✓ Configured token is VALID")
    elif configured_valid is False:
        print("❌ Configured token is EXPIRED or INVALID")
    else:
        print("⚠️  Could not verify configured token status")

    if new_token:
        print("✓ Successfully generated new token")
    else:
        print("❌ Failed to generate new token")

    print("\n✓ Auto-refresh will happen:")
    print("  - 60 seconds before token expires")
    print("  - When API returns 401 (Unauthorized)")
    print("  - On next get_valid_token() call after expiration")


if __name__ == "__main__":
    main()
