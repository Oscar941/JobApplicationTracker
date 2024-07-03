import os
from dotenv import load_dotenv
import re

load_dotenv()

def is_valid_email(email):
    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error validating email: {e}")
        return False

def is_valid_phone_number(phone):
    try:
        regex = r'\+?1?\d{9,15}$'
        if re.fullmatch(regex, phone):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error validating phone number: {e}")
        return False

def format_application_date(date):
    try:
        return '-'.join(reversed(date.split('/')))
    except Exception as e:
        print(f"Error formatting application date: {e}")
        return ""

def get_config_var(var_name):
    try:
        return os.getenv(var_name)
    except Exception as e:
        print(f"Error retrieving configuration variable {var_name}: {e}")
        return None

def validate_input(text, min_length=1):
    try:
        return text is not None and len(text) >= min_length
    except Exception as e:
        print(f"Error validating input: {e}")
        return False

def clean_string_input(input_string):
    try:
        return input_string.strip()
    except Exception as e:
        print(f"Error cleaning string input: {e}")
        return ""

def get_api_key():
    try:
        return get_config_var("API_KEY")
    except Exception as e:
        print(f"Error getting API key: {e}")
        return None