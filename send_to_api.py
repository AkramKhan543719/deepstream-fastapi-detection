import json
import requests
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000/api/v1/detections"

JSON_DIR = Path("detection_json")


# =========================================================
# SEND ONE JSON FILE
# =========================================================

def send_json_file(json_file):

    print()
    print("=" * 60)
    print(f"Sending: {json_file.name}")
    print("=" * 60)

    try:

        # -------------------------------------------------
        # Read JSON file
        # -------------------------------------------------

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            events = json.load(file)

        print(
            f"Found {len(events)} detection events."
        )

        successful = 0
        failed = 0

        # -------------------------------------------------
        # Send every detection event
        # -------------------------------------------------

        for index, event in enumerate(
            events,
            start=1
        ):

            try:

                response = requests.post(
                    API_URL,
                    json=event,
                    timeout=30
                )

                if response.status_code == 201:

                    successful += 1

                    print(
                        f"[{index}/{len(events)}] SUCCESS"
                    )

                    print(
                        response.json()
                    )

                else:

                    failed += 1

                    print(
                        f"[{index}/{len(events)}] FAILED"
                    )

                    print(
                        response.status_code,
                        response.text
                    )

            except requests.RequestException as e:

                failed += 1

                print(
                    f"[{index}/{len(events)}] "
                    f"REQUEST ERROR: {e}"
                )

        # -------------------------------------------------
        # File summary
        # -------------------------------------------------

        print()
        print(
            f"{json_file.name} completed"
        )

        print(
            f"Successful: {successful}"
        )

        print(
            f"Failed: {failed}"
        )

        return successful, failed

    except Exception as e:

        print(
            f"Error reading {json_file.name}: {e}"
        )

        return 0, 0


# =========================================================
# MAIN
# =========================================================

def send_all_json_files():

    if not JSON_DIR.exists():

        print(
            f"JSON directory not found: {JSON_DIR}"
        )

        return

    # -----------------------------------------------------
    # Find all detection JSON files
    # -----------------------------------------------------

    json_files = sorted(
        JSON_DIR.glob("*_detections.json")
    )

    if not json_files:

        print(
            "No detection JSON files found."
        )

        return

    print(
        f"Found {len(json_files)} JSON files."
    )

    print()

    total_successful = 0
    total_failed = 0

    # -----------------------------------------------------
    # Send every JSON file
    # -----------------------------------------------------

    for json_file in json_files:

        successful, failed = send_json_file(
            json_file
        )

        total_successful += successful
        total_failed += failed

    # -----------------------------------------------------
    # Final summary
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("ALL JSON FILES SENT")
    print("=" * 60)

    print(
        f"JSON files processed: {len(json_files)}"
    )

    print(
        f"Total successful requests: {total_successful}"
    )

    print(
        f"Total failed requests: {total_failed}"
    )

    print("=" * 60)


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    send_all_json_files()