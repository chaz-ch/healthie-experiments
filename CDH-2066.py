import csv
import requests
import random
import json
import random
import uuid
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number, generate_npi
from names_generator import generate_name

# --- Configuration ---
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your CSV file
CSV_FILE_PATH = "CDH-2066.csv"

def random_BreastDensity():

    random_ID = None
    BDs = {
        'Result::BreastDensity::Dense': '32349', 
        'Result::BreastDensity::NonDense': '32350'
    }
    
    BD = random.choice(list(BDs.keys()))
    random_ID = BDs[BD]
    
    return random_ID

def random_TCLifetimeRisk():

    random_ID = None
    TCLifetimeRisks = {
        'Result::TCLifetimeRisk::Average':      '32351',
        'Result::TCLifetimeRisk::High':         '32352',
        'Result::TCLifetimeRisk::Intermediate': '32353'
    }
    
    TCLifetimeRisk = random.choice(list(TCLifetimeRisks.keys()))
    random_ID = TCLifetimeRisks[TCLifetimeRisk]
    
    return random_ID
                
def random_BIRADS():

    random_ID = None
    BIRADS = {
        'Result::BIRADS::0': '32343', 
        'Result::BIRADS::1': '32344',
        'Result::BIRADS::2': '32345',
        'Result::BIRADS::3': '32346',
        'Result::BIRADS::4': '32347',
        'Result::BIRADS::5': '32348'
    }
    BIRAD = random.choice(list(BIRADS.keys()))
    random_ID = BIRADS[BIRAD]
    return random_ID

def random_BAC():
    random_ID = None
    BACs = {
        'Result::BAC::Absent': '32341', 
        'Result::BAC::Present': '32342'
    }
    BAC = random.choice(list(BACs.keys()))
    random_ID = BACs[BAC]
    return random_ID

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie(API_KEY)
    
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                
                random_uuid = str(uuid.uuid4())
                CHAZ_PROVIDER_ID = 3996427
                random_lastname = generate_name()
                random_digits = random.randint(1000000, 9999999)
                random_email = f"chazlarson+{random_digits}@gmail.com"

                variables = {
                    "first_name": row.get("firstname"),
                    "last_name": random_lastname,      # row.get("lastname"),
                    "email": random_email,             # row.get("email"),
                    "dietitian_id": str(CHAZ_PROVIDER_ID),
                    "skipped_email": not is_valid_email(random_email),
                    "phone_number": row.get("phone_number") if validate_phone_number(row.get("phone_number")) else None,
                    "dont_send_welcome": True,
                    "record_identifier": random_uuid,  # would be userid from CSV
                    "dob": convert_date_format(row.get("dateofbirth")),
                    "gender": standardize_gender(row.get("gender")),
                }

                # Must have - Phase 1: 
                #     Patient First name                       √
                #     Patient Last Name                        √
                #     Patient Email Address                    √
                #     Patient Phone Number                     √
                #     Patient Date of Birth                    √
                #     Patient Sex at Birth                     √
                #     Navigator Name [Helathie ID of Provider] √
                
                response = H.create_user(variables)
                print(response)
                # {'createClient': {'user': {'id': '4181385'}, 'messages': None}}
                try:
                    new_user_id = response['createClient']['user']['id']
                except Exception:
                    print("exiting")
                    exit()

                # Tags - Phase 1: 
                #     Tags - 
                #     1) Status: Created (Phase 1) 
                #     2) Patient Report Type (Phase 1) 
                #         MGP - Mammogram+ 
                #         MGPH - Mammogram + Heart 

                # As shown here:
                #     <https://cascaidhealth.atlassian.net/wiki/spaces/SRN/pages/140705795/Healthie+Tags>
                # these tags have been created in Healthie:
                # 'Status::Created':                      '32355'
                # 'ReportType::MGP':                      '32338'
                # 'ReportType::MGPH':                     '32339'
                
                CREATED_TAG = 32355
                MGPH_TAG = 32339
                
                # assign tags to that new user:
                response = H.assign_tag([CREATED_TAG, MGPH_TAG], new_user_id)
                print(response)

                # Nice to have Phase 1: 
                #     Patient Medical Data (As tags) 
                #          (Nice to have Phase 1) 
                #                 Patient Breast Density
                #                     Only one value would be sent
                #                     Potential Values: A, B, C, D
                # 'Result::BreastDensity::Dense':         '32349'
                # 'Result::BreastDensity::NonDense':      '32350'
                #                 Patient Lifetime Risk 
                #                     Only one value would be sent
                #                     Potential Values: Average, Intermediate, High 
                # 'Result::TCLifetimeRisk::Average':      '32351'
                # 'Result::TCLifetimeRisk::High':         '32352'
                # 'Result::TCLifetimeRisk::Intermediate': '32353'
                #                 Patient BIRAD Value
                #                     Only one value would be sent
                #                     Potential Values: 0, 1, 2, 3, 4, 5
                # 'Result::BIRADS::0':                    '32343'
                # 'Result::BIRADS::1':                    '32344'
                # 'Result::BIRADS::2':                    '32345'
                # 'Result::BIRADS::3':                    '32346'
                # 'Result::BIRADS::4':                    '32347'
                # 'Result::BIRADS::5':                    '32348'
                #                 Patient BAC Value
                #                     Only one value would be sent
                #                     Potential Values: Present, Absent 
                # 'Result::BAC::Absent':                  '32341'
                # 'Result::BAC::Present':                 '32342'

                # set some random values from those:
                response = H.assign_tag([random_BreastDensity(), random_TCLifetimeRisk(), random_BIRADS(), random_BAC()], new_user_id)
                print(response)

                # Nice to have Phase 1: 
                #     Referring Provider First Name (Nice to have Phase 1)
                #     Referring Provider Last Name (Nice to have Phase 1)
                #     Referring Provider NPI (Nice to have Phase 1)

                # These are the minimum fields required
                variables = {
                    "input": {
                        "first_name": generate_name(),
                        "last_name": generate_name(),
                        "npi": generate_npi(),
                    }
                }
        
                response = H.create_referring_physician(variables)
                print(response)
                # {'createReferringPhysician': {'duplicated_physician': None, 'messages': None, 'referring_physician': {'id': '42306', 'full_name': 'admiring_chaum competent_knuth', 'npi': '5654222254'}}}
                try:
                    if response['createReferringPhysician']['duplicated_physician']:
                        physician_id = response['createReferringPhysician']['duplicated_physician']['id']
                    elif response['createReferringPhysician']['referring_physician']:
                        physician_id = response['createReferringPhysician']['referring_physician']['id']
                    else:
                        exit()
                except Exception as e:
                    print(f"{e}")
                    exit()
        
                # reason not required
                variables = {
                    "input": {
                        # "referral_reason": "initial consult",
                        "referring_physician_id": physician_id,
                        "user_id": new_user_id
                    }
                }

                response = H.create_referral(variables)
                print(response)
                # {"data": {"createReferral": {"messages": null,"referral": {"id": "57421"}}}}
                
                # send welcome email
                variables = {
                    "id": new_user_id,
                    "resend_welcome": True,
                }
                
                response = H.update_user(variables)


    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
