import datetime
from alive_progress import alive_bar
from modules.healthie import Healthie
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
NOTIFIED_USERS_FILE_PATH = "users_notified.txt"
NOT_FOUND_USERS_FILE_PATH = "users_not_found.txt"
BIRAD_TARGET_FILE_PATH = "birad-0-emails.txt"

# TARGET_ENV = "STAGE"
TARGET_ENV = "PROD"

BIRAD_TEXT = "<p>We’ve reviewed your report, and it shows a BI-RADS 0 result. I want to reassure you that this does not mean you have cancer — it means the radiologist needs additional information to complete your personalized breast screening and give you a final result.</p><p>The usual next step is a diagnostic mammogram, and potentially a breast ultrasound if you have increased breast density, so the radiologist can take a more detailed, focused look. Once the imaging is completed, your report will be updated, and clear next steps will be recommended.</p><p>If you’ve already had your follow-up imaging, that’s great — let us know here in this chat so we can help ensure everything is on track. If you haven’t had follow-up imaging yet, you do not have to navigate this alone. I can help coordinate your care and answer any questions you have about this result, your options, or what to expect.</p><p>Just reply here if you’d like me to get started with scheduling or walk through this together with you.</p>"


def main():
    """
    Main function to read the CSV file and process each row.
    """
    notified_users = []
    birad_target_users = []

    with open(NOTIFIED_USERS_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        notified_users = [line.strip().lower() for line in file]

    with open(NOT_FOUND_USERS_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        not_found_users = [line.strip().lower() for line in file]

    with open(BIRAD_TARGET_FILE_PATH, "r") as file:
        # This reads every line, strips whitespace/newlines, and stores it in a list
        birad_target_users = [line.strip().lower() for line in file]

    H = Healthie(TARGET_ENV)
    rt_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = open(f"user_actions-{TARGET_ENV}-{rt_str}.txt", "a")

    updated_count = 0
    error_count = 0
    row_index = 0
    try:
        with alive_bar(len(birad_target_users)) as bar:
            for user_email in birad_target_users:
                if (
                    user_email not in notified_users
                    and user_email not in not_found_users
                ):
                    response = H.get_user_by_email(str(user_email))
                    # print(response, file=responses)
                    new_user_id = None

                    if len(response["users"]) > 0:
                        new_user_id = response["users"][0]["id"]
                        variables = {"id": new_user_id}

                        response = H.get_user_details(variables)

                        navigator_id = response["user"]["dietitian_id"]

                    else:
                        print(f"No user found for email: {user_email}", file=log)
                        not_found_users.append(str(user_email))

                        # print("exiting")
                        error_count += 1
                        # exit()

                    if new_user_id:
                        variables = {
                            "client_id": str(new_user_id),
                        }

                        response = H.list_patient_conversationMemberships(variables)

                        conversation_memberships = response["conversationMemberships"]

                        # get navigator conversation
                        for conversation in conversation_memberships:
                            conversation_id = conversation["conversation_id"]
                            dietitian_id = conversation["convo"]["dietitian_id"]

                            variables = {
                                "conversation_id": conversation["conversation_id"]
                            }

                            response = H.get_notes(variables)

                            if len(response["notes"]) == 0:
                                print("  No notes found")
                                continue

                            first_note = response["notes"][-1]

                            started_by_navigator = (
                                first_note["creator"]["id"] == navigator_id
                            )

                            if started_by_navigator:
                                is_autogenerated = (
                                    "your Care Navigator" in first_note["content"]
                                )

                                if is_autogenerated:
                                    # here's the right one

                                    # create note with text in that conversation

                                    variables = {
                                        "conversation_id": conversation_id,
                                        "content": BIRAD_TEXT,
                                        "user_id": navigator_id,
                                    }

                                    response = H.create_note(variables)
                                    print(response, file=log)
                                    notified_users.append(str(user_email))

                else:
                    print(f"Skipping {user_email}, already processed.", file=log)

                bar()

        print("Final tally")
        print(f"updated: {updated_count}, errors: {error_count}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "log" in locals() and not log.closed:
            log.close()
            print("log closed.")

        with open(NOTIFIED_USERS_FILE_PATH, "w") as file:
            for email in notified_users:
                # We use f-strings to add the newline character easily
                file.write(f"{email}\n")

        with open(NOT_FOUND_USERS_FILE_PATH, "w") as file:
            for email in not_found_users:
                # We use f-strings to add the newline character easily
                file.write(f"{email}\n")


if __name__ == "__main__":
    main()
