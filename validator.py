import re
from datetime import date
from rest_framework import serializers

#Define function to validate first name
def validate_first_name(value):
    if not re.match("^[a-zA-Z]+$", value):
        raise serializers.ValidationError("First name should only contain alphabetic characters.")
    if len(value) < 3:
        raise serializers.ValidationError("First name should be at least 3 characters long.")
    if len(value) > 50:
        raise serializers.ValidationError("First name should not exceed 50 characters.")
    return value

#Define function to validate last name
def validate_last_name(value):
    if not re.match("^[a-zA-Z]+$", value):
        raise serializers.ValidationError("Last name should only contain alphabetic characters.")
    if len(value) < 1:
        raise serializers.ValidationError("Last name should be at least 1 character long.")
    if len(value) > 50:
        raise serializers.ValidationError("Last name should not exceed 50 characters.")
    return value

#Define function to validate email
def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise serializers.ValidationError("Enter a valid email address.")
    return value

#Define function to validate email
def validate_username(value):
    if not re.match("^[a-zA-Z0-9]+$", value):
        raise serializers.ValidationError("Username should only contain alphanumeric characters.")
    if len(value) < 3:
        raise serializers.ValidationError("Username should be at least 3 characters long.")
    if len(value) > 20:
        raise serializers.ValidationError("Username should not exceed 20 characters.")
    return value

#Define function to validate phone number
def validate_phone_number(value):
    if not re.match("^[0-9]+$", value):
        raise serializers.ValidationError("Phone number should only contain numeric digits.")
    if len(value) != 10:
        raise serializers.ValidationError("Phone number should be 10 digits long.")
    return value

#Define function to validate address
def validate_address(value):
    if len(value) > 255:
        raise serializers.ValidationError("Address should not exceed 255 characters.")
    return value

#Define function to validate pincode
def validate_pin_code(value):
    if not re.match(r'^\d+$', value):
        raise serializers.ValidationError("PIN code should only contain numeric digits.")
    if len(value) != 6:
        raise serializers.ValidationError("PIN code should be exactly 6 digits long.")
    return value

#Define function to validate date of birth
def validate_dob(value):
    dob_string = str(value)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob_string):
        raise serializers.ValidationError("Date of Birth should be in the format YYYY-MM-DD.")
    dob_date = date.fromisoformat(dob_string)

    if dob_date > date.today():
        raise serializers.ValidationError("Date of Birth cannot be in the future.")
    return value

#Define function to validate customer
def validate_user_type(value):
    valid_user_types = ["customer", "manager", "staff"]
    value = value.lower() 
    if value not in valid_user_types:
        raise serializers.ValidationError("User type must be 'customer', 'manager', or 'staff'")
    return value

#Define function to validate password
def validate_password(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password should be at least 8 characters long.")

    if not re.search(r'[A-Za-z]', value):
        raise serializers.ValidationError("Password should contain at least one letter (uppercase or lowercase).")

    if not re.search(r'\d', value):
        raise serializers.ValidationError("Password should contain at least one digit.")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError("Password should contain at least one special character.")

    return value