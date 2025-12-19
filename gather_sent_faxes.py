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

    current_cursor = None

    all_faxes = []

    # Loop until a page returns fewer results than the limit (PAGE_SIZE)
    while True:
        # Define the variables for the current query
        variables = {"after": current_cursor}

        try:
            response = H.list_faxes(variables)
            the_faxes = response["sentFaxes"]

            if not the_faxes:
                print("No charts to fetch. Loop complete.")
                break

            for chart in the_faxes:
                current_cursor = chart["cursor"]

            all_faxes.extend(the_faxes)

        except Exception as e:
            print(f"An error occurred during the API request: {e}")
            break

    print(f"Fetched {len(all_faxes)} sent faxes.")

    for fax in all_faxes:
        print(
            f"Fax ID: {fax['id']}, Recipient: {fax['patient']['id']} {fax['patient']['name']} @ {fax['destination_number']}, Sender: {fax['sender']['id']} {fax['sender']['name']},  Status: {fax['status']}"
        )


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
