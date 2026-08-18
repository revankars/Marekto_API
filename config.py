# config.py

# Marketo REST API endpoint base URL.
# Example:
# https://123-ABC-456.mktorest.com
MARKETO_BASE_URL = "https://<marketoapi>.mktorest.com"

# OAuth credentials from Marketo LaunchPoint.
CLIENT_ID = "client-id"
CLIENT_SECRET = "client-secret"

# If an access token has already been provided to you,
# put it here.
#
# If this is None/empty, the script will obtain a new token
# using CLIENT_ID and CLIENT_SECRET.
ACCESS_TOKEN = "access token"

# CSV file to import
CSV_FILE = "lead_data.csv"

# Poll Marketo every N seconds while the import is running.
POLL_INTERVAL_SECONDS = 10
