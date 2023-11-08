from app.blueprints.data_endpoints.add_data_dr.postman import Postman
from app import db

def main(Customer,Machine,machine_dictionary):
    # machine_dictionary = Postman("flannery@machinemax.com", "*!CnCwcbz7PEgUcGR_yz","Zeppelin",'32afd2bd-7bad-4618-a0df-1dcc1b8fdaa2').GET()
    # machine_dictionary = dict(machine_dictionary)

    # Check if the customer exists or create a new one
    customer = Customer.query.filter_by(name=machine_dictionary['name']).first()
    if not customer:
        customer = Customer(name=machine_dictionary['name'],
                            orgID=machine_dictionary['orgID']
                            )

        db.session.add(customer)

    for key in machine_dictionary['fleet'].keys():
        machine_payload = {
            'asset_id': machine_dictionary['fleet'][key]['Asset ID'],
            'model': machine_dictionary['fleet'][key]['Model'],
            'oem': machine_dictionary['fleet'][key]['OEM'],
            'latest_call_type': machine_dictionary['fleet'][key]['Latest Call Type'],
            'latest_call': machine_dictionary['fleet'][key]['Latest Call'],
            'api_calls': machine_dictionary['fleet'][key]['API Calls'],
            'owner': customer
        }

        # Check if this machine already exists for the customer
        machine = Machine.query.filter_by(asset_id=machine_payload['asset_id'], owner=customer).first()

        if machine:
            # Update the machine attributes
            for attr, value in machine_payload.items():
                setattr(machine, attr, value)
        else:
            # Create a new machine entry
            machine = Machine(**machine_payload)
            db.session.add(machine)

    # Commit changes after processing all machines
    db.session.commit()