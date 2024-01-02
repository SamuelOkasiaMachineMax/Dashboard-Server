class BatteryManager:
    def __init__(self,results):
        self.alerts = {}

        for row in results:
            sensor_data = {
                'battery_level': row.battery_level,
                "battery_voltage": row.battery_voltage,
                "deveui": row.deveui,
                "organisation_id": row.organisation_id,
                "customer": row.name,
                "tag": row.tag,
                "model": row.model}
            self.add_sensor_data(row.name, sensor_data)

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

    def get_overview(self):
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

class VoltageManager:
    def __init__(self, results):
        self.alerts = {}

        for row in results:
                    sensor_data = {
                        'external_voltage': row.external_voltage,
                        "gsm_signal": row.gsm_signal,
                        "machine_id": row.machine_id,
                        "organisation_id": row.organisation_id,
                        "name": row.name,
                    }
                    self.add_sensor_data(row.name, sensor_data)

    def add_sensor_data(self, customer_name, sensor_data):
        if customer_name not in self.alerts:
            self.alerts[customer_name] = {'no_voltage': [], 'low_voltage': [], 'normal_voltage': []}

        battery_level = float(sensor_data['external_voltage'])
        if battery_level < 1.0:
            self.alerts[customer_name]['no_voltage'].append(sensor_data)
        elif battery_level < 1000.0:
            self.alerts[customer_name]['low_voltage'].append(sensor_data)
        else:
            self.alerts[customer_name]['normal_voltage'].append(sensor_data)

    def generate_alert_messages(self):
        messages = []
        for name, data in self.alerts.items():

            if data['no_voltage']:
                count = len(data['no_voltage'])
                messages.append({'customer':name, 'message':f'{count} {"sensor has" if count == 1 else "sensors have"} no voltage'})
            elif data['low_voltage']:
                count = len(data['low_voltage'])
                messages.append({'customer':name, 'message':f'{count} {"sensor has" if count == 1 else "sensors have"} low voltage.'})
        return messages

    def get_overview(self):

        return [
            {
                'customer': name,
                'no_voltage': len(data['no_voltage']),
                'low_voltage': len(data['low_voltage']),
                'normal_voltage': len(data['normal_voltage'])
            } for name, data in self.alerts.items()
        ]