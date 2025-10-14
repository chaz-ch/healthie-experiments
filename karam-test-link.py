import csv
import requests
import json
import random
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number
import uuid


# --- Configuration ---
# Your Healthie API Key
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your CSV file
CSV_FILE_PATH = "cz_mammo_plus_heart_new4.csv"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie(API_KEY)
    
    try:
                
        variables = {
            "first_name": "Karam",
            "last_name": "The Tester",
            "email": "",
            "dietitian_id": "3996427",
            "skipped_email": True,
            "phone_number": "204-998-1319",
            "dont_send_welcome": True,
            "record_identifier": str(uuid.uuid4()),
            "dob": "1962-04-08",
            "gender": "Male",
            "other_provider_ids": [f"{random.randint(1000000, 9999999)}"]
        }
        
        response = H.create_user(variables)

        new_user_id = response['createClient']['user']['id']
        print (f"created user id {new_user_id}")

        response = H.get_user_signup_link(new_user_id)
        
        signup_link = response['user']['set_password_link']
        print (f"signup link {signup_link}")
        
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
