from modules.healthie import Healthie


# Path to your CSV file
CSV_FILE_PATH = "cz_mammo_plus_heart_new4.csv"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"


def main():
    H = Healthie("STAGE")

    try:
        variables = {
            "id": "",
            "first_name": None,
            "last_name": None,
            "legal_name": None,
            "email": None,
            "active": None,
            "additional_phone_number": None,
            "additional_record_identifier": None,
            "current_email": None,
            "dietitian_id": None,
            "dob": None,
            "gender": None,
            "phone_number": None,
            "resend_welcome": None,
            "send_form_request_reminder": None,
            "skipped_email": None,
            "timezone": None,
            "user_group_id": None,
        }

        variables["id"] = "4363493"
        # variables["resend_welcome"] = True

        response = H.update_user(variables)
        print(response)

        # variables["id"] = '4053352'

        # response = H.update_user(variables)
        # print(response)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
