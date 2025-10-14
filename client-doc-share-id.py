import csv
import requests
import json
import random
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number


# --- Configuration ---
# Your Healthie API Key
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

CHAZ_AS_PATIENT = 4097532
CHAZ_AS_PROVIDER = 3996427

def main():

    H = Healthie(API_KEY)
    
    try:
                
        variables = {
            "id": None
        }
        
        variables["id"] = str(CHAZ_AS_PATIENT)

        response = H.get_ids(variables)
        print(response)

        variables["id"] = str(CHAZ_AS_PROVIDER)

        response = H.get_ids(variables)
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
