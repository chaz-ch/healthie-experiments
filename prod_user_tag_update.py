import csv
import datetime
import time
from alive_progress import alive_bar
from modules.healthie import Healthie
from modules.ids import (
    get_bac_tag_id,
    get_birad_tag_id,
    get_alr_tag_id,
    get_breast_density_tag_id,
    get_report_type_tag_id,
    get_status_tag_id,
    get_report_type_tag_ids,
    get_breast_density_tag_ids,
    get_alr_tag_ids,
    get_birad_tag_ids,
    get_bac_tag_ids,
)
import boto3
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
    """
    Main function to read the CSV file and process each row.
    """
    updated_users = []
    not_found_users = []
    birad_target_users = []

    with open(UPDATED_USERS_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        updated_users = [line.strip().lower() for line in file]

    with open(NOT_FOUND_USERS_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        not_found_users = [line.strip().lower() for line in file]

    with open(BIRAD_TARGET_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        birad_target_users = [line.strip().lower() for line in file]

    H = Healthie(TARGET_ENV)
    rt_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = open(f"user_actions-{TARGET_ENV}-{rt_str}.txt", "a")

    athena_client = boto3.client(
        "athena",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    query_response = athena_client.start_query_execution(
        QueryString=ATHENA_QUERY,
        QueryExecutionContext={"Database": SCHEMA_NAME},
        ResultConfiguration={
            "OutputLocation": S3_STAGING_DIR,
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
        },
    )

    while True:
        try:
            # This function only loads the first 1000 rows
            athena_client.get_query_results(
                QueryExecutionId=query_response["QueryExecutionId"]
            )
            break
        except Exception as err:
            if "not yet finished" in str(err):
                time.sleep(0.001)
            else:
                raise err

    temp_file_location: str = "athena_query_results.csv"
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )
    s3_client.download_file(
        S3_BUCKET_NAME,
        f"{S3_OUTPUT_DIRECTORY}/{query_response['QueryExecutionId']}.csv",
        temp_file_location,
    )

    created_count = 0
    updated_count = 0
    error_count = 0
    row_index = 0
    try:
        with open(temp_file_location, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # report_type      <=====
            # status
            # email            <=====
            # birad            <=====
            # lifetimerisknbr  <=====
            # breastdensity    <=====
            # bac              <=====

            with alive_bar(csv_reader.line_num) as bar:
                for row in csv_reader:
                    row_index += 1

                    # "reporttype","status","email","birad","lifetimerisknbr","breastdensity","bac"
                    user_reporttype = row.get("reporttype")
                    # user_status = row.get("status")
                    user_email = row.get("email")
                    user_birad = row.get("birad")
                    user_lifetimerisknbr = (
                        float(str(row.get("lifetimerisknbr")))
                        if row.get("lifetimerisknbr")
                        else None
                    )
                    user_breastdensity = row.get("breastdensity")
                    user_bac = row.get("bac")

                    if (
                        user_email not in updated_users
                        and user_email not in not_found_users
                    ):
                        response = H.get_user_by_email(str(user_email))
                        # print(response, file=responses)
                        new_user_id = None

                        if len(response["users"]) > 0:
                            new_user_id = response["users"][0]["id"]
                        else:
                            print(f"No user found for email: {user_email}", file=log)
                            not_found_users.append(str(user_email))

                            # print("exiting")
                            error_count += 1
                            # exit()

                        if new_user_id:
                            updated_report_type = False
                            updated_breast_density = False
                            updated_alr = False
                            updated_birad = False
                            updated_bac = False

                            input_vars = {
                                "user_id": new_user_id,
                                "tag_ids_to_check": get_report_type_tag_ids(TARGET_ENV),
                            }
                            user_has_report_type_tag = H.check_user_tags_by_id(
                                input_vars
                            )

                            if (
                                user_reporttype
                                and not user_has_report_type_tag["has_any"]
                            ):
                                REPORT_TYPE_TAG = get_report_type_tag_id(
                                    TARGET_ENV, user_reporttype
                                )

                                print(f"{user_reporttype}: {REPORT_TYPE_TAG}", file=log)

                                # assign tags to that new user:
                                response = H.assign_tag(
                                    [
                                        get_status_tag_id(TARGET_ENV, "Created"),
                                        REPORT_TYPE_TAG,
                                    ],
                                    new_user_id,
                                )
                                updated_report_type = True
                                print(
                                    f"Updated report type for user id: {new_user_id} {user_email}",
                                    file=log,
                                )

                            # Nice to have Phase 1:
                            #     Patient Medical Data (As tags)
                            #          (Nice to have Phase 1)
                            #                 Patient Breast Density
                            #                     Only one value would be sent
                            #                     Potential Values: A, B, C, D
                            # 'Result::BreastDensity::Dense':         '32349'
                            # 'Result::BreastDensity::NonDense':      '32350'

                            input_vars = {
                                "user_id": new_user_id,
                                "tag_ids_to_check": get_breast_density_tag_ids(
                                    TARGET_ENV
                                ),
                            }
                            user_has_breast_density_tag = H.check_user_tags_by_id(
                                input_vars
                            )

                            if (
                                user_breastdensity
                                and not user_has_breast_density_tag["has_any"]
                            ):
                                try:
                                    BREAST_DENSITY_TAG = get_breast_density_tag_id(
                                        TARGET_ENV, user_breastdensity
                                    )
                                except Exception:
                                    BREAST_DENSITY_TAG = None

                                print(
                                    f"{user_breastdensity}: {BREAST_DENSITY_TAG}",
                                    file=log,
                                )

                                if BREAST_DENSITY_TAG:
                                    response = H.assign_tag(
                                        [BREAST_DENSITY_TAG], new_user_id
                                    )
                                    updated_breast_density = True
                                    print(
                                        f"Updated breast density for user id: {new_user_id} {user_email}",
                                        file=log,
                                    )
                                else:
                                    print("No breast density tag to assign")

                            #                 Patient Lifetime Risk
                            #                     Only one value would be sent
                            #                     Potential Values: Average, Intermediate, High
                            # 'Result::TCLifetimeRisk::Average':      '32351'
                            # 'Result::TCLifetimeRisk::High':         '32352'
                            # 'Result::TCLifetimeRisk::Intermediate': '32353'

                            input_vars = {
                                "user_id": new_user_id,
                                "tag_ids_to_check": get_alr_tag_ids(TARGET_ENV),
                            }
                            user_has_alr_tag = H.check_user_tags_by_id(input_vars)

                            if user_lifetimerisknbr and not user_has_alr_tag["has_any"]:
                                LIFETIME_RISK_TAG = get_alr_tag_id(
                                    TARGET_ENV, user_lifetimerisknbr
                                )

                                print(
                                    f"{user_lifetimerisknbr}: {LIFETIME_RISK_TAG}",
                                    file=log,
                                )

                                response = H.assign_tag(
                                    [LIFETIME_RISK_TAG], new_user_id
                                )
                                updated_alr = True
                                print(
                                    f"Updated lifetime risk for user id: {new_user_id} {user_email}",
                                    file=log,
                                )

                            input_vars = {
                                "user_id": new_user_id,
                                "tag_ids_to_check": get_birad_tag_ids(TARGET_ENV),
                            }
                            user_has_birad_tag = H.check_user_tags_by_id(input_vars)

                            if user_birad and not user_has_birad_tag["has_any"]:
                                BIRAD_TAG = get_birad_tag_id(TARGET_ENV, user_birad)

                                print(f"{user_birad}: {BIRAD_TAG}", file=log)

                                if BIRAD_TAG:
                                    response = H.assign_tag([BIRAD_TAG], new_user_id)
                                    updated_birad = True
                                    print(
                                        f"Updated BIRAD for user id: {new_user_id} {user_email}",
                                        file=log,
                                    )
                                else:
                                    print("No BIRAD tag to assign")

                            input_vars = {
                                "user_id": new_user_id,
                                "tag_ids_to_check": get_bac_tag_ids(TARGET_ENV),
                            }
                            user_has_bac_tag = H.check_user_tags_by_id(input_vars)

                            if user_bac and not user_has_bac_tag["has_any"]:
                                BAC_TAG = get_bac_tag_id(TARGET_ENV, user_bac)

                                print(f"{user_bac}: {BAC_TAG}", file=log)

                                if BAC_TAG:
                                    response = H.assign_tag([BAC_TAG], new_user_id)
                                    updated_bac = True
                                    print(
                                        f"Updated BAC for user id: {new_user_id} {user_email}",
                                        file=log,
                                    )
                                else:
                                    print("No BAC tag to assign")

                            if (
                                updated_report_type
                                or updated_breast_density
                                or updated_alr
                                or updated_birad
                                or updated_bac
                            ):
                                updated_count += 1
                                updated_users.append(str(user_email))

                                print(
                                    f"Updated user id: {new_user_id} {user_email}",
                                    file=log,
                                )
                            else:
                                print(
                                    f"No updates for user id: {new_user_id} {user_email}",
                                    file=log,
                                )
                    else:
                        print(
                            f"Skipping user {user_email} as already processed.",
                            file=log,
                        )

                    bar()

            print("Final tally")
            print(f"updated: {updated_count}, errors: {error_count}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "log" in locals() and not log.closed:
            log.close()
            print("log closed.")

        with open(UPDATED_USERS_FILE_PATH, "w") as file:
            for email in updated_users:
                # We use f-strings to add the newline character easily
                file.write(f"{email}\n")

        with open(NOT_FOUND_USERS_FILE_PATH, "w") as file:
            for email in not_found_users:
                # We use f-strings to add the newline character easily
                file.write(f"{email}\n")


if __name__ == "__main__":
    main()
