from modules.healthie import Healthie


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
    
    for client in CLIENTS_WITH_PROVIDER:
        try:
            variables = {
                'file_path': PDF_FILE_PATH, 
                'clients_ids': client,
                'display_name': None, 
                'provider_ids': [f"{CLIENTS_WITH_PROVIDER[client]}"]
            }

            # folder_id = None,
            # care_plan_id = None,
            # course_id = None,
            # description = None,
            # file_string = None,
            # from_date = None,
            # from_program_create = False,
            # generate_ccda_for_rel_user_id = False,
            # generate_human_readable_ccda_for_rel_user_id = False,
            # include_in_charting = False,
            # is_photo_id = False,
            # metadata = None,
            # on_form_for_user_id = None,
            # org_level = False,
            # payout_id = None,
            # rcf_id = None,
            # rel_user_id = None,
            # report_type = None,
            # share_users = None,
            # share_with_rel = False,
            # to_date = None

            response = H.create_document(variables)
            print(response)

        except FileNotFoundError:
            print(f"Error: The file '{PDF_FILE_PATH}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

{'createClient': {'user': {'id': '4053342'}, 'messages': None}}
{'createClient': {'user': {'id': '4053349'}, 'messages': None}}
{'createClient': {'user': {'id': '4053351'}, 'messages': None}}
{'createClient': {'user': {'id': '4053352'}, 'messages': None}}

{'createDocument': {'document': {'id': '601421'}, 'messages': None}}
