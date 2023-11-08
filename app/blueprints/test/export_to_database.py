import pandas as pd
from app import db
from app.models import Sensor,Customer,Overview  # Adjust the import based on where your models are defined
import os
from datetime import timedelta, datetime

customerID = 4
def string_to_timedelta(time_str):
    """Converts a string formatted as hh:mm:ss or hh:mm to a timedelta object."""
    if isinstance(time_str, float):  # Handle float values (like NaN) from pandas read_csv
        return timedelta(hours=0, minutes=0, seconds=0)

    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours, minutes = parts
        seconds = 0
    else:
        raise ValueError(f"Unexpected time format: {time_str}")

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def convert_to_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y/%m/%d').date()
    except Exception as e:
        return None
def utilisation_calculator(utilisation_value):
    try:
        return str(1000 - int(utilisation_value))
    except:
        return 'NULL'


def populate_sensors_from_excel():
    # Read the Excel file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SENSORS_CSV_PATH = os.path.join(BASE_DIR, 'sensors.csv')
    df = pd.read_csv(SENSORS_CSV_PATH)
    # customer = Customer(name='US Sugar',
    #                     orgID='f97bbc91-e293-450d-8d6c-9ca94b40a406'
    #                     )
    # db.session.add(customer)
    # print('done')
    # Iterate over each row in the dataframe
    for _, row in df.iterrows():
        # Create a new Sensor instance for each row
        sensor = Sensor(
            imei=row['IMEI'],
            source_name=row['Source Name'],
            asset_id=row['AssetID'],
            machine_name=row['MachineName'],
            source_status=row['Source Status'],
            battery_voltage=row['Battery Voltage (mV)'],
            battery_status=row['Battery Status'],
            signal_status=row['Signal Status'],

            latest_connection=row['Latest Connection'],
            data_completion="15:04:00",

            latest_hours=row['Latest Hours'],
            latest_latitude=row['Latest Latitude'],
            latest_longitude=row['Latest Longitude'],
            latest_location_timestamp=row['Latest Location Timestamp'],
            site=row['Site'],
            device_model=row['Device Model'],
            firmware_version=row['Firmware Version'],
            configuration_version=row['Configuration Version'],
            device_mode=row['Device Mode'],
            first_associated=row['First Associated'],
            signal=row['Signal'],
            customer_id=customerID  # Hardcoded for this example
        )

        # Add the sensor to the session and commit
        db.session.add(sensor)

    # Commit all changes
    db.session.commit()


def data_completeness_calculator(on,off):
    try:
        completeness =  str(int(str(on).replace(':','')) + int(str(off).replace(':','')))

        x = 6 - len(completeness)
        completeness = completeness + x*'0' #just to add remaining zero's so its 6 characters long

        completeness_formatted =  ':'.join([completeness[i:i+2] for i in range(0, len(completeness), 2)])


        return completeness_formatted
    except Exception as e:

        return '00:00:00'


def populate_overview_from_excel():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MACHINES_CSV_PATH = os.path.join(BASE_DIR, 'overview.csv')
    df = pd.read_csv(MACHINES_CSV_PATH)



    for _, row in df.iterrows():
        start_date = convert_to_date(row['StartDate'])
        end_date = convert_to_date(row['EndDate'])

        total_on = string_to_timedelta(row['Total On (hh:mm)'])
        total_off = string_to_timedelta(row['Off (hh:mm)'])
        data_completeness = total_on + total_off
        data_completeness_str = str(data_completeness)

        overview = Overview(
            start_date=start_date,
            end_date=end_date,
            asset_id=row['AssetID'],
            machine_name=row['MachineName'],
            machine_type=row['MachineType'],
            load_capacity_tonnes=row['Load Capacity (Tonnes)'],
            oem=row['OEM'],
            model=row['Model'],
            vin=row['VIN'],
            manufacturing_year=row['Manufacturing year'],
            engine_type=row['EngineType'],
            emission_standard=row['EmissionStandard'],
            site=row['Site'],
            active_time=row['Active (hh:mm)'],
            idle_time=row['Idle (hh:mm)'],
            total_on_time=row['Total On (hh:mm)'],
            off_time=row['Off (hh:mm)'],

            data_completeness=data_completeness_calculator(row['Total On (hh:mm)'], row['Off (hh:mm)']),

            idle_percentage=row['Idle (%)'],

            utilisation_percentage=utilisation_calculator(row['Idle (%)']),

            data_level_percentage=row['Data Level (%)'],
            telematics_found=row['Telematics found'],
            activity_data_source=row['Activity Data Source'],
            location_data_source=row['Location Data Source'],
            hour_meter_data_source=row['Hour Meter Data Source'],
            ownership_type=row['Ownership type'],
            owner=row['Owner'],
            note=row['Note'],
            subscriptions=row['Subscriptions'],

            customer_id = customerID  # Hardcoded for this example

        )

        db.session.add(overview)

    db.session.commit()

