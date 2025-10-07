import glob, os, re, signal, sys, time
from datetime import datetime, timedelta
# from num2words import num2words
# from pathvalidate import is_valid_filename, sanitize_filename
# from plexapi.audio import Album, Track
# from plexapi.video import Season, Episode, Movie
from requests.exceptions import HTTPError
# from tenacity import retry_if_exception
# from tenacity.wait import wait_base
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException
import base64


# class TimeoutExpired(Exception):
# class TimeoutExpired(Exception):
#     pass

# class LimitReached(Exception):
#     pass

# class Failed(Exception):
#     pass

# class FilterFailed(Failed):
#     pass

# class Continue(Exception):
#     pass

# class Deleted(Exception):
#     pass

# class NonExisting(Exception):
#     pass

# class NotScheduled(Exception):
#     pass

# class NotScheduledRange(NotScheduled):
#     pass


# class retry_if_http_429_error(retry_if_exception):

#     def __init__(self):
#         def is_http_429_error(exception: BaseException) -> bool:
#             return isinstance(exception, HTTPError) and exception.response.status_code == 429

#         super().__init__(predicate=is_http_429_error)


# class wait_for_retry_after_header(wait_base):
#     def __init__(self, fallback):
#         self.fallback = fallback

#     def __call__(self, retry_state):
#         exc = retry_state.outcome.exception()
#         if isinstance(exc, HTTPError):
#             retry_after = exc.response.headers.get("Retry-After", None)
#             try:
#                 if retry_after is not None:
#                     return int(retry_after)
#             except (TypeError, ValueError):
#                 pass

#         return self.fallback(retry_state)


# days_alias = {
#     "monday": 0, "mon": 0, "m": 0,
#     "tuesday": 1, "tues": 1, "tue": 1, "tu": 1, "t": 1,
#     "wednesday": 2, "wed": 2, "w": 2,
#     "thursday": 3, "thurs": 3, "thur": 3, "thu": 3, "th": 3, "r": 3,
#     "friday": 4, "fri": 4, "f": 4,
#     "saturday": 5, "sat": 5, "s": 5,
#     "sunday": 6, "sun": 6, "su": 6, "u": 6
# }
# mod_displays = {
#     "": "is", ".not": "is not", ".is": "is", ".isnot": "is not", ".begins": "begins with", ".ends": "ends with", ".before": "is before", ".after": "is after",
#     ".gt": "is greater than", ".gte": "is greater than or equal", ".lt": "is less than", ".lte": "is less than or equal", ".regex": "is"
# }
# pretty_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
# lower_days = {v.lower(): k for k, v in pretty_days.items()}
# pretty_months = {
#     1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
#     7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
# }
# lower_months = {v.lower(): k for k, v in pretty_months.items()}
# seasons = ["current", "winter", "spring", "summer", "fall"]
# advance_tags_to_edit = {
#     "Movie": ["metadata_language", "use_original_title", "credits_detection"],
#     "Show": ["episode_sorting", "keep_episodes", "delete_episodes", "season_display", "episode_ordering", "metadata_language", "use_original_title", "credits_detection", "audio_language", "subtitle_language", "subtitle_mode"],
#     "Season": ["audio_language", "subtitle_language", "subtitle_mode"],
#     "Artist": ["album_sorting"]
# }
# tags_to_edit = {
#     "Movie": ["genre", "label", "collection", "country", "director", "producer", "writer"],
#     "Video": ["genre", "label", "collection", "country", "director", "producer", "writer"],
#     "Show": ["genre", "label", "collection"],
#     "Artist": ["genre", "label", "style", "mood", "country", "collection", "similar_artist"]
# }
# collection_mode_options = {
#     "default": "default", "hide": "hide",
#     "hide_items": "hideItems", "hideitems": "hideItems",
#     "show_items": "showItems", "showitems": "showItems"
# }
# image_content_types = ["image/png", "image/jpeg", "image/webp"]
# parental_types = {"Sex & Nudity": "Nudity", "Violence & Gore": "Violence", "Profanity": "Profanity", "Alcohol, Drugs & Smoking": "Alcohol", "Frightening & Intense Scenes": "Frightening"}
# parental_values = ["None", "Mild", "Moderate", "Severe"]
# parental_levels = {"none": [], "mild": ["None"], "moderate": ["None", "Mild"], "severe": ["None", "Mild", "Moderate"]}
# parental_labels = [f"{t}:{v}" for t in parental_types.values() for v in parental_values]
# previous_time = None
# start_time = None

def validate_phone_number(number_str, country_code=None):
    """
    Validates a phone number using the phonenumbers library.

    Args:
        number_str (str): The phone number string (e.g., '650 253 0000', '+16502530000').
        country_code (str, optional): The default country code (e.g., 'US')
                                      to use if the number is missing a prefix.

    Returns:
        bool: True if the number is valid, False otherwise.
    """
    try:
        # Parse the number, which converts the string into a PhoneNumber object
        # The 'country_code' is a hint for non-international numbers
        parsed_number = phonenumbers.parse(number_str, country_code)
        
        # Check if the number is valid based on length, prefix, and region.
        return phonenumbers.is_valid_number(parsed_number)
        
    except NumberParseException:
        # This exception is raised if the string cannot be parsed at all 
        # (e.g., contains too many letters).
        return False

def to_boolean_any(s):
    """
    Converts a boolean-like string to a Boolean.
    Returns None if the string is not recognized.
    """
    if not isinstance(s, str):
        # Handle non-string inputs (e.g., already a bool, int, or None)
        return bool(s)

    # Normalize the string for case-insensitive matching
    normalized_s = s.strip().lower()

    # Define the mapping for True and False values
    true_values = ('true', 't', 'yes', 'y', 'on', '1')
    false_values = ('false', 'f', 'no', 'n', 'off', '0')

    if normalized_s in true_values:
        return True
    elif normalized_s in false_values:
        return False
    else:
        # Return None or raise a ValueError for unhandled strings
        return None

def is_valid_email(email):
    """
    Checks email validity using the robust email_validator library.
    This also includes basic DNS checks on the domain by default.
    """
    try:
        # Validate the email. This raises an error if it fails.
        # It can also return a normalized email address.
        validate_email(email, check_deliverability=True)
        return True
    except EmailNotValidError as e:
        # print(str(e)) # Optional: print the reason for failure
        return False

def convert_date_format(date_string):
    """
    Converts a date string from "MM/DD/YYYY" to "YYYY-MM-DD".

    Args:
        date_string (str): The date string in "MM/DD/YYYY" format.

    Returns:
        str: The converted date string in "YYYY-MM-DD" format.
    """
    # 12/12/12
    bits = date_string.split('/')
    year = f"20{bits[2]}" if int(bits[2]) < 26 else f"19{bits[2]}"
    
    date_string = f"{bits[0]}/{bits[1]}/{year}"    
    try:
        # Parse the input date string
        datetime_object = datetime.strptime(date_string, "%m/%d/%Y")
        # Format the datetime object to the new format
        new_date_string = datetime_object.strftime("%Y-%m-%d")
        return new_date_string
    except ValueError as e:
        return f"Error: {e}"

def standardize_gender(gender_string):
    """
    Converts various string representations of "female" to "Female".

    Args:
        gender_string (str): The string to standardize.

    Returns:
        str: The standardized string, or the original string if no match is found.
    """
    if gender_string.lower() in ["f", "female"]:
        return "Female"
    if gender_string.lower() in ["m", "male"]:
        return "Male"
    else:
        # For this example, we return the original string if it doesn't match.
        return gender_string

def file_to_base64(filepath):
    """
    Converts a local PDF file to a Base64 string.
    """
    try:
        # 1 & 2: Open and read the PDF file as bytes
        with open(filepath, "rb") as input_file:
            file_bytes = input_file.read()

        # 3: Base64 encode the bytes
        encoded_bytes = base64.b64encode(file_bytes)

        # 4: Decode the Base64 bytes into a regular string
        base64_string = encoded_bytes.decode('utf-8')

        return base64_string
    except FileNotFoundError:
        return f"Error: File not found at {filepath}"
    except Exception as e:
        return f"An error occurred: {e}"
