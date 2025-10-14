import csv
import requests
import json
import random
from datetime import datetime
from modules.healthie import Healthie
from modules.util import convert_date_format, standardize_gender, is_valid_email, to_boolean_any, validate_phone_number


# --- Configuration ---
# Your Healthie API Key
API_KEY = "gh_sbox_vRYSSCYeu4n1G05EAXyc0KxWumBGYTQcXKCeaT34dmWKJWrFvWjq11Hn2sxnyy7a"

# Path to your CSV file
CSV_FILE_PATH = "cz_mammo_plus_heart_new4.csv"
# CSV_FILE_PATH = "cz_mammo_plus.csv"
# CSV_FILE_PATH = "cz_mammo_plus_heart.csv"

def main():
    """
    Main function to read the CSV file and process each row.
    """
    H = Healthie(API_KEY)
    
    CHAZ_PATIENT="4097532"
    CHAZ_PROVIDER="3996427"
    
    try:

            # assignee_ids · [ID!] · IDs of the users assigned to this task
            # client_id · String · The identifier of the client (patient) associated with this task
            # complete · Boolean Optional. Set to true if the Task is already complete
            # completed_by_id · ID
            # $content: String 	Content of the Task
            # created_by_id · String · The ID of the user (provider or staff member) who is listed as creating the task
            # $due_date: String Optional. A due date of the Task
            # note_id · ID
            # $priority: Int 0 or 1
            # $reminder: TaskReminderInput
            #   reminder.is_enabled	Set to true to enable the reminder, false otherwise
            #   reminder.reminder_time	Time, expressed in number of minutes from midnight, to trigger the reminder at
            #   reminder.interval_type	Frequency of the reminder. Possible options are:
            #     daily
            #     weekly
            #     once - default
            #   reminder.interval_value	Date when to trigger the reminder
            # seen · Boolean


        variables = {
            "content": "Here's a Task",
            "priority": 0,
            "client_id": CHAZ_PATIENT,
            "due_date": None,
            "reminder": None,
            "assignee_ids": [CHAZ_PROVIDER],
            "complete": False,
            "created_by_id": CHAZ_PROVIDER,
            "note_id": None,
            "seen": False
        }
        
        response = H.create_task(variables)
        print(response)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
