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

CHARTING_TEMPLATE = 2224075
INTAKE_TEMPLATE = 2224074
PROGRAM_TEMPLATE = 2224076

# Answer fields:
            # "label": "short-answer",
            # "mod_type": "text",
            # "label": "pick-some",
            # "mod_type": "checkbox",
            # "label": "birthdate",
            # "mod_type": "date",
            # "label": "lunch-hour",
            # "mod_type": "time",
            # "label": "dog-count",
            # "mod_type": "number",
            # "label": "favorite-guy",
            # "mod_type": "dropdown",

# Field IDs:

# "id": "2224075",
# "name": "test-charting",

# "19104587"  "test-charting-form"    "label",
# "19104590"  "short-answer"          "text",
# "19104591"  "pick-some"             "checkbox",
# "19104592"  "birthdate"             "date",
# "19104593"  "lunch-hour"            "time",
# "19104594"  "dog-count"             "number",
# "19104595"  "favorite-guy"          "dropdown",

# "id": "2224074",
# "name": "test-intake",

# "19104596"  "intake-form"   "label",
# "19104579"  "short-answer"  "text",
# "19104581"  "pick-some"     "checkbox",
# "19104583"  "birthdate"     "date",
# "19104584"  "lunch-hour"    "time",
# "19104585"  "dog-count"     "number",
# "19104586"  "favorite-guy"  "dropdown",

# "id": "2224076",
# "name": "test-program",

# "19104597"  "test-program"  "label",
# "19104598"  "short-answer"  "text",
# "19104600"  "pick-one"      "radio",
# "19104601"  "birth-date"    "date",
# "19104602"  "lunch-hour"    "time",
# "19104603"  "dog-count"     "number",
# "19104604"  "favorite-guy"  "dropdown",

# Charting form answers being set:
    #   {"answer":"answer-text","conditional_custom_module_id":null,"filter_type":null,"id":"12966499","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104590"},
    #   {"answer":"bing\\r\\nboing","conditional_custom_module_id":null,"filter_type":null,"id":"12966500","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104591"},
    #   {"answer":"2025-10-14","conditional_custom_module_id":null,"filter_type":null,"id":"12966501","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104592"},
    #   {"answer":"2025-10-07T21:10:00.769Z","conditional_custom_module_id":null,"filter_type":null,"id":"12966502","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104593"},
    #   {"answer":"678","conditional_custom_module_id":null,"filter_type":null,"id":"12966503","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104594"},
    #   {"answer":"geezer","conditional_custom_module_id":null,"filter_type":null,"id":"12966504","user_id":"4097532","value_to_filter":null,"custom_module_id":"19104595"}],

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

# {'user': {'id': '4097532', 'doc_share_id': 'user-4097532'}}

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
