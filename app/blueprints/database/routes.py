from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os
from app.models import Sensor,Customer, Overview
from sqlalchemy import and_

from app.blueprints.telamatics.script import noTelamaticsMain
database_blueprint = Blueprint('database', __name__)

@database_blueprint.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    result = [customer.as_dict() for customer in customers]

    for dictionary in result:
        count_yes = Overview.query.filter(
            and_(Overview.customer_id == dictionary['id'], Overview.telematics_found == 'No')).count()
        dictionary.update({'telematics':count_yes})


    #number = Overview.query.filter_by(Overview.customer_id == 2, Overview.telematics_found == "No").count()

    return jsonify(result)


@database_blueprint.route('/sensors/<customer_name>', methods=['GET'])
def get_sensors(customer_name):
    # Retrieve the customer object by name
    customer = Customer.query.filter_by(name=customer_name).first()

    # Check if the customer exists
    if not customer:
        return jsonify({'error': 'Customer not found'})

    # Fetch all sensors for the specific customer using the relationship
    sensors = Sensor.query.filter_by(customer_id=customer.id).all()

    # Convert the list of Sensor objects to a list of dictionaries for JSON serialization
    result = [sensor.as_dict() for sensor in sensors]

    return jsonify(result)


