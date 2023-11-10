from flask import Flask, jsonify, request, send_from_directory, Blueprint, current_app
from app.blueprints.tools.scripts.GeoFenceFormatter import GeoFenceFormatter
from app.blueprints.tools.scripts.CustomerFilter import CustomerFilter, CustomerToJson
import os

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

        GeoFenceFormatter.main(file_path)

    return jsonify({'filename': uploaded_file.filename})


@tools_blueprint.route('/api/CustomerFilter/<value>', methods=['POST'])
def CustomerFilterr(value):
    if value == 'view':
        print(value)
        return jsonify(CustomerToJson.ReturnCustomerList())

    else:
        print('donnne')
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            CustomerFilter.main(file_path, value)
            print("process compelete")

        return jsonify({'filename': uploaded_file.filename})
