import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

def is_valid_email(email):
    """Validate email address format."""
    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return bool(re.fullmatch(regex, email))
    except Exception as e:
        print(f"Error validating email: {e}")
        return False

def is_valid_phone_number(phone):
    """Validate phone number format."""
    try:
        regex = r'\+?1?\d{9,15}$'
        return bool(re.fullmatch(regex, phone))
    except Exception as e:
        print(f"Error validating phone number: {e}")
        return False

def format_application_date(date):
    """Format application date from DD/MM/YYYY to YYYY-MM-DD."""
    try:
        return '-'.join(reversed(date.split('/')))
    except Exception as e:
        print(f"Error formatting application date: {e}")
        return ""

def get_config_var(var_name):
    """Retrieve a configuration variable."""
    try:
        return os.getenv(var_name)
    except Exception as e:
        print(f"Error retrieving configuration variable {var_name}: {e}")
        return None

def validate_input(text, min_length=1):
    """Validate if the input text meets the minimum length requirement."""
    try:
        return bool(text) and len(text) >= min_length
    except Exception as e:
        print(f"Error validating input: {e}")
        return False

def clean_string_input(input_string):
    """Trim whitespace from an input stemilring."""
    try:
        return input_string.strip()
    except Exception as e:
        print(f"Error cleaning string input: {e}")
        return ""

def get_api_key():
    """Retrieve the API key from environment variables."""
    try:
        return get_config_var("API_KEY")
    except Exception as e:
        print(f"Error getting API key: {e}")
        return None