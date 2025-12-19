import csv
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


def main():
    H = Healthie(TARGET_ENV)

    log = open(f"user_details-{TARGET_ENV}-{RT_STR}.txt", "a")

    print(
        "accessed_account\tactive\tany_incomplete_onboarding_steps\tany_shared_courses\tany_shared_documents\tany_shared_incomplete_courses\tany_unviewed_documents\tarchived_at\tconsented_to_labs\tconsents_required\tcreated_at\tcursor\tdietitian_id\tdob\tdoc_share_id\temail\tfull_name\thas_created_password\thas_forms_to_complete\thas_lab_orders\thuman_id\tid\tinvite_code\tis_patient\tlast_active\tlast_activity\tlast_conversation_id\tlast_sign_in_at\tname\tphone_number\trecord_identifier\trequires_reactivation\tset_password_link\tsignup_completed\tskipped_email",
        file=log,
    )

    clinician_consult_charts_opened = {}
    clinician_consult_charts_signed = {}

    order_charts_opened = {}
    order_charts_signed = {}

    invited_users = {}
    responding_users = {}
    row_index = 0
    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                row_index += 1
                print(f"Processing row: {row_index}")

                user_id = row.get("user_id")
                if not user_id:
                    print(
                        f"Skipping row {row_index}: 'user_id' column is missing or empty."
                    )
                    continue

                variables = {"user_id": user_id}
                user_charts = H.list_charts(variables)

                for chart in user_charts["chartNotes"]:
                    print(
                        f"Row: {row_index} - Chart: {chart['id']} - {chart['chart_note_status']} - finished: {chart['finished']} - created: {chart['created_at']} - {chart['name']} - filler: [{chart['filler']['id']} - {chart['filler']['name']}] - user: {chart['user']['id']}",
                        file=log,
                    )
                    if "Clinician Consult" in chart["name"]:
                        if chart["chart_note_status"] == "CREATED":
                            clinician_consult_charts_opened[chart["id"]] = chart[
                                "chart_note_status"
                            ]
                        elif chart["chart_note_status"] == "SIGNED_AND_LOCKED":
                            clinician_consult_charts_opened[chart["id"]] = chart[
                                "chart_note_status"
                            ]
                            clinician_consult_charts_signed[chart["id"]] = chart[
                                "chart_note_status"
                            ]

                    if "Order" in chart["name"]:
                        if chart["chart_note_status"] == "CREATED":
                            order_charts_opened[chart["id"]] = chart[
                                "chart_note_status"
                            ]
                        elif chart["chart_note_status"] == "SIGNED_AND_LOCKED":
                            order_charts_opened[chart["id"]] = chart[
                                "chart_note_status"
                            ]
                            order_charts_signed[chart["id"]] = chart[
                                "chart_note_status"
                            ]

                #     print(f"Chart: {chart['id']} - {chart['chart_note_status']} - finished: {chart['finished']} - created: {chart['created_at']} - {chart['name']} - filler: [{chart['filler']['id']} - {chart['filler']['name']}] - user: {chart['user']['id']}")
        print(
            f"Total Clinician Consult Charts Opened: {len(clinician_consult_charts_opened)}"
        )
        print(
            f"Total Clinician Consult Charts Signed: {len(clinician_consult_charts_signed)}"
        )
        print(f"Total Order Charts Opened: {len(order_charts_opened)}")
        print(f"Total Order Charts Signed: {len(order_charts_signed)}")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "log" in locals() and not log.closed:
            log.close()
            print("log closed.")

    # for user in accessed_users:
    #     print(f"{user}: {accessed_users[user]}")


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
