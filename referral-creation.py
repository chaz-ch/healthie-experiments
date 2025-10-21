from modules.healthie import Healthie
from modules.util import generate_npi
from names_generator import generate_name

# --- Configuration ---
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie("STAGE")
    
    CHAZ_AS_PATIENT = 4097532
    
    try:

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
            if response['duplicated_physician']:
                physician_id = response['duplicated_physician']['id']
            elif response['referring_physician']:
                physician_id = response['referring_physician']['id']
            else:
                exit()
        except Exception as e:
            print(f"{e}")
            exit()
        
        variables = {
            "input": {
                "referral_reason": "initial consult",
                "referring_physician_id": physician_id,
                "user_id": CHAZ_AS_PATIENT
            }
        }

        response = H.create_referral(variables)
        print(response)
        # {"data": {"createReferral": {"messages": null,"referral": {"id": "57421"}}}}
        

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
