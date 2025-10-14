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
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            # Use DictReader to read each row as a dictionary
            csv_reader = csv.DictReader(csv_file)
            
            # Loop through each row in the CSV file
            for row in csv_reader:
                # The 'row' variable is a dictionary: {'name': '...', 'email': '...'}
                # create_client(row)
                # 
                # patientid,
                # masterid,
                # userid,
                # orderid,
                # orderdt,
                # firstname,
                # lastname,
                # dateofbirth,
                # gender,
                # birad,
                # lifetimerisk,
                # lifetimerisknbr,
                # breastdensity,
                # menarcheage,
                # firstchildbirthage,
                # hrtusage,
                # age,
                # height,
                # weight,
                # race,
                # ashkenazijewish,
                # hispanic,
                # brca1probability,
                # brca2probability,
                # populationlifetimerisk,
                # riskreversalpotential,
                # mammogramcompleteddate,
                # breastdensityrmloimageurl,
                # breastdensitylmloimageurl,
                # breastdensityimageurl,
                # breastdensityimagetype,
                # bacscanimageurl,
                # bodyiq,
                # testimonials,
                # email,
                # phonenumber,
                # bac,
                # appttyperefcd,
                # appttypegrpcd,
                # appttyperefnm,
                # appttyperefdesc,
                # cptcd1,
                # cptcd2,
                # cptcd3,
                # modalitynbr,
                # reporttypedesc,
                # reporttype,
                # dietitian_id,       # CHAZ ADDED
                # dont_send_welcome,  # CHAZ ADDED
                # other_provider_ids  # CHAZ ADDED
                
                variables = {
                    "first_name": row.get("firstname"),
                    "last_name": row.get("lastname"),
                    "email": row.get("email"),
                    "dietitian_id": row.get("dietitian_id"),
                    "skipped_email": not is_valid_email(row.get("email")),
                    "phone_number": row.get("phone_number") if validate_phone_number(row.get("phone_number")) else None,
                    "dont_send_welcome": to_boolean_any(row.get("dont_send_welcome")),
                    "record_identifier": row.get("userid"),
                    "dob": convert_date_format(row.get("dateofbirth")),
                    "gender": standardize_gender(row.get("gender")),
                    "other_provider_ids": [f"{random.randint(1000000, 9999999)}"]
                }
                
                response = H.create(variables)
                print(response)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
