from flask import Flask, jsonify, request, send_from_directory, Blueprint, current_app
from app.blueprints.csm.scripts import DataStatusReport
import os

csm_blueprint = Blueprint('csm', __name__)

@csm_blueprint.route('/csm', methods=['POST'])
def download_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        try:
            return jsonify({'CSM':DataStatusReport.viewDataStatusReport(file_path,'CSM'),
                            'FULL':DataStatusReport.viewDataStatusReport(file_path,'FULL')
                            })

        except:
            return jsonify({'filename': 'Error'})

@csm_blueprint.route('/get-bigquery-data', methods=['GET'])
def get_bigquery_data():
    bigquery_client = current_app.bigquery_client_UK

    query = """
       SELECT ID
       FROM `machinemax-prod-635d.google_cloud_postgresql_public.roles`
       WHERE NAME = 'internal' 
       LIMIT 10
       """
    try:
        # Run the query and get the results
        query_job = bigquery_client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        # Process the results
        data = [{"ID": row.ID } for row in results]

        # Return as JSON
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500