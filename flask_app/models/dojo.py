# We need a database to work with!
# Connect to MySQL by importing through your mysqlconnection file
# If your mysqlconnection is in config it will need a file route
from flask_app.config.mysqlconnection import connectToMySQL
#use pretty print to make terminal prints easier to read
from pprint import pprint
from flask import flash

#Create a class and remember that this class will need to be imported into server.py
class Dojo:
    #create a variable that connects to the correct database
    DB = "dojos_and_ninjas schema"

    #initialize!!
    def __init__(self, data):
        #EVERY COLUMN FROM OUR DATABASE MUST BE IMPORTED HERE
        #self is FOR this .py file, data is FROM the database
        #The order DOES matter
        self.id = data ['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_dojo(cls, data):
        query = """INSERT INTO dojos 
        (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW())"""

        results = connectToMySQL(cls.DB).query_db(query,data)
        print(results)
        return(results)

    @classmethod
    def get_dojo_by_id(cls, dojo_id):
        query = "SELECT * FROM dojos WHERE id = %(id)s"
        data = {
            'id': dojo_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])  # Return the first dojo found
        else:
            return None

    
    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM dojos"
        results = connectToMySQL(cls.DB).query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(cls(dojo))
        print(dojos)
        return dojos 



    @staticmethod
    def validate_dojo(dojo):
        is_valid = True
        if len(dojo['name']) < 1 :
            flash('Input must be at least 1 character')
            is_valid=False
        return is_valid