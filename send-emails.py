import csv
import datetime
from modules.healthie import Healthie


# Path to your CSV file
CSV_FILE_PATH = "prod-welcome-emails.csv"
EXCLUSION_FILE_PATH = "prod-welcome-exclusions.csv"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

TARGET_ENV = "PROD"


def log_this(this, there):
    print(this)
    print(this, file=there)


def main():
    H = Healthie(TARGET_ENV)

    rt_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = open(f"user_actions-{TARGET_ENV}-{rt_str}.txt", "a")
    # responses = open(f"api_responses-{TARGET_ENV}-{rt_str}.txt", "a")

    try:
        exclusion_list = []
        sent_list = []

        with open(EXCLUSION_FILE_PATH, "r", newline="") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                exclusion_list.append(row)

        with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as csv_file:
            # Use DictReader to read each row as a dictionary
            csv_reader = csv.reader(csv_file)

            # Loop through each row in the CSV file
            for row in csv_reader:
                the_email = row[0]

                if the_email in exclusion_list:
                    log_this(f"Excluding {the_email}", log)
                    continue

                the_user = H.find_users_by_keywords(the_email)
                try:
                    the_id = the_user["users"][0]["id"]
                    # print(f"{the_id} : {the_email}")
                except Exception as e:
                    log_this(f"         : {the_email} Error: {e}", log)
                    continue

                if the_id in sent_list:
                    log_this(f"{the_id} : {the_email} Already sent", log)
                    continue

                variables = {
                    "id": the_id,
                    "resend_welcome": True,
                }

                sent_list.append(the_id)
                log_this(f"{the_id} : {the_email} Sending welcome email", log)

                response = H.update_user(variables)
                log_this(response, log)

    except FileNotFoundError:
        print("Error: a file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
