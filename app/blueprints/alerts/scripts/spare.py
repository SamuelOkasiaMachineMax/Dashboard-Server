from flask import Blueprint, jsonify, request, send_from_directory, current_app

alerts_blueprint = Blueprint('alerts', __name__)
from app.models import Overview, Customer




class AlertManager:
    def __init__(self):
        self.alerts = {}

    def add_sensor_data(self, customer_name, sensor_data):
        if customer_name not in self.alerts:
            self.alerts[customer_name] = {'no_battery': [], 'low_battery': [], 'medium_battery': [], 'high_battery': []}

        battery_level = float(sensor_data['battery_level'])
        if battery_level < 1.0:
            self.alerts[customer_name]['no_battery'].append(sensor_data)
        elif battery_level < 10.0:
            self.alerts[customer_name]['low_battery'].append(sensor_data)
        elif battery_level < 66.0:
            self.alerts[customer_name]['medium_battery'].append(sensor_data)
        else:
            self.alerts[customer_name]['high_battery'].append(sensor_data)

    def get_alerts(self):
        return [
            {
                'customer': customer,
                'low_battery_count': len(data['low_battery']),
                'medium_battery_count': len(data['medium_battery']),
                'high_battery_count': len(data['high_battery'])
            } for customer, data in self.alerts.items()
        ]

    def generate_alert_messages(self):
        messages = []
        for customer, data in self.alerts.items():


            if data['no_battery']:
                count = len(data['no_battery'])
                messages.append({'customer':customer, 'message':f'{count} {"sensor needs" if count == 1 else "sensors need"} battery replacement.'})
            elif data['low_battery']:
                count = len(data['low_battery'])
                messages.append({'customer':customer, 'message':f'{count} {"sensor has" if count == 1 else "sensors have"} low battery.'})
        return messages


def get_sensor_data():
    bigquery_client = current_app.bigquery_client_UK

    query = f"""
            SELECT ls.battery_level, ls.battery_voltage, dv.deveui, dv.organisation_id, dv.tag, org.name, fd.model
            FROM `machinemax-prod-635d.google_cloud_postgresql_public.latest_status` AS ls
            LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.devices` as dv
            ON ls.deveui = dv.deveui
            LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.organisations` AS org
            on dv.organisation_id = org.id
            LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.fotaweb_device` AS fd
            ON ls.deveui = CAST(fd.imei AS STRING)
              """
    query_job = bigquery_client.query(query)
    results = query_job.result()
    return results

@alerts_blueprint.route('/alerts', methods=['GET'])
def alerts():
    try:
        results = get_sensor_data()
        alert_manager = AlertManager()

        for row in results:
            sensor_data = {
                'battery_level': row.battery_level,
                "battery_voltage": row.battery_voltage,
                "deveui": row.deveui,
                "organisation_id": row.organisation_id,
                "customer": row.name,
                "tag": row.tag,
                "model": row.model}
            alert_manager.add_sensor_data(row.name, sensor_data)

        alert_messages = alert_manager.generate_alert_messages()

        return jsonify({'alerts': alert_manager.get_alerts(), 'messages': alert_messages})

    except Exception as e:
        # Implement logging here if necessary
        return jsonify({'error': str(e)}), 500

# Flask app run configuration
