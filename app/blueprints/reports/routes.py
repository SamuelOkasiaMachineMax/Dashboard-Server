from flask import Blueprint, jsonify, request, send_from_directory, current_app
from flask import send_file

reports_blueprint = Blueprint('reports', __name__)

from app.blueprints.reports.scripts.US_SUGAR.report import US_Sugar_main

report_dict={ 'US Sugar' : ['Completeness Report', "ExampleReport"],
              'Zeppelin' : ['ExampleReport']

              }

@reports_blueprint.route('/reports', methods=['GET'])
def reports():
    print(report_dict['US Sugar'])
    report_structure = [(customer,name) for customer in report_dict.keys() for name in report_dict[customer]]
    return jsonify(report_structure)



@reports_blueprint.route('/reports/<customer_name>/<name>/<action>', methods=['GET'])
def get(customer_name, name, action):
    if customer_name == 'US Sugar':
        return US_Sugar_main(name,action)
    return 'Report not found', 404
