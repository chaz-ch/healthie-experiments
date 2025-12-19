from modules.healthie import Healthie
from modules.ids import (
    get_global_provider_id,
)
import os
from dotenv import load_dotenv

load_dotenv()

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


def main():
    H = Healthie(TARGET_ENV)

    input_data = {
        "provider_id": get_global_provider_id(TARGET_ENV),
    }
    response = H.get_provider_appt_id(input_data)

    appt_id = response["appointmentSetting"]["id"]
    hide_link = response["appointmentSetting"]["hide_link"]

    print(f"{appt_id=}, {hide_link=}")

    input_data = {"appointmentSettingId": appt_id}

    response = H.hide_email_links(input_data)

    print(response)

    input_data = {
        "provider_id": get_global_provider_id(TARGET_ENV),
    }
    response = H.get_provider_appt_id(input_data)

    appt_id = response["appointmentSetting"]["id"]
    hide_link = response["appointmentSetting"]["hide_link"]

    print(f"{appt_id=}, {hide_link=}")


if __name__ == "__main__":
    main()
