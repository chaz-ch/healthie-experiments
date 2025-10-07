import csv
import requests
import json
import random
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number
from names_generator import generate_name

# --- Configuration ---
# Your GraphQL API endpoint URL
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"


def main():

    H = Healthie(API_KEY)
    
                
    try:
        response = H.list_tags()
        print(response)

        sample_user_id = '4037175'
        # '31050'

        inputs = {
            'name': generate_name()
        }

        response = H.create_tag(inputs)
        print(response)
        
        # {'createTag': {'tag': None, 'messages': [{'field': 'name', 'message': 'has already been taken'}]}}
        new_tag_id = response['createTag']['tag']['id']
        print (f"created tag id {new_tag_id}")
        
        # user: 4037175
        response = H.assign_tag([new_tag_id], sample_user_id)
        print(response)
        
        response = H.list_tags_with_users()
        print(response)
        
        response = H.remove_tag(new_tag_id, sample_user_id)
        print(response)
        
        response = H.list_tags_with_users()
        print(response)

        response = H.delete_tag(new_tag_id)
        print(response)

        response = H.list_tags()
        print(response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
