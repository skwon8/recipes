from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re


class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
# Create NEW USER classmethod
    @classmethod
    def create_new_user(cls, data):

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result = connectToMySQL("recipes").query_db(query, data)

        return result
    
# Get user by FIRST NAME method
    @classmethod
    def get_user_by_first_name(cls, data):

        query = "SELECT * FROM users WHERE first_name = %(first_name)s;"

        results = connectToMySQL("recipes").query_db(query, data)

        if len(results) == 0:
            return False
        else:
            return User(results[0])

# Get user by LAST NAME method
    @classmethod
    def get_user_by_last_name(cls, data):

        query = "SELECT * FROM users WHERE last_name = %(last_name)s;"

        results = connectToMySQL("recipes").query_db(query, data)

        if len(results) == 0:
            return False
        else:
            return User(results[0])

# Get user by EMAIL method
    @classmethod
    def get_user_by_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL("recipes").query_db(query, data)

        if len(results) == 0:
            return False
        else:
            return User(results[0])

# VALIDATE method
    @staticmethod
    def validate_new_user(data):
        is_valid = True

        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        # username is not in use
        if User.get_user_by_first_name(data):
            is_valid = False
            flash("First Name should be Unique!")

        if User.get_user_by_last_name(data):
            is_valid = False
            flash("Last Name should be Unique!")

        # username 3-50 characters long
        if len(data['first_name']) < 2 or len(data['first_name']) > 50:
            is_valid = False
            flash("First Name should be 2 to 50 characters long")
            
        if len(data['last_name']) < 2 or len(data['last_name']) > 50:
            is_valid = False
            flash("Last Name should be 2 to 50 characters long")

        # email is not in use
        if User.get_user_by_email(data):
            is_valid = False
            flash("Email shoud be Unique!")

        # email is valid
        if not email_regex.match(data['email']):
            is_valid = False
            flash("Email address is not formatted correctly.")

        # password is of minimum length
        if len(data['password']) < 8:
            is_valid = False
            flash("Password shoud be at least 8 characters long.")
            
        # password and confirm password match
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Password and Confirm Password do not match.")
        return is_valid
