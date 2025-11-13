import csv
import datetime
from modules.healthie import Healthie

# Path to your CSV file
CSV_FILE_PATH = "healthie-user-ID-update.csv"

# ch_user_id,                           sm_user_id,                           healthie_user_id, email
# cb9fd4e9-c334-45c6-b311-5dd69e0f71cd, f0dfcebe-8ad0-4ea1-933b-ca4653c5a160, 10666933,         bridget@cascaidhealth.com

# TARGET_ENV = "STAGE"
TARGET_ENV = "PROD"


def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie(TARGET_ENV)
    rt_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = open(f"user_actions-{TARGET_ENV}-{rt_str}.txt", "a")
    responses = open(f"api_responses-{TARGET_ENV}-{rt_str}.txt", "a")

    print("Healthie ID\tCascaid ID\tSimonMed ID", file=log)

    updated_count = 0
    error_count = 0
    row_index = 0

    try:
        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # ch_user_id,
            # sm_user_id,
            # healthie_user_id,
            # email,
            for row in csv_reader:
                row_index += 1
                print(
                    f"Processing row: {row_index} - updated: {updated_count}, errors: {error_count}"
                )

                print(row, file=responses)

                user_healthie_id = row.get("healthie_user_id")
                user_email = row.get("email")
                ch_user_id = row.get("ch_user_id")
                sm_user_id = row.get("sm_user_id")

                if user_healthie_id is str(11223186):
                    print("Dhaval thinks we can stop here")

                variables = {"id": str(user_healthie_id)}

                response = H.get_ids(variables)
                # print(response)

                if response["user"] is None:
                    print(f"User {user_healthie_id}:{user_email} does not exist")
                    continue

                current_record_id = response["user"]["record_identifier"]

                if current_record_id == ch_user_id:
                    print(
                        f"User {user_healthie_id}:{user_email} already has correct Cascaid ID: {ch_user_id}"
                    )
                    continue

                print(
                    f"User {user_healthie_id}:{user_email} record_identifier is: {current_record_id}"
                )
                print(f"should be: {ch_user_id}")

                variables = {
                    "id": user_healthie_id,
                    "record_identifier": ch_user_id,
                    "additional_record_identifier": "",
                }

                response = H.update_user_record_identifier(variables)
                # print(response, file = responses)

                if response["updateClient"]["messages"]:
                    print(
                        f"Error updating user id {user_healthie_id}: {response['updateClient']['messages']}"
                    )
                    error_count += 1
                    continue
                else:
                    user_id = response["updateClient"]["user"]["id"]
                    record_identifier = response["updateClient"]["user"][
                        "record_identifier"
                    ]
                    additional_record_identifier = response["updateClient"]["user"][
                        "additional_record_identifier"
                    ]
                    print(f"Updated user id:              {user_id}")
                    print(f"email:                        {user_email}")
                    print(f"record_identifier:            {record_identifier}")
                    print(
                        f"additional_record_identifier: {additional_record_identifier}"
                    )

                # {'user': {
                # 'id': '10961362',
                # 'record_identifier': '88e4e761-d2d3-4406-88b9-a47f4ce9a0b4',
                # 'additional_record_identifier': ''
                # },
                # 'messages': None}

                updated_count += 1

            print("Final tally")
            print(f"updated: {updated_count}, errors: {error_count}")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "log" in locals() and not log.closed:
            log.close()
            print("log closed.")


if __name__ == "__main__":
    main()
