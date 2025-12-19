from alive_progress import alive_bar
from modules.healthie import Healthie
import os
from dotenv import load_dotenv

load_dotenv()

PAGE_SIZE = (
    100  # The number of users to request per page (determine the server's limit)
)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

SCHEMA_NAME = "sm-development-athena-db-cortex-rz"
S3_BUCKET_NAME = "ch-dev-healthie-temp"
S3_OUTPUT_DIRECTORY = "output"
S3_STAGING_DIR = f"s3://{S3_BUCKET_NAME}/{S3_OUTPUT_DIRECTORY}/"
AWS_REGION = "us-west-2"
ATHENA_QUERY = "select reporttype, status, email, birad, lifetimerisknbr, breastdensity, bac from cz_mammo_reports_unified_vw where status in ('READY')"

# Path to your CSV file
UPDATED_USERS_FILE_PATH = "users_updated.txt"
NOT_FOUND_USERS_FILE_PATH = "users_not_found.txt"
BIRAD_TARGET_FILE_PATH = "birad-0-emails.txt"

# TARGET_ENV = "STAGE"
TARGET_ENV = "PROD"


def id_is_not_provider(user_id):
    return user_id not in [
        "10410358",
        "10578403",
        "10666933",
        "10578423",
        "11008105",
        "11008180",
        "10578357",
    ]


def main():
    """
    Main function to read the CSV file and process each row.
    """

    H = Healthie(TARGET_ENV)

    current_offset = 0
    all_users = []

    # Loop until a page returns fewer results than the limit (PAGE_SIZE)
    while True:
        # Define the variables for the current query
        variables = {"offset": current_offset, "page_size": PAGE_SIZE}

        try:
            response = H.list_users_notification_settings(variables)

            users_on_page = response["users"]

            all_users.extend(users_on_page)

            print(f"Fetched {len(users_on_page)} users. Total so far: {len(all_users)}")

            if not users_on_page:
                # No more users found, end the loop
                print("No more users to fetch. Loop complete.")
                break

            # Check if this was the last page
            if len(users_on_page) < PAGE_SIZE:
                print("Last page retrieved. Loop complete.")
                break

            # Increment the offset for the next iteration
            current_offset += PAGE_SIZE

        except Exception as e:
            print(f"An error occurred during the API request: {e}")
            break

    # now we have all users with notification settings

    with alive_bar(len(all_users)) as bar:
        for user in all_users:
            print(f"{user['id']}: {user['email']}")
            notification_id = user["notification_setting"].get("id")

            input_data = {"notificationSettingId": notification_id}
            if id_is_not_provider(user["id"]):
                response = H.disable_notification_setting(input_data)
                print(
                    f"Updated notification setting for user {user['email']}: {response}"
                )
            else:
                print(f"Skipped provider user {user['email']}")

            bar()


if __name__ == "__main__":
    main()
