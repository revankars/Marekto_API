import csv
import json
import os
import sys
import time
from pathlib import Path

import requests

import config
from token_manager import TokenManager


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

BASE_URL = config.MARKETO_BASE_URL.rstrip("/")
CSV_FILE = config.CSV_FILE
POLL_INTERVAL = config.POLL_INTERVAL_SECONDS

# Marketo Bulk Lead Import endpoint
IMPORT_URL = f"{BASE_URL}/bulk/v1/leads.json"

# Global token manager
token_manager = TokenManager()


# These are the columns expected in the CSV.
#
# IMPORTANT:
# These must be the actual Marketo REST API field names,
# not necessarily the friendly/display names shown in Marketo.
EXPECTED_COLUMNS = [
    "Email",
    "mktoadobeCmpn",
    "mktolastTouchChannel",
    "mktoECID",
]


# ------------------------------------------------------------
# Authentication
# ------------------------------------------------------------

def get_access_token():
    """
    Get a valid access token, regenerating if necessary.

    Returns a token that is guaranteed to be valid before expiration.
    """
    return token_manager.get_valid_token()


# ------------------------------------------------------------
# CSV validation
# ------------------------------------------------------------

def validate_csv(csv_file):
    """
    Validate the CSV before sending it to Marketo.
    """

    path = Path(csv_file)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file does not exist: {csv_file}"
        )

    # Marketo Bulk Lead Import requires the file to be < 10 MB.
    file_size = path.stat().st_size

    if file_size >= 10 * 1024 * 1024:
        raise ValueError(
            f"CSV file is {file_size / (1024 * 1024):.2f} MB. "
            "Marketo Bulk Lead Import requires the file to be "
            "less than 10 MB."
        )

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_handle:

        reader = csv.DictReader(csv_handle)

        if reader.fieldnames is None:
            raise ValueError(
                "CSV does not contain a header row."
            )

        actual_columns = [
            column.strip()
            for column in reader.fieldnames
        ]

        print("CSV columns:")
        for column in actual_columns:
            print(f"  - {column}")

        missing = [
            column
            for column in EXPECTED_COLUMNS
            if column not in actual_columns
        ]

        if missing:
            raise ValueError(
                "CSV is missing the following expected columns: "
                + ", ".join(missing)
            )

        row_count = sum(1 for _ in reader)

    if row_count == 0:
        raise ValueError("CSV contains no data rows.")

    print(f"CSV validation successful. Rows: {row_count}")


# ------------------------------------------------------------
# Start import
# ------------------------------------------------------------

def start_import(access_token):
    """
    Submit the CSV to Marketo Bulk Lead Import.

    Handles token expiration by automatically refreshing and retrying.
    """

    print("\nStarting Marketo Bulk Lead Import...")

    params = {
        "format": "csv",
    }

    with open(
        CSV_FILE,
        "rb",
    ) as csv_file:

        files = {
            "file": (
                os.path.basename(CSV_FILE),
                csv_file,
                "text/csv",
            )
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.post(
            IMPORT_URL,
            params=params,
            headers=headers,
            files=files,
            timeout=120,
        )

    print(f"HTTP status: {response.status_code}")

    # Handle 401 Unauthorized (token expired)
    if response.status_code == 401:
        print("Access token expired. Regenerating token and retrying...")
        access_token = token_manager.generate_token()

        with open(
            CSV_FILE,
            "rb",
        ) as csv_file:

            files = {
                "file": (
                    os.path.basename(CSV_FILE),
                    csv_file,
                    "text/csv",
                )
            }

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            response = requests.post(
                IMPORT_URL,
                params=params,
                headers=headers,
                files=files,
                timeout=120,
            )

        print(f"Retry HTTP status: {response.status_code}")

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(
            "Marketo returned a non-JSON response:\n"
            + response.text
        )

    print("\nMarketo response:")
    print(json.dumps(data, indent=2))

    if not response.ok:
        raise RuntimeError(
            f"Marketo HTTP error {response.status_code}"
        )

    if not data.get("success", False):
        raise RuntimeError(
            "Marketo rejected the import:\n"
            + json.dumps(data, indent=2)
        )

    result = data.get("result", [])

    if not result:
        raise RuntimeError(
            "Marketo response did not contain an import result."
        )

    import_result = result[0]

    batch_id = import_result.get("batchId")

    if not batch_id:
        raise RuntimeError(
            "Marketo response did not contain a batchId."
        )

    print(f"\nImport submitted successfully.")
    print(f"Batch ID: {batch_id}")
    print(f"Status: {import_result.get('status')}")

    return batch_id


# ------------------------------------------------------------
# Check import status
# ------------------------------------------------------------

def get_import_status(access_token, batch_id):
    """
    Poll Marketo until the bulk import completes.

    Refreshes token if expired during polling.
    """

    status_url = (
        f"{BASE_URL}/bulk/v1/leads/batch/{batch_id}.json"
    )

    print("\nWaiting for Marketo to process the import...")

    while True:

        # Refresh token if needed before making the request
        access_token = token_manager.get_valid_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(
            status_url,
            headers=headers,
            timeout=30,
        )

        # Handle 401 Unauthorized (token expired)
        if response.status_code == 401:
            print("Access token expired during polling. Regenerating...")
            access_token = token_manager.generate_token()
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(
                status_url,
                headers=headers,
                timeout=30,
            )

        response.raise_for_status()

        data = response.json()

        if not data.get("success", False):
            raise RuntimeError(
                "Unable to retrieve import status:\n"
                + json.dumps(data, indent=2)
            )

        result = data.get("result", [])

        if not result:
            raise RuntimeError(
                "Marketo returned no import status."
            )

        status = result[0]

        current_status = status.get("status")

        print(
            f"Status: {current_status}"
        )

        if current_status in (
            "Complete",
            "Failed",
        ):
            return status

        time.sleep(POLL_INTERVAL)


# ------------------------------------------------------------
# Retrieve failures
# ------------------------------------------------------------

def get_failures(access_token, batch_id):
    """
    Download failure information from Marketo.
    """

    url = (
        f"{BASE_URL}/bulk/v1/leads/"
        f"batch/{batch_id}/failures.json"
    )

    # Refresh token if needed
    access_token = token_manager.get_valid_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60,
    )

    # Handle 401 Unauthorized
    if response.status_code == 401:
        print("Access token expired. Regenerating...")
        access_token = token_manager.generate_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(
            url,
            headers=headers,
            timeout=60,
        )

    if not response.ok:
        print(
            "Unable to retrieve failure file:"
            f" HTTP {response.status_code}"
        )
        print(response.text)
        return

    output_file = (
        f"marketo_import_failures_{batch_id}.csv"
    )

    with open(
        output_file,
        "wb",
    ) as file_handle:

        file_handle.write(response.content)

    print(
        f"Failure file saved to: {output_file}"
    )


# ------------------------------------------------------------
# Retrieve warnings
# ------------------------------------------------------------

def get_warnings(access_token, batch_id):
    """
    Download warning information from Marketo.
    """

    url = (
        f"{BASE_URL}/bulk/v1/leads/"
        f"batch/{batch_id}/warnings.json"
    )

    # Refresh token if needed
    access_token = token_manager.get_valid_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60,
    )

    # Handle 401 Unauthorized
    if response.status_code == 401:
        print("Access token expired. Regenerating...")
        access_token = token_manager.generate_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(
            url,
            headers=headers,
            timeout=60,
        )

    if not response.ok:
        print(
            "Unable to retrieve warning file:"
            f" HTTP {response.status_code}"
        )
        print(response.text)
        return

    output_file = (
        f"marketo_import_warnings_{batch_id}.csv"
    )

    with open(
        output_file,
        "wb",
    ) as file_handle:

        file_handle.write(response.content)

    print(
        f"Warning file saved to: {output_file}"
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    try:

        print("======================================")
        print("Marketo Bulk Lead Import")
        print("======================================")

        # 1. Validate CSV
        validate_csv(CSV_FILE)

        # 2. Authenticate and validate token
        print("\nValidating access token...")
        access_token = get_access_token()

        if not access_token:
            raise RuntimeError("Failed to obtain a valid access token.")

        print("Access token is valid.")

        # 3. Submit import
        batch_id = start_import(access_token)

        # 4. Poll until complete
        status = get_import_status(
            access_token,
            batch_id,
        )

        print("\n======================================")
        print("Import Result")
        print("======================================")

        print(
            json.dumps(
                status,
                indent=2,
            )
        )

        # 5. Retrieve failures/warnings
        num_failed = status.get(
            "numOfRowsFailed",
            0,
        )

        num_warnings = status.get(
            "numOfRowsWithWarning",
            0,
        )

        if num_failed:
            print(
                f"\n{num_failed} row(s) failed."
            )

            get_failures(
                access_token,
                batch_id,
            )

        if num_warnings:
            print(
                f"\n{num_warnings} row(s) have warnings."
            )

            get_warnings(
                access_token,
                batch_id,
            )

        print("\nImport process finished.")

    except requests.exceptions.RequestException as exc:
        print(
            f"\nHTTP/API error: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    except Exception as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()