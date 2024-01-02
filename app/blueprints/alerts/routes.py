from flask import Blueprint, jsonify
from app.blueprints.alerts.scripts.sensor_manager import SensorManager
from app.blueprints.alerts.scripts.alert_manager import BatteryManager, VoltageManager

alerts_blueprint = Blueprint('alerts', __name__)

@alerts_blueprint.route('/alerts', methods=['GET'])
def alerts():
    sensor_manager = SensorManager()
    battery_data = sensor_manager.fetch_battery_data()
    voltage_data= sensor_manager.fetch_voltage_data()



    batteryManager = BatteryManager(battery_data)
    battery_alerts = batteryManager.generate_alert_messages()
    battery_results = batteryManager.get_overview()

    voltageManager = VoltageManager(voltage_data)
    voltage_alerts = voltageManager.generate_alert_messages()
    voltage_results = voltageManager.get_overview()

    all_alerts = battery_alerts + voltage_alerts

    return jsonify({'alerts': all_alerts, 'battery_overview':battery_results, 'voltage_overview':voltage_results})




