from modules.healthie import Healthie
from names_generator import generate_name

# --- Configuration ---
# Your GraphQL API endpoint URL
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your PDF file
PDF_FILE_PATH = "test_document.pdf"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

CLIENT_ID = 12345
PROVIDER_ID = 54321

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
    H = Healthie(API_KEY)

    try:

        variables = {
            'file_path': PDF_FILE_PATH, 
            'client_id': '4097532',
            'conversation_name': generate_name(), 
            'owner_id': "3996427"
        }


        response = H.create_conversation(variables)
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
