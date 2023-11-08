from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os
from app.blueprints.test import export_to_database
from app.blueprints.telamatics.script import noTelamaticsMain
from app.models import Customer
from app import db

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test', methods=['POST'])
def some_view_function():
    try:
        export_to_database.populate_sensors_from_excel()
        return 'Worked'

    except Exception as e:
        return 'Error: ' + str(e)



@test_blueprint.route('/test_overview', methods=['POST'])
def add_overview():
    try:
        export_to_database.populate_overview_from_excel()
        return 'Worked'

    except Exception as e:
        return 'Error: ' + str(e)



@test_blueprint.route('/add_customer', methods=['POST'])
def add_data():
    customer = Customer.query.filter_by(name='Imery').first()
    if not customer:
        customer = Customer(name="Imery",
                            orgID="0b4ad8cc-e7dc-4d8f-a4db-213c6618036b"
                            )

        db.session.add(customer)
        db.session.commit()
        return 'added'
    return 'already there'