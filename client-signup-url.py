import csv
import requests
import json
import random
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number


# --- Configuration ---
# Your GraphQL API endpoint URL
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your CSV file
CSV_FILE_PATH = "cz_mammo_plus_heart_new4.csv"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

def main():

    H = Healthie(API_KEY)
    
    try:
                
        variables = {
            "id": None
        }
        
        variables["id"] = '4108931'

        response = H.get_signup_url(variables)
        print(response)

        variables["id"] = '4053352'

        response = H.get_signup_url(variables)
        print(response)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
