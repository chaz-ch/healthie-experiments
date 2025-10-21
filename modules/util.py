import random
import base64
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException


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

def generate_npi():
    """
    Generates a random, valid 10-digit National Provider Identifier (NPI).

    The NPI is generated according to the Luhn algorithm for checksum validation.
    """
    # 1. Generate the first 9 digits. The first digit must be between 1 and 8.
    # The prefix 80840 is a constant part of the NPI calculation.
    prefix = '80840'
    
    # Generate 9 random digits for the main identifier part.
    # The first digit of an NPI cannot be 0, so we start with a choice from 1-8.
    first_digit = str(random.randint(1, 8))
    middle_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    nine_digits = first_digit + middle_digits

    # 2. Calculate the checksum using the Luhn algorithm.
    temp_npi = prefix + nine_digits
    
    total = 0
    for i, digit_char in enumerate(reversed(temp_npi)):
        digit = int(digit_char)
        # Double every second digit from the right
        if i % 2 == 1:
            doubled_digit = digit * 2
            # If doubling results in a two-digit number, add the digits
            if doubled_digit > 9:
                total += (doubled_digit // 10 + doubled_digit % 10)
            else:
                total += doubled_digit
        else:
            total += digit

    # 3. Find the check digit.
    # The check digit is the amount needed to round the total up to the nearest 10.
    check_digit = (10 - (total % 10)) % 10

    # 4. Append the check digit to form the final 10-digit NPI.
    return nine_digits + str(check_digit)

def random_BreastDensity():

    random_ID = None
    BDs = {
        'Result::BreastDensity::Dense': '32349', 
        'Result::BreastDensity::NonDense': '32350'
    }
    
    BD = random.choice(list(BDs.keys()))
    random_ID = BDs[BD]
    
    return random_ID

def random_TCLifetimeRisk():

    random_ID = None
    TCLifetimeRisks = {
        'Result::TCLifetimeRisk::Average':      '32351',
        'Result::TCLifetimeRisk::High':         '32352',
        'Result::TCLifetimeRisk::Intermediate': '32353'
    }
    
    TCLifetimeRisk = random.choice(list(TCLifetimeRisks.keys()))
    random_ID = TCLifetimeRisks[TCLifetimeRisk]
    
    return random_ID
                
def random_BIRADS():

    random_ID = None
    BIRADS = {
        'Result::BIRADS::0': '32343', 
        'Result::BIRADS::1': '32344',
        'Result::BIRADS::2': '32345',
        'Result::BIRADS::3': '32346',
        'Result::BIRADS::4': '32347',
        'Result::BIRADS::5': '32348'
    }
    BIRAD = random.choice(list(BIRADS.keys()))
    random_ID = BIRADS[BIRAD]
    return random_ID

def random_BAC():
    random_ID = None
    BACs = {
        'Result::BAC::Absent': '32341', 
        'Result::BAC::Present': '32342'
    }
    BAC = random.choice(list(BACs.keys()))
    random_ID = BACs[BAC]
    return random_ID

