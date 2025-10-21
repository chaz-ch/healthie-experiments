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

    H = Healthie("STAGE")

    try:
        variables = {
            'offset': None,
            'keywords': None,
            'folder_id': None,
            'file_types': None,
            'file_type': None,
            'sort_by': None,
            'private_user_id': None,
            'viewable_user_id': None,
            'consolidated_user_id': None,
            'filter': None,
            'should_paginate': None,
            'for_template_use': None,
            'provider_id': None
        }

        response = H.list_documents(variables)
        print(response)

    except FileNotFoundError:
        print(f"Error: The file '{PDF_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
