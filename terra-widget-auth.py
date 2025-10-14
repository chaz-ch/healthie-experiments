from modules.healthie import Healthie
from names_generator import generate_name
import requests

# --- Configuration ---
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

TERRA_URL = "https://api.tryterra.co/v2/"
TERRA_DEV_ID = "cascaidhealth-testing-d1h71YqtMH"
TERRA_API_KEY = "r_laSpk1CGnVhoxp-Z4gMfLTWqFvyN5C"

TERRA_SUCCESS_URL = "https://cascaid.com"
TERRA_FAILURE_URL = "https://cascaid.com"

CHAZ_AS_PATIENT = 4097532
CHAZ_AS_PROVIDER = 3996427

def get_ids(client_id):
    H = Healthie(API_KEY)

    variables = {
        "id": str(client_id)
    }
    
    response = H.get_ids(variables)
    doc_share_id = response['user']['doc_share_id']
    record_identifier = response['user']['record_identifier']
    user_name = response['user']['name']
    
    return doc_share_id, record_identifier, user_name

def connect_to_terra(healthie_user_id: int):

    ENDPOINT = "auth/generateWidgetSession"
    TERRA_TARGET_URL = f"{TERRA_URL}{ENDPOINT}"

    TERRA_HEADERS = {
        "Content-Type": "application/json",
        "Dev-Id": TERRA_DEV_ID,
        "X-Api-Key": TERRA_API_KEY
    }

    doc_share_id, record_identifier, user_name = get_ids(healthie_user_id)

    TERRA_REQUEST_DATA = {
          "providers": "GARMIN,FITBIT,OURA,WITHINGS,SUUNTO",
          "language": "en",
          "reference_id": record_identifier,
          "auth_success_redirect_url": TERRA_SUCCESS_URL,
          "auth_failure_redirect_url": TERRA_FAILURE_URL
        }

    response = requests.post(
        TERRA_TARGET_URL,
        headers=TERRA_HEADERS,
        json=TERRA_REQUEST_DATA
    )
    response.raise_for_status()

    return response.json()

def send_terra_url_to_user(client_id, provider_id, terra_url):

    doc_share_id, record_identifier, user_name = get_ids(client_id)

    variables = {
        'simple_added_users': doc_share_id,
        'conversation_name': generate_name(), 
        'owner_id': provider_id,
        'initial_message': f"Hello, {user_name}, connect your mobile device by going to this URL: {terra_url}"
    }

    H = Healthie(API_KEY)
    response = H.create_conversation(variables)
    print(response)


def main():

    details = connect_to_terra(CHAZ_AS_PATIENT)
    
    if details["status"] != "success":
        print(details["status"])
    else:
        terra_widget_url = details["url"]
        print(terra_widget_url)

    send_terra_url_to_user(CHAZ_AS_PATIENT, CHAZ_AS_PROVIDER, terra_widget_url)

if __name__ == "__main__":
    main()
