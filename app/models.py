from datetime import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    orgID = db.Column(db.String(100), nullable=False)

    # One-to-many relationship: one customer has many machines
    machines = db.relationship('Machine', backref='owner', lazy=True)
    sensors = db.relationship('Sensor', backref='customer', lazy=True)
    overviews = db.relationship('Overview', backref='customer', lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "orgID": self.orgID
        }

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    imei = db.Column(db.String(100))
    source_name = db.Column(db.String(100))

    asset_id = db.Column(db.String(100))
    machine_name = db.Column(db.String(100))
    source_status = db.Column(db.String(100))
    battery_voltage = db.Column(db.String(100))
    battery_status = db.Column(db.String(100))
    signal_status = db.Column(db.String(100))

    latest_connection = db.Column(db.String(100))
    data_completion = db.Column(db.String(100))
    latest_hours = db.Column(db.String(100))
    latest_latitude = db.Column(db.String(100))
    latest_longitude = db.Column(db.String(100))
    latest_location_timestamp = db.Column(db.String(100))
    site = db.Column(db.String(100))

    device_model = db.Column(db.String(100))
    firmware_version = db.Column(db.String(100))
    configuration_version = db.Column(db.String(100))
    device_mode = db.Column(db.String(100))
    first_associated = db.Column(db.String(100))
    signal = db.Column(db.String(100))

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def as_dict(self):
        return {
            'imei': self.imei,
            'source_name': self.source_name,
            'asset_id': self.asset_id,
            'machine_name': self.machine_name,
            'source_status': self.source_status,
            'battery_voltage': self.battery_voltage,
            'battery_status': self.battery_status,
            'signal_status': self.signal_status,
            'latest_connection': self.latest_connection,
            'data_completion': self.data_completion,
            'latest_hours': self.latest_hours,
            'latest_latitude': self.latest_latitude,
            'latest_location_timestamp': self.latest_location_timestamp,
            'site': self.site,
            'device_model': self.device_model,
            'firmware_version': self.firmware_version,
            'configuration_version': self.configuration_version,
            'device_mode': self.device_mode,
            'first_associated': self.first_associated,
            'signal': self.signal,
        }


class Overview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    asset_id = db.Column(db.String(100))
    machine_name = db.Column(db.String(100))
    machine_type = db.Column(db.String(100))
    load_capacity_tonnes = db.Column(db.String(100))
    oem = db.Column(db.String(100))
    model = db.Column(db.String(100))
    vin = db.Column(db.String(100))
    manufacturing_year = db.Column(db.Integer)
    engine_type = db.Column(db.String(100))
    emission_standard = db.Column(db.String(100))
    site = db.Column(db.String(100))
    active_time = db.Column(db.String(20))
    idle_time = db.Column(db.String(20))
    total_on_time = db.Column(db.String(20))
    off_time = db.Column(db.String(20))
    data_completeness = db.Column(db.String(100))
    idle_percentage = db.Column(db.String(100))
    utilisation_percentage = db.Column(db.String(100))
    data_level_percentage = db.Column(db.String(100))
    telematics_found = db.Column(db.String(100))
    activity_data_source = db.Column(db.String(100))
    location_data_source = db.Column(db.String(100))
    hour_meter_data_source = db.Column(db.String(100))
    ownership_type = db.Column(db.String(100))
    owner = db.Column(db.String(100))
    note = db.Column(db.Text)
    subscriptions = db.Column(db.String(100))

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'asset_id': self.asset_id,
            'machine_name': self.machine_name,
            'machine_type': self.machine_type,
            'load_capacity_tonnes': self.load_capacity_tonnes,
            'oem': self.oem,
            'model': self.model,
            'vin': self.vin,
            'manufacturing_year': self.manufacturing_year,
            'engine_type': self.engine_type,
            'emission_standard': self.emission_standard,
            'site': self.site,
            'active_time': self.active_time,
            'idle_time': self.idle_time,
            'total_on_time': self.total_on_time,
            'off_time': self.off_time,
            'data_completeness': self.data_completeness,
            'idle_percentage': self.idle_percentage,
            'utilisation_percentage': self.utilisation_percentage,
            'data_level_percentage': self.data_level_percentage,
            'telematics_found': self.telematics_found,
            'activity_data_source': self.activity_data_source,
            'location_data_source': self.location_data_source,
            'hour_meter_data_source': self.hour_meter_data_source,
            'ownership_type': self.ownership_type,
            'owner': self.owner,
            'note': self.note,
            'subscriptions': self.subscriptions
        }


class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    oem = db.Column(db.String(100), nullable=False)
    latest_call_type = db.Column(db.String(100))
    latest_call = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to Customer model
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # For storing API calls data, we use JSON column
    api_calls = db.Column(db.JSON)

