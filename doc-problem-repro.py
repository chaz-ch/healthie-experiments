import requests
import json
from typing import Dict, Any, List
import random
import string

# --- Configuration ---
TARGET_GRAPHQL_URL = "https://staging-api.gethealthie.com/graphql"
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

AUTH_HEADERS = {
    "Authorization": f"Basic {API_KEY}",
    "AuthorizationSource": "API"
}

# Path to your PDF file
PDF_FILE_PATH = "test_document.pdf"

CLIENT_ID = 12345
PROVIDER_ID = 54321

CHAZ_AS_PATIENT = "4097532"
CHAZ_AS_PROVIDER = "3996427"

def _execute_upload_request(data: Dict[str, Any], files: Dict[str, Any],timeout: int = 10) -> Dict[str, Any]:

    """
    Internal core method to handle the POST request execution.
    This method is already built to handle any structure passed in the 'variables' dict.
    """
    
    try:
        response = requests.post(
            TARGET_GRAPHQL_URL, 
            data = data,
            files = files,
            headers = AUTH_HEADERS,
            timeout=timeout
        )

        response.raise_for_status() 
        
        data: Dict[str, Any] = response.json()
        
        if 'errors' in data:
            error_messages: List[str] = [err.get('message', 'Unknown GraphQL Error') for err in data['errors']]
            raise ValueError(f"GraphQL Query Error(s): {'; '.join(error_messages)}")

        return data

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API Request Error: {e}")

def create_document(variables: Dict[str, Any]) -> Dict[str, Any]:

    file = open(variables['file_path'], 'rb')

    inputs = {
        'file:': None, # Upload

        'display_name:': variables['display_name'], 
        'clients_ids:': variables['clients_ids'],
        'provider_ids:': variables['provider_ids'],
    }

    mutation = """
    mutation createDocument(
        $file: Upload, 
        $display_name: String, 
        $clients_ids: String,
        $provider_ids: [String],
        ) {
        createDocument(input: { 
        file: $file,
        display_name: $display_name,
        clients_ids: $clients_ids,
        provider_ids: $provider_ids,
        }) {
        document {
            id
        }
        messages {
            field
            message
        }
        }
    }
    """

    operations = json.dumps({
        "query": mutation,
        "variables": inputs
    })
    
    map = json.dumps({ "0": ["variables.file"] })

    data = {
        "operations": operations,
        "map": map
    }
    
    files = {
        "0" : file
    }
    
    response = _execute_upload_request(
        data,
        files
    )

    return response.get('data', {})

def main():
    """
    Main function to read the CSV file and process each row.
    """
    try:
        
        length = 16
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        variables = {
            'file_path': PDF_FILE_PATH, 
            'clients_ids': CHAZ_AS_PATIENT,
            'display_name': random_string, 
            'provider_ids': [CHAZ_AS_PROVIDER]
        }

        response = create_document(variables)
        print(response)

    except FileNotFoundError:
        print(f"Error: The file '{PDF_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
