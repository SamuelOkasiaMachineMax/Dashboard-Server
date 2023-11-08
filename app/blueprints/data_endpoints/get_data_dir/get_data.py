from app import db
from flask import jsonify

def main(Customer,Machine,customer_name):
    customer = Customer.query.filter_by(name=customer_name).first()

    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    machines = Machine.query.filter_by(customer_id=customer.id).all()

    data = {
        "customer_name": customer.name,
        "machines":[]
    }

    for machine in machines:
        machine_data = {
            "asset_id": machine.asset_id,
            "model": machine.model,
            "oem": machine.oem,
            "latest_call_type": machine.latest_call_type,
            "latest_call": machine.latest_call,
            "api_calls": machine.api_calls
        }
        data["machines"].append(machine_data)

    return data