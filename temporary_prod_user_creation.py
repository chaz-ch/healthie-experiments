import csv
import random
import uuid
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, validate_phone_number, generate_npi
from names_generator import generate_name

# Path to your CSV file
CSV_FILE_PATH = "interim_user_creation/patient_import_one.csv"

GLOBAL_PROVIDER_ID = 3996427 # this is chaz
# 3920603
SMI_INBOUND_GROUP_ID = 93581

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie("STAGE")
    
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:

                # Must have - Phase 1: 
                #     Patient First name                       √
                #     Patient Last Name                        √
                #     Patient Email Address                    √
                #     Patient Phone Number                     √
                #     Patient Date of Birth                    √
                #     Patient Sex at Birth                     √
                #     Navigator Name [Helathie ID of Provider] √
                
                variables = {
                    "first_name": str(row.get("firstname")).title(),
                    "last_name": str(row.get("lastname")).title(),
                    "email": row.get("email"),
                    "dietitian_id": str(GLOBAL_PROVIDER_ID),
                    "skipped_email": not is_valid_email(row.get("email")),
                    "phone_number": row.get("phone_number") if validate_phone_number(row.get("phone_number")) else None,
                    "dont_send_welcome": True,
                    "record_identifier": row.get("userid"),
                    "dob": convert_date_format(row.get("dateofbirth")),
                    "gender": standardize_gender(row.get("gender")),
                    "user_group_id": str(SMI_INBOUND_GROUP_ID)
                }

                print(variables)
                
                response = H.create_user(variables)
                print(response)

                new_user_id = None

                if response['createClient']['user']:
                # {'createClient': {'user': {'id': '4181385'}, 'messages': None}}
                    new_user_id = response['createClient']['user']['id']
                else:
                    # {'createClient': {'user': None, 'messages': [{'field': 'email', 'message': 'The email address that you entered already exists for your client Test McTest.'}]}}
                    if response['createClient']['messages']: 
                        if "The email address that you entered already exists" in response['createClient']['messages'][0]['message']:
                            # This person already exists in healthie
                            print("This person already exists in healthie, let's find them:")
                            
                            response = H.get_user_by_email(str(row.get("email")))
                            print(response)

                            if len(response['users']) > 0:
                                new_user_id = response['users'][0]['id']
                                # now we need to update the user with the other information
                                variables["id"] = new_user_id
                                variables.pop("dietitian_id") # ERROR: "Clients cannot get assigned to a support member"

                                response = H.update_user(variables)
                                print(response)

                                print(f"Updated user id {new_user_id}")
                            else:
                                print("No user found, even though creation failed")
                                print("exiting")
                                exit()

                        else:
                            print(response)
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
                
                CREATED_TAG = "32355"
                
                if row.get("reporttype") == "MGP":
                    REPORT_TYPE_TAG = "32338"
                else:
                    REPORT_TYPE_TAG = "32339"
                
                print(f"{row.get("reporttype")}: {REPORT_TYPE_TAG}")                

                # assign tags to that new user:
                response = H.assign_tag([CREATED_TAG, REPORT_TYPE_TAG], new_user_id)
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

                BD = row.get("breastdensity")
                if BD in ["C", "D"]:
                    BREAST_DENSITY_TAG = "32349"
                elif BD in ["A", "B"]:
                    BREAST_DENSITY_TAG = "32350"
                else:
                    BREAST_DENSITY_TAG = None

                print(f"{row.get("breastdensity")}: {BREAST_DENSITY_TAG}")
                
                if BREAST_DENSITY_TAG:
                    response = H.assign_tag([BREAST_DENSITY_TAG], new_user_id)
                    print(response)
                else:
                    print("No breast density tag to assign")

                ltr = float(str(row.get("lifetimerisknbr")))
                
                if ltr >= 20:
                    LIFETIME_RISK_TAG = "32352"
                elif ltr >= 15:
                    LIFETIME_RISK_TAG = "32353"
                else:
                    LIFETIME_RISK_TAG = "32351"

                print(f"{row.get("lifetimerisknbr")}: {LIFETIME_RISK_TAG}")
                
                response = H.assign_tag([LIFETIME_RISK_TAG], new_user_id)
                print(response)

                if row.get("birad") == "0":
                    BIRAD_TAG = "32343"
                elif row.get("birad") == "1":
                    BIRAD_TAG = "32344"
                elif row.get("birad") == "2":
                    BIRAD_TAG = "32345"
                elif row.get("birad") == "3":   
                    BIRAD_TAG = "32346"
                elif row.get("birad") == "4":   
                    BIRAD_TAG = "32347"
                else:
                    BIRAD_TAG = "32348"
                    
                print(f"{row.get("birad")}: {BIRAD_TAG}")
                
                response = H.assign_tag([BIRAD_TAG], new_user_id)
                print(response)
                
                if row.get("bac") == "Detected":
                    BAC_TAG = "32342"
                elif row.get("bac") == "Not Detected":
                    BAC_TAG = "32341"
                else:
                    BAC_TAG = None

                print(f"{row.get("bac")}: {BAC_TAG}")

                if BAC_TAG:
                    response = H.assign_tag([BAC_TAG], new_user_id)
                    print(response)
                else:
                    print("No BAC tag to assign")

                # Nice to have Phase 1: 
                #     Referring Provider First Name (Nice to have Phase 1)
                #     Referring Provider Last Name (Nice to have Phase 1)
                #     Referring Provider NPI (Nice to have Phase 1)

                # These are the minimum fields required
                variables = {
                    "input": {
                        "first_name": str(row.get("referring_provider_first_nm")).title(),
                        "last_name": str(row.get("referring_provider_last_nm")).title(),
                        "npi": row.get("referring_provider_npi_nbr"),
                    }
                }

                print(variables)
                
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
                        "referral_reason": "client setup",
                        "referring_physician_id": physician_id,
                        "user_id": new_user_id
                    }
                }

                print(variables)
                
                response = H.create_referral(variables)
                print(response)
                # {"data": {"createReferral": {"messages": null,"referral": {"id": "57421"}}}}
                
                try:
                    referral_id = response['createReferral']['referral']['id']
                except Exception as e:
                    print(f"{e}")
                    exit()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      


    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
