# jobpostings.py
from flask import request
from flask_restful import Resource
import json
from pymongo import MongoClient

with open('local_config.json', 'r') as config_file:
    config_data = json.load(config_file)

MONGO_CONFIG = config_data['MONGO_CONFIG']

class JobPosting(Resource):
    def __init__(self, collection):
        super().__init__()
        self.collection = collection


    def post(self):
        # Extract data from the request
        data = request.get_json()
        company_name = data.get('company_name')
        profile = data.get('profile')
        branches = data.get('branches')
        skills_required = data.get('skills_required')
        ctc = data.get('ctc')
        percentage = data.get('percentage')
        bond_years = data.get('bond_years')
        work_location = data.get('work_location')
        year_of_passing = data.get('year_of_passing')
        positions_open = data.get('positions_open')

        # Check if all required fields are present
        if not (company_name and profile and branches and skills_required and ctc and percentage and bond_years and
                work_location and year_of_passing and positions_open):
            return {"error": "Missing required fields"}, 400

        # Insert job posting data into MongoDB
        job_data = {
            "company_name": company_name,
            "profile": profile,
            "branches": branches,
            "skills_required": skills_required,
            "ctc": ctc,
            "percentage": percentage,
            "bond_years": bond_years,
            "work_location": work_location,
            "year_of_passing": year_of_passing,
            "positions_open": positions_open
        }
        result = self.collection.insert_one(job_data)
        job_data['_id'] = str(result.inserted_id)

        # Return a success message along with job data
        return {"message": "Job posting successful", "job_posting": job_data}, 201
