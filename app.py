# from flask import Flask
# from flask_restful import Api
# from web.signup import Signup  # Import the Signup class from the signup module
# from pymongo import MongoClient

# class MyFlask(Flask):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.global_variables = {}
#         self.client = MongoClient('mongodb://localhost:27017')
#         self.db = self.client['signup']
#         self.collection = self.db['sign']

#     def add_api(self):
#         api = Api(self, catch_all_404s=True)
#         api.add_resource(
#             Signup,
#             "/api/v1/signup",
#             resource_class_kwargs={'collection': self.collection}  # Pass the collection to the Signup resource
#         )

# if __name__ == "__main__":
#     app = MyFlask(__name__)
#     app.add_api()
#     app.run(debug=True)
# app.py
from flask import Flask
from flask_restful import Api
from web.signup import Signup
from pymongo import MongoClient
import json
from web.login import Login  # Import the Login class from the login module


class MyFlask(Flask):
    def __init__(self, config_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_variables = {}

        # Read MongoDB credentials from local_config.json based on the provided config_key
        with open('local_config.json') as config_file:
            config = json.load(config_file)
            mongodb_uri = config[config_key]['mongodb_uri']
            database_name = config[config_key]['database_name']
            collection_name = config[config_key]['collection_name']

        # Connect to MongoDB
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add_api(self):
        api = Api(self, catch_all_404s=True)
        api.add_resource(
            Signup,
            "/api/v1/signup",
            resource_class_kwargs={'collection': self.collection}
        )
        api.add_resource(
            Login,
            "/api/v1/login",
            resource_class_kwargs={'collection': self.collection}  # Pass the collection to the Login resource
        )

# Create the Flask app instance
app = MyFlask("SIGN_UP_STUDENT", __name__)
app.add_api()

# Only run the app if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
