# app.py
from flask import Flask
from flask_restful import Api
from web.signup import Signup
from web.jobpostings import JobPosting  # Import JobPosting from jobpostings module
import json
from pymongo import MongoClient  # Import MongoClient from pymongo

with open('local_config.json', 'r') as config_file:
    config_data = json.load(config_file)

MONGO_CONFIG = config_data['MONGO_CONFIG']

class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(MONGO_CONFIG['uri'])
        self.db = self.client[MONGO_CONFIG['db_name']]
        self.collection = self.db[MONGO_CONFIG['collection_name']]

    def add_api(self):
        api = Api(self, catch_all_404s=True)
        api.add_resource(
            Signup,
            "/api/v1/signup",
            resource_class_kwargs={'collection': self.collection}
        )
        api.add_resource(
            JobPosting,
            "/api/v1/job_postings",
            resource_class_kwargs={'collection': self.collection}  # Pass the collection to JobPosting
        )

if __name__ == "__main__":
    app = MyFlask(__name__)
    app.add_api()
    app.run(debug=True)
