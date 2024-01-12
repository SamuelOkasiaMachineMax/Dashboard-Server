from flask import Blueprint, jsonify, request, current_app
import json
import os
from datetime import datetime
FFTools_blueprint = Blueprint('FFTools', __name__)



@FFTools_blueprint.route('/FFTools/<deveui>/<start_date>/<end_date>', methods=['POST'])
def FFTools(deveui,start_date,end_date):
    print(deveui,start_date,end_date)


    def format_datetime(datetime_str):
        # Convert to datetime object
        dt_obj = datetime.fromisoformat(datetime_str)
        # Format to BigQuery compatible string (add ':00' for seconds)
        return dt_obj.strftime('%Y-%m-%d %H:%M:00')

    start_date = format_datetime(start_date)
    end_date = format_datetime(end_date)

    bigquery_client = current_app.bigquery_client_UK

    query = f"""
         SELECT 
    V.battery_level,  
    V.battery_voltage,
    V.external_voltage,
    V.gsm_signal,
    V.read_at,
    V.source_id

FROM 
    `machinemax-prod-635d.google_cloud_postgresql_public.latest_uplink` U
JOIN 
    `machinemax-prod-635d.google_cloud_postgresql_public.status_teltonika` V ON U.source_id = V.source_id
   
WHERE 
    U.deveui = '{deveui}' AND  V.read_at >= '{start_date}' AND 
    V.read_at <= '{end_date}'
          """

    try:
        # Run the query and get the results
        query_job = bigquery_client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        # Process the results
        data = [{"battery_level": row.battery_level,
                 "battery_voltage": row.battery_voltage,
                 "external_voltage": row.external_voltage,
                 "gsm_signal": row.gsm_signal,
                 "source_id": row.source_id,
                 "read_at": row.read_at,
                 } for row in results]

        latest_data_query = f"""
            SELECT 
                external_voltage,
                gsm_signal,
                read_at
            FROM 
                `machinemax-prod-635d.google_cloud_postgresql_public.latest_status_teltonika`
            WHERE 
                source_id = '{data[0]['source_id']}'
        """

        latest_data_query_job = bigquery_client.query(latest_data_query)
        latest_data_query_data_results = latest_data_query_job.result()
        latest_data = [{"External Voltage": row.external_voltage,
                        "GSM Signal": row.gsm_signal,
                        "Read At": row.read_at,
                        }
                        for row in latest_data_query_data_results][0]

        latest_location_query = f"""
        SELECT  
        latitude,
        longitude
         
        FROM `machinemax-prod-635d.google_cloud_postgresql_public.latest_gps` WHERE deveui = '{deveui}' LIMIT 1000
        """
        latest_location_query_job = bigquery_client.query(latest_location_query)
        latest_location_query_job_results = latest_location_query_job.result()
        latest_location = [{"Latitude": row.latitude,
                            "Longitude": row.longitude, }
                            for row in latest_location_query_job_results][0]

        gps_query = f"""
               SELECT gps, tips, machine_id, accelerometer FROM `machinemax-prod-635d.google_cloud_postgresql_public.source_associations` WHERE source_id = '{data[0]['source_id']}' LIMIT 100
               """
        gps_query_job = bigquery_client.query(gps_query)
        gps_query_job_results = gps_query_job.result()
        gps = [{"Gps": row.gps,
                "Tips": row.tips,
                "Movement":row.accelerometer,
                'Machine ID': row.machine_id,
                'Machine Link': "https://machinemax.com/machines/"+row.machine_id+'?ref=activities'}
                for row in gps_query_job_results][0]


        gps_value = gps['Gps']
        on_with_fix = latest_location['Latitude'] != None and latest_location['Longitude'] != None
        if gps_value and on_with_fix:
            GNSS_value = "On with Fix"
        elif gps_value and not on_with_fix:
            GNSS_value = "ON no fix"
        else:
            GNSS_value = "Not on and no fix"

        GNSS = {"GNSS Status" : GNSS_value}

        machine_id = gps['Machine ID']


        devices_query = f"""
                SELECT  tag FROM `machinemax-prod-635d.google_cloud_postgresql_public.devices` WHERE deveui = '{deveui}' LIMIT 100"""
        devices_query_job = bigquery_client.query(devices_query)
        devices_query_job_results = devices_query_job.result()
        devices = [{"Tag": row.tag}
               for row in devices_query_job_results][0]


        fotaWeb_query = f"""
                SELECT  model FROM `machinemax-prod-635d.google_cloud_postgresql_public.fotaweb_device` WHERE imei = {deveui} LIMIT 1000
                """
        fotaWeb_query_job = bigquery_client.query(fotaWeb_query)
        fotaWeb_query_job_results = fotaWeb_query_job.result()
        fotaWeb = [{"Model": row.model}
               for row in fotaWeb_query_job_results][0]

        speed_query = f"""
                      SELECT speed FROM `machinemax-prod-635d.google_cloud_postgresql_public.machine_latest_location` WHERE machine_id = '{machine_id}' LIMIT 1000
                      """
        speed_query_job = bigquery_client.query(speed_query)
        speed_query_job_results = speed_query_job.result()
        speed = [{"Speed": row.speed}
                   for row in speed_query_job_results][0]


        print(latest_data)
        print(latest_location)

        latest_data = {**latest_data, **latest_location, **gps, **GNSS, **fotaWeb, **speed}
        # I removed devices for space
        print(latest_data)
        # Return as JSON
        return jsonify({'range_data':data, 'latest_data':latest_data})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # FFToolsFile = os.path.join(BASE_DIR, 'FFTools.json')
    #
    # with open(FFToolsFile, 'r') as json_file:
    #     data = json.load(json_file)
    #     # variables = ["GPS coordinates", "GSM signal", "External voltage (mV)"]
    #     variables = variablesList
    #     def parse_date(date_str):
    #         for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
    #             try:
    #                 return datetime.strptime(date_str, fmt)
    #             except ValueError:
    #                 continue
    #         raise ValueError(f"Date format for '{date_str}' is not supported.")
    #
    #     # Convert start and end dates to datetime objects using the parse_date function
    #     start_dt = parse_date(start_date)
    #     end_dt = parse_date(end_date)
    #
    #     # Dictionary to store the filtered results
    #     filtered_results = {}
    #
    #     for device_id, timestamps in data.items():
    #         for timestamp_str, details in timestamps.items():
    #             # Use the parse_date function which tries multiple formats
    #             timestamp = parse_date(timestamp_str)
    #
    #             # Check if the timestamp is within the given range
    #             if start_dt <= timestamp <= end_dt:
    #                 # If the timestamp is within the range, filter out the variables
    #                 filtered_details = {key: value for key, value in details.items() if key in variables}
    #
    #                 # Add the filtered details to the results dictionary
    #                 if device_id not in filtered_results:
    #                     filtered_results[device_id] = {}
    #                 filtered_results[device_id][timestamp_str] = filtered_details
    #
    #     print(filtered_results)


