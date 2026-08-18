import json
import time
from typing import Optional

import requests

import config


class TokenManager:
    """
    Manages OAuth access tokens for Marketo API.

    Handles token generation, expiration tracking, and automatic
    regeneration when needed.
    """

    def __init__(self):
        self.token: Optional[str] = None
        self.expiration_time: Optional[float] = None
        self.base_url = config.MARKETO_BASE_URL.rstrip("/")

    def is_token_valid(self) -> bool:
        """
        Check if the current token is valid and not expired.

        A token is valid if:
        - A token exists
        - Expiration time is set
        - Current time is before expiration (with 60 second buffer)
        """
        if not self.token or self.expiration_time is None:
            return False

        current_time = time.time()
        buffer = 60  # Refresh 60 seconds before actual expiration

        return current_time < (self.expiration_time - buffer)

    def generate_token(self) -> str:
        """
        Request a new OAuth token from Marketo.

        Returns:
            The access token string

        Raises:
            RuntimeError: If token generation fails or response is invalid
        """
        print("Generating new access token...")

        identity_url = f"{self.base_url}/identity/oauth/token"

        params = {
            "grant_type": "client_credentials",
            "client_id": config.CLIENT_ID,
            "client_secret": config.CLIENT_SECRET,
        }

        response = requests.get(
            identity_url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "access_token" not in data:
            raise RuntimeError(
                f"Marketo did not return an access token:\n"
                f"{json.dumps(data, indent=2)}"
            )

        access_token = data["access_token"]
        expires_in = data.get("expires_in", 3600)

        # Store token and calculate expiration time
        self.token = access_token
        self.expiration_time = time.time() + expires_in

        print(f"Successfully obtained access token.")
        print(f"Token expires in {expires_in} seconds.")

        return access_token

    def get_valid_token(self) -> str:
        """
        Get a valid access token.

        If a token is configured in config.py, use it (but don't track expiration).
        Otherwise, generate a new token or refresh if expired.

        Returns:
            A valid access token string
        """
        # If a token is explicitly configured, use it
        if config.ACCESS_TOKEN:
            print("Using configured access token.")
            return config.ACCESS_TOKEN

        # If we don't have a valid token, generate a new one
        if not self.is_token_valid():
            return self.generate_token()

        print("Using valid cached token.")
        return self.token

    def refresh_if_needed(self) -> str:
        """
        Check if token needs refresh and regenerate if expired.

        This is useful when you want to proactively refresh before
        making API calls.

        Returns:
            A valid access token string
        """
        if not self.is_token_valid():
            print("Token is expired or invalid. Regenerating...")
            return self.generate_token()

        return self.token
