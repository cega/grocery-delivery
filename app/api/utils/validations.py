# Contain validations for data received by endpoints

import re
from flask_restplus import reqparse
import jwt


class Validations():

    def __init__(self):
        pass

    def add_arguments(self, parser, fields):
        for field in fields:
            parser.add_argument(field, help='Field {} cannot be blank.'
                                .format(field), required=True)

    def validate_password(self, password):
        if re.match(r"(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.\
                    *[A-Z])(?=.*[0-9])))(?=.{8,})", password):
            return True
        return False

    def validate_email(self, email):
        if re.match(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email):
            return True
        return False

    def validate_name(self, name):
        if re.match(r"(^[a-zA-Z]+$)", name):
            return True
        return False

    def check_if_empty(self, fields):
        is_empty = False
        is_empty_message = {}
        for key, value in fields.items():
            if not value and key is not "location":
                is_empty = True
                is_empty_message[key] = "{} should not be empty".format(key)

            #  check whether the role is customer so as to validate location
            else:
                if fields['role'] is "customer":
                    is_empty = True
                    is_empty_message[key] = "{} should not be empty".format(key)
        if is_empty:
            return is_empty_message
        return is_empty

    def check_if_role(self, role):
        if role == "admin":
            return True
        elif role == "customer":
            return True
        else:
            return False

    def token_present(self, token):
        if token:
            return True

    def check_if_admin(self, role):
        if role == "admin":
            return True

    def check_if_customer(self, role):
        if role == "customer":
            return True

    def check_token_error(self, error):
        if error == "ExpiredSignatureError" or error == "InvalidTokenError":
            return True

    def validate_registration_data(self, first_name, last_name, email, phone,
                                   password, role, location=None):

        error_response = {}
        error = False

        user = dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            location=location,
            password=password,
            role=role
        )

        is_empty = self.check_if_empty(user)
        if is_empty:
            return dict(error=is_empty)
        if not self.validate_name(first_name):
            error = True
            error_response['first_name'] = "First name should contain letters only"
        if not self.validate_name(last_name):
            error = True
            error_response['last_name'] = "Last name should contain letters only"
        if not self.validate_email(email):
            error = True
            error_response['email'] = "Invalid email"
        if not re.match(r"^([\s\d]+)$", phone):
            error = True
            error_response['phone'] = "Invalid phone number"
        if not self.validate_password(password):
            error = True
            error_response['password'] = "The password should contain a small and a capital letter, a number and a special character"
        if not self.check_if_role(role):
            error = True
            error_response['role'] = "Role should be admin or customer"
        if role is 'customer':
            if not self.validate_name(location):
                error = True
                error_response['last_name'] = "Location should contain letters only"

        if error:
            return dict(error=error_response)
