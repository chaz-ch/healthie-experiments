import csv
import requests
import json
import random
import pprint
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number
from names_generator import generate_name

# --- Configuration ---
# Your GraphQL API endpoint URL
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"


tags = [
    'Chart::ChartCreated',
    'Chart::OrderCreated',
    'Consent::TelemedicineSigned',
    'Engagement::Responsive',
    'Engagement::Unresponsive',
    'ReportType::MGP',
    'ReportType::MGPH',
    'ReportType::StandardMG',
    'Result::BAC::Absent',
    'Result::BAC::Present',
    'Result::BIRADS::0',
    'Result::BIRADS::1',
    'Result::BIRADS::2',
    'Result::BIRADS::3',
    'Result::BIRADS::4',
    'Result::BIRADS::5',
    'Result::BreastDensity::Dense',
    'Result::BreastDensity::NonDense',
    'Result::TCLifetimeRisk::Average',
    'Result::TCLifetimeRisk::High',
    'Result::TCLifetimeRisk::Intermediate',
    'Status::Accessed',
    'Status::Created',
    'Status::Invited'
]

tags_created = {}

def main():

    H = Healthie(API_KEY)
    
    try:
        for tag in tags:

            inputs = {
                'name': tag
            }

            response = H.create_tag(inputs)
            print(response)
            # {'createTag': {'tag': None, 'messages': [{'field': 'name', 'message': 'has already been taken'}]}}

            if response['createTag']['tag'] is not None:
                new_tag_id = response['createTag']['tag']['id']
                print (f"created tag id {new_tag_id}")
                
                tags_created[tag] = new_tag_id
            else:
                tags_created[tag] = response['createTag']['messages']

        # Now we've created a bunch of tags
        pprint.pprint(tags_created)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


