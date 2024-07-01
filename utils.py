import os
from dotenv import load_dotenv
import re

load_dotenv()

def is_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False

def is_valid_phone_number(phone):
    regex = r'\+?1?\d{9,15}$'
    if re.fullmatch(regex, phone):
        return True
    else:
        return False

def format_application_date(date):
    return '-'.join(reversed(date.split('/')))

def get_config_var(var_name):
    return os.getenv(var_name)

def validate_input(text, min_length=1):
    return text is not None and len(text) >= min_length

def clean_string_input(input_string):
    return input_string.strip()

def get_api_key():
    return get_config_var("API_KEY")