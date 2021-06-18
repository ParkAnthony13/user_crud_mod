# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users

    @classmethod #creating a new user
    def save(cls, data):
        query = "INSERT INTO users(first_name,last_name,email,created_at,updated_at) VALUES ( %(fname)s , %(lname)s , %(email)s , NOW() , NOW() );"
        return connectToMySQL('users_schema').query_db(query, data)

    @classmethod #select single user
    def select_single(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('users_schema').query_db(query, data)
        print(result)
        return User(result[0])

    @classmethod #select most last on the list
    def last(cls,data):
        query = "SELECT id FROM users ORDER BY id DESC LIMIT 1;"
        return connectToMySQL('users_schema').query_db(query)

    @classmethod #delete user
    def delete(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        connectToMySQL('users_schema').query_db(query, data)
        return True

    @classmethod #update user
    def update(cls, data):
        query = "UPDATE users SET first_name=%(fname)s,last_name=%(lname)s,email=%(email)s,created_at=NOW(),updated_at=NOW() WHERE id=%(id)s;"
        connectToMySQL('users_schema').query_db(query, data)