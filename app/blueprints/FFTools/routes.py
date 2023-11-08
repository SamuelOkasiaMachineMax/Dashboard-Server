from flask import Blueprint, jsonify, request
import json
import os
from datetime import datetime
FFTools_blueprint = Blueprint('FFTools', __name__)



@FFTools_blueprint.route('/FFTools/<variablesList>/<start_date>/<end_date>', methods=['GET'])
def FFTools(variablesList,start_date,end_date):
    variablesList = str(variablesList).split(',')
    print(variablesList,start_date,end_date)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FFToolsFile = os.path.join(BASE_DIR, 'FFTools.json')

    with open(FFToolsFile, 'r') as json_file:
        data = json.load(json_file)
        # variables = ["GPS coordinates", "GSM signal", "External voltage (mV)"]
        variables = variablesList
        def parse_date(date_str):
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Date format for '{date_str}' is not supported.")

        # Convert start and end dates to datetime objects using the parse_date function
        start_dt = parse_date(start_date)
        end_dt = parse_date(end_date)

        # Dictionary to store the filtered results
        filtered_results = {}

        for device_id, timestamps in data.items():
            for timestamp_str, details in timestamps.items():
                # Use the parse_date function which tries multiple formats
                timestamp = parse_date(timestamp_str)

                # Check if the timestamp is within the given range
                if start_dt <= timestamp <= end_dt:
                    # If the timestamp is within the range, filter out the variables
                    filtered_details = {key: value for key, value in details.items() if key in variables}

                    # Add the filtered details to the results dictionary
                    if device_id not in filtered_results:
                        filtered_results[device_id] = {}
                    filtered_results[device_id][timestamp_str] = filtered_details

        print(filtered_results)


    return jsonify(filtered_results)