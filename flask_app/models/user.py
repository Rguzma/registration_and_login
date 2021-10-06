from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   

from flask import flash

class User:
    db = "register_and_login"
    def __init__(self, data):
        self.id=data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.created_at = data['created_at']
        self.confirm=data['confim']
    
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,SYSDATE())"
        return connectToMySQL("register_and_login").query_db(query,data)   

    @classmethod                                    
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("register_and_login").query_db(query)
        users = []
        for u in results:
            users.append (cls (u))
        return users
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("register_and_login").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("register_and_login").query_db(query,data)
        return cls(results[0])
        


    @classmethod
    def get_one (cls, data):
        query="SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL('register_and_login').query_db(query,data)
        return cls(result[0])


    #PROCESO DE VALIDACION

    @staticmethod
    def validate_register(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('register_and_login').query_db(query,data)
        
        
        
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
        return is_valid