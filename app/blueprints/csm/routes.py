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


    # print(DataStatusReport.viewDataStatusReport())
    # return jsonify(DataStatusReport.viewDataStatusReport())

