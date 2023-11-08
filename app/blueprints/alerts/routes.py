from flask import Blueprint, jsonify, request, send_from_directory, current_app

alerts_blueprint = Blueprint('alerts', __name__)
from app.models import Overview, Customer


@alerts_blueprint.route('/alerts', methods=['POST'])
def alerts():
    customers = Customer.query.all()
    result = [customer.as_dict() for customer in customers]
    