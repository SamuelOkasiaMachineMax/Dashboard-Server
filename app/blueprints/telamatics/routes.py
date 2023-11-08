from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os

from app.blueprints.telamatics.script import noTelamaticsMain
telamatics_blueprint = Blueprint('telamatics', __name__)
from app.models import Overview, Customer


@telamatics_blueprint.route('/search-telematics-upload', methods=['POST'])
def some_view_function():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    organisation = request.form.get('orgID', "")

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        outcome = noTelamaticsMain.main(file_path, organisation)
        print(outcome)
        return jsonify(
            {'message': 'File uploaded successfully',
             'machines': outcome
             }), 200


@telamatics_blueprint.route('/search-telematics/<customer>/<orgID>', methods=['POST'])
def search_telematics(customer,orgID):
    customer = Customer.query.filter_by(name=customer).first()

    records = (Overview.query
               .filter_by(customer_id=customer.id)
               .filter(Overview.telematics_found == 'No')
               .with_entities(Overview.asset_id, Overview.vin)
               .all())

    machine_dict = {}
    for record in records:
        asset_id, vin = record
        machine_dict[vin] = {'AssetID':asset_id}

    #x = [(record[0],record[1]) for record in records]
    outcome = noTelamaticsMain.main_but_no_import(machine_dict,orgID)
    return outcome
