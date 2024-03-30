# We need a database to work with!
# Connect to MySQL by importing through your mysqlconnection file
# If your mysqlconnection is in config it will need a file route
from flask_app.config.mysqlconnection import connectToMySQL
#use pretty print to make terminal prints easier to read
from pprint import pprint
from flask import flash

#Create a class and remember that this class will need to be imported into server.py
class Ninja:
    #create a variable that connects to the correct database
    DB = "dojos_and_ninjas schema"

    #initialize!!
    def __init__(self, data):
        #EVERY COLUMN FROM OUR DATABASE MUST BE IMPORTED HERE
        #self is FOR this .py file, data is FROM the database
        #The order DOES matter
        self.id = data ['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']

#NOW that we have properly imported the data from our database, we can start running class methods

#create a class method using this:
    @classmethod
    #we need to pass this class in as an argument, as well as the data because we are sending data to the database
    def create_ninja(cls, data):
        #assign our query to a string called query
        #This particular query is to insert data into our database
        #Include the command to insert into the table 
        #Include the locations of the insertions
        #Include the values (data) you are inserting
        #Include NOW() for NOW timestamp
        query = """INSERT INTO ninjas 
        (first_name, last_name, age, 
        created_at, updated_at, dojo_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, NOW(), NOW(), %(dojo_id)s)"""

        #connectToMySQL is a class method that is defined in the mySQLConnection class of our mysqlconnection sheet that actually connects us to our database using any argument we provide as the link to the database
        #So, return our connected database using our class and our database first_name
        #then using the . we access the query_db class method and provide it with our query variable and data as the arguments
        results = connectToMySQL(cls.DB).query_db(query,data)
        pprint(results)
        return(results)
        #Now in order for this to ~work~ this class needs to be imported into our server.py

#This part of our logic should not be read UNTIL you have imported the previous information into the server.py, created a html sheet to take in the data, and created an html sheet to display the data
#If you have not done that yet, please do that and come back after
    
    #We now create a class method that will GET ALL of our ninjas
    @classmethod 
    #There is no need to pass in data on this method because we are only selecting
    def get_all(cls):
        query = "SELECT * FROM ninjas"
        #This is the same logic from the previous class method
        results = connectToMySQL(cls.DB).query_db(query)
        #Create an empty string to pass all new data into
        ninjas = []
        #Create a for loop that iterates through each item in the results
        #SO, if we just submitted data from our root route, upon redirecting to the new page, we will call this function which will iterate through every item in the database
        #in this case the ninja is arbitrary, it could be I or X if you wanted
        #append to your empty ninjas string, and ninja that is found in the class
        for ninja in results:
            ninjas.append(cls(ninja))
        print(ninjas)
        return ninjas 
        #Now that this class method is complete, we can call it in our server.py file under the appropriate route
    #Now we will validate user inputs to prevent any code breaking

    @classmethod
    def get_ninjas_by_dojo(cls, dojo_id):
        query = "SELECT * FROM ninjas WHERE dojo_id = %(dojo_id)s"
        data = {
            'dojo_id': dojo_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        ninjas = []
        for result in results:
            ninjas.append(cls(result))
        return ninjas

    @staticmethod
    def validate_ninja(ninja):
        is_valid = True
        if len(ninja['first_name']) < 1 :
            flash('First name must be at least 1 character')
            is_valid=False
        if len(ninja['last_name']) < 1:
            flash('Last name must be at least 1 character')
            is_valid=False
        try:
            age = int(ninja['age'])
        except ValueError:
            flash('Age must be a number')
            is_valid = False
        else:
            if age < 1:
                flash('Age must be at least 1 character')
                is_valid = False
    
        return is_valid


