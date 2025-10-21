from modules.healthie import Healthie


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
    H = Healthie("STAGE")
    
    for client in CLIENTS_WITH_PROVIDER:
        try:
            variables = {
                'file_path': PDF_FILE_PATH, 
                'clients_ids': client,
                'display_name': None, 
                'provider_ids': CLIENTS_WITH_PROVIDER[client]
            }

            # attached_audio · Upload
            # attached_document · Upload
            # attached_image · Upload
            # attached_image_string · String
            # content · String
            # conversation_id · String
            # created_at · String
            # hide_org_chat_confirmation · Boolean
            # org_chat · Boolean · True, if a note create action called in the organization chat context
            # scheduled_at · String
            # updated_at · String
            # user_id · String

            response = H.create_document(variables)
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

{'createDocument': {'document': {'id': '601421'}, 'messages': None}}

# Me as provider:
    #   {
    #     "id": "3996427",
    #     "first_name": "Chaz",
    #     "last_name": "Larson",
    #     "email": "chaz@cascaidhealth.com",
    #     "has_api_access": true
    #   },
