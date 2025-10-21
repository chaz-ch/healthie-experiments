from modules.healthie import Healthie
from names_generator import generate_name

# --- Configuration ---
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your PDF file
PDF_FILE_PATH = "test_document.pdf"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

CHAZ_AS_PATIENT = 4097532
CHAZ_AS_PROVIDER = 3996427

CLIENTS_WITH_PROVIDER = {
    '4053342': 3920603,
    '4053349': 3920603,
    '4053351': 3970418,
    '4053352': 3970418,
}

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie("STAGE")

    try:

        variables = {
            "id": str(CHAZ_AS_PATIENT)
        }
        
        response = H.get_doc_share_id(variables)
        doc_share_id = response['user']['doc_share_id']

        variables = {
            'simple_added_users': doc_share_id,
            'conversation_name': generate_name(), 
            'owner_id': CHAZ_AS_PROVIDER,
            'initial_message': f"Hello, {CHAZ_AS_PATIENT}, I am your navigator, {CHAZ_AS_PROVIDER}"
        }

        response = H.create_conversation(variables)
        print(response)

        conversation_id = response['createConversation']['conversation']['id']

        variables = {
            "content": "This is a test message from the owner of the API Key",
            "conversation_id": conversation_id,
            "user_id": CHAZ_AS_PATIENT,
            "org_chat": True,
            "hide_org_chat_confirmation": True
        }

        response = H.create_note(variables)
        print(response)

    except FileNotFoundError:

        print(f"Error: The file '{PDF_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# {'createClient': {'user': {'id': '4053342'}, 'messages': None}} true
# {'createClient': {'user': {'id': '4053349'}, 'messages': None}} false
# {'createClient': {'user': {'id': '4053351'}, 'messages': None}} true
# {'createClient': {'user': {'id': '4053352'}, 'messages': None}} false

# {'createDocument': {'document': {'id': '601421'}, 'messages': None}}
