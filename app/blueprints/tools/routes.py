from flask import Flask, jsonify, request, send_from_directory, Blueprint, current_app
from app.blueprints.tools.scripts.GeoFenceFormatter import GeoFenceFormatter
from app.blueprints.tools.scripts.CustomerFilter import CustomerFilter, CustomerToJson
import os
import json

tools_blueprint = Blueprint('tools', __name__)


@tools_blueprint.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@tools_blueprint.route('/api/GeoFenceFormatter', methods=['POST'])
def GeoFenceFormatterr():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        try:
            GeoFenceFormatter.main(file_path)
            return jsonify({'filename': uploaded_file.filename})

        except:
            return jsonify({'filename': 'Error'})


@tools_blueprint.route('/OrgToSubOrg', methods=['GET'])
def OrgToSubOrg():
    bigquery_client = current_app.bigquery_client_UK
    query = f"""SELECT PO2.name as org, PO.name as suborg, FROM 

    `machinemax-prod-635d.google_cloud_postgresql_public.dealer_relationships` DR
    JOIN `machinemax-prod-635d.google_cloud_postgresql_public.organisations` PO on DR.organisation_id = PO.id
    LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.organisations` PO2 on PO2.id = DR.dealer_organisation_id
    """

    try:
        query_job = bigquery_client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        data = [{"org": row.org,
                 "suborg": row.suborg,
                 } for row in results]

        result = {}
        for item in data:
            org = item['org']
            suborg = item['suborg']
            if org not in result:
                result[org] = []
            result[org].append(suborg)

            # return jsonify(CustomerToJson.ReturnCustomerList())
        return jsonify(result)

    except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
@tools_blueprint.route('/api/CustomerFilter', methods=['POST'])
def CustomerFilterr():
    try:
        # Handle the file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

        # Handle the JSON data
        data = json.loads(request.form['data'])
        value = data.get('value')

        # Process the file with the provided values
        CustomerFilter.main(file_path, value)
        print("process complete")

        return jsonify({'filename': uploaded_file.filename})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
