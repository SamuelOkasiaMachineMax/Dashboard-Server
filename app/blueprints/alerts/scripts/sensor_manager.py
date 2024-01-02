from flask import Blueprint, jsonify, request, send_from_directory, current_app

class SensorManager:

    def __init__(self):
        self.bigquery_client = current_app.bigquery_client_UK

    def fetch_battery_data(self):

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
        query_job = self.bigquery_client.query(query)
        return query_job.result()

    def fetch_voltage_data(self):

        query = f"""
                SELECT  lst.external_voltage, lst.gsm_signal, sa.machine_id, ma.organisation_id, org.name
                FROM `machinemax-prod-635d.google_cloud_postgresql_public.latest_status_teltonika` as lst
                LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.source_associations` as sa
                ON lst.source_id = sa.source_id
                LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.machines` AS ma
                ON sa.machine_id = ma.id
                LEFT JOIN `machinemax-prod-635d.google_cloud_postgresql_public.organisations` AS org
                on ma.organisation_id = org.id 
                 """
        query_job = self.bigquery_client.query(query)
        return query_job.result()
