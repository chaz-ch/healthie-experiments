import datetime
from modules.healthie import Healthie

# TARGET_ENV = "STAGE"
TARGET_ENV = "PROD"

# Path to your CSV file
CSV_FILE_PATH = "user_ids.csv"

PAGE_SIZE = (
    100  # The number of users to request per page (determine the server's limit)
)

RT_STR = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

POSSIBLE_STATUSES = [
    "CREATED",
    "SIGNED",
    "CO_SIGNED",
    "LOCKED",
    "CO_SIGNED_AND_LOCKED",
    "SIGNED_AND_LOCKED",
]


def main():
    H = Healthie(TARGET_ENV)

    clinician_consult_charts_opened = {}
    clinician_consult_charts_signed = {}

    order_charts_opened = {}
    order_charts_signed = {}

    other_charts_opened = {}
    other_charts_signed = {}

    charts_locked = 0

    for status in POSSIBLE_STATUSES:
        current_cursor = None

        all_charts = []

        # Loop until a page returns fewer results than the limit (PAGE_SIZE)
        while True:
            # Define the variables for the current query
            variables = {
                "after": current_cursor,
                "chart_note_status": status,
                "should_paginate": True,
            }
            # print(f"Fetching users with offset: {current_offset}...")

            try:
                response = H.list_charts_by_status(variables)
                the_charts = response["chartNotes"]

                if not the_charts:
                    print("No charts to fetch. Loop complete.")
                    break

                for chart in the_charts:
                    current_cursor = chart["cursor"]

                all_charts.extend(the_charts)

            except Exception as e:
                print(f"An error occurred during the API request: {e}")
                break

        print(f"Fetched {len(all_charts)} charts with status {status}.")

        for chart in all_charts:
            if status == "CREATED":
                if "Clinician Consult" in chart["name"]:
                    clinician_consult_charts_opened[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                elif "Order" in chart["name"]:
                    order_charts_opened[chart["id"]] = chart["chart_note_status"]
                else:
                    other_charts_opened[chart["id"]] = chart["chart_note_status"]
            elif status == "SIGNED":
                if "Clinician Consult" in chart["name"]:
                    clinician_consult_charts_opened[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                    clinician_consult_charts_signed[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                elif "Order" in chart["name"]:
                    order_charts_opened[chart["id"]] = chart["chart_note_status"]
                    order_charts_signed[chart["id"]] = chart["chart_note_status"]
                else:
                    other_charts_opened[chart["id"]] = chart["chart_note_status"]
                    other_charts_signed[chart["id"]] = chart["chart_note_status"]
            elif status == "CO_SIGNED":
                if "Clinician Consult" in chart["name"]:
                    clinician_consult_charts_opened[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                    clinician_consult_charts_signed[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                elif "Order" in chart["name"]:
                    order_charts_opened[chart["id"]] = chart["chart_note_status"]
                    order_charts_signed[chart["id"]] = chart["chart_note_status"]
                else:
                    other_charts_opened[chart["id"]] = chart["chart_note_status"]
                    other_charts_signed[chart["id"]] = chart["chart_note_status"]
            elif status == "LOCKED":
                charts_locked += 1
            elif status == "CO_SIGNED_AND_LOCKED":
                if "Clinician Consult" in chart["name"]:
                    clinician_consult_charts_opened[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                    clinician_consult_charts_signed[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                elif "Order" in chart["name"]:
                    order_charts_opened[chart["id"]] = chart["chart_note_status"]
                    order_charts_signed[chart["id"]] = chart["chart_note_status"]
                else:
                    other_charts_opened[chart["id"]] = chart["chart_note_status"]
                    other_charts_signed[chart["id"]] = chart["chart_note_status"]
            elif status == "SIGNED_AND_LOCKED":
                if "Clinician Consult" in chart["name"]:
                    clinician_consult_charts_opened[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                    clinician_consult_charts_signed[chart["id"]] = chart[
                        "chart_note_status"
                    ]
                elif "Order" in chart["name"]:
                    order_charts_opened[chart["id"]] = chart["chart_note_status"]
                    order_charts_signed[chart["id"]] = chart["chart_note_status"]
                else:
                    other_charts_opened[chart["id"]] = chart["chart_note_status"]
                    other_charts_signed[chart["id"]] = chart["chart_note_status"]

    print(
        f"Total Clinician Consult Charts Opened: {len(clinician_consult_charts_opened)}"
    )
    print(
        f"Total Clinician Consult Charts Signed: {len(clinician_consult_charts_signed)}"
    )
    print(f"Total Order Charts Opened: {len(order_charts_opened)}")
    print(f"Total Order Charts Signed: {len(order_charts_signed)}")
    print(f"Total Other Charts Opened: {len(other_charts_opened)}")
    print(f"Total Other Charts Signed: {len(other_charts_signed)}")
    print(f"Total Charts Locked: {charts_locked}")


if __name__ == "__main__":
    main()

# OK here is the ask, please and thank you!
# Number of Patients that have accessed healthie. Maybe a breakdown by status
# Created
# Invited
# Accessed
# Count of number of patients that have responded to a provider in Healthie (2-way chat)
# Number of clinician consult charts that have been created
# Number of clinician consult charts that have been reviewed/signed
# Number of order charts that have been created
# Number of order charts that have been reviewed/signed
