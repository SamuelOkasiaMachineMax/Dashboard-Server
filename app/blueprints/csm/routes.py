from flask import Flask, jsonify, request, send_from_directory, Blueprint, current_app
from app.blueprints.csm.scripts import DataStatusReport
import os

csm_blueprint = Blueprint('csm', __name__)

@csm_blueprint.route('/csm/<value>', methods=['POST'])
def download_file(value):
    print(value)
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        try:
            return jsonify(DataStatusReport.viewDataStatusReport(file_path,value))

        except:
            return jsonify({'filename': 'Error'})


    # print(DataStatusReport.viewDataStatusReport())
    # return jsonify(DataStatusReport.viewDataStatusReport())

