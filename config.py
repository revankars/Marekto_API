# config.py

# Marketo REST API endpoint base URL.
# Example:
# https://123-ABC-456.mktorest.com
MARKETO_BASE_URL = "https://235-vbq-065.mktorest.com"

# OAuth credentials from Marketo LaunchPoint.
CLIENT_ID = "81f0bbaa-dd24-4a4e-8014-c414d580956f"
CLIENT_SECRET = "82EACMz6PS60LlATzLJ8ytsZtUBjEfqf"

# If an access token has already been provided to you,
# put it here.
#
# If this is None/empty, the script will obtain a new token
# using CLIENT_ID and CLIENT_SECRET.
ACCESS_TOKEN = "f9692f20-02c1-409b-a9e7-ea5a2de8cd3f:or2"

# CSV file to import
CSV_FILE = "lead_data.csv"

# Poll Marketo every N seconds while the import is running.
POLL_INTERVAL_SECONDS = 10