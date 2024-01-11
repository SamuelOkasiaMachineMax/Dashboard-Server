from flask import Blueprint, jsonify, request, send_from_directory, current_app
from flask import send_file

reports_blueprint = Blueprint('reports', __name__)

from app.blueprints.reports.scripts.US_SUGAR.report import US_Sugar_main

report_dict={ 'US Sugar' : ['Completeness Report', "ExampleReport"],
              'Zeppelin' : ['ExampleReport']

              }

@reports_blueprint.route('/reports', methods=['GET'])
def reports():
    print(report_dict['US Sugar'])
    report_structure = [(customer,name) for customer in report_dict.keys() for name in report_dict[customer]]
    return jsonify(report_structure)



@reports_blueprint.route('/reports/<customer_name>/<name>/<action>', methods=['GET'])
def get(customer_name, name, action):
    if customer_name == 'US Sugar':
        return US_Sugar_main(name,action)
    return 'Report not found', 404

@reports_blueprint.route('/customer-select', methods=['GET'])
def customer_select():
    bigquery_client = current_app.bigquery_client_UK
    query = f"""SELECT id,name FROM `machinemax-prod-635d.google_cloud_postgresql_public.organisations`"""

    try:
            query_job = bigquery_client.query(query)
            results = query_job.result()  # Waits for the job to complete.

            # Process the results
            data = [{"value": row.id,
                     "name": row.name,
                     } for row in results]

            print('done')

            return jsonify({'data':data})

    except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

@reports_blueprint.route('/reports-data_completeness/<customer>', methods=['GET'])
def data_completeness(customer):
    bigquery_client = current_app.bigquery_client_UK

    query = f"""
            WITH DistinctTableA AS (
    SELECT DISTINCT source_id, machine_id
    FROM `machinemax-prod-635d.google_cloud_postgresql_public.source_associations`
),
DistinctTableB AS (
    SELECT DISTINCT source_id, deveui
    FROM `machinemax-prod-635d.google_cloud_postgresql_public.latest_uplink`
)

SELECT
    DA.machine_id,
    M.asset_id,
    DT_A.source_id,
    FD.model,
    DT_B.deveui,
    COALESCE(MAX(LS.updated_at), MAX(LST.updated_at)) AS last_updated_at,
    SUM(DA.off_hours + DA.total_hours) AS data_completeness,
    CASE
        WHEN DATE(COALESCE(MAX(LS.updated_at), MAX(LST.updated_at))) = CURRENT_DATE() THEN 'Responsive'
        ELSE 'Unresponsive'
    END AS status

FROM
    `machinemax-prod-635d.google_cloud_postgresql_public.daily_aggregate` DA
INNER JOIN 
    `machinemax-prod-635d.google_cloud_postgresql_public.machines` M on M.ID = DA.machine_id

LEFT JOIN
    DistinctTableA DT_A ON DA.machine_id = DT_A.machine_id
LEFT JOIN
    DistinctTableB DT_B ON DT_A.source_id = DT_B.source_id
LEFT JOIN 
    `machinemax-prod-635d.google_cloud_postgresql_public.latest_status` LS on LS.deveui = DT_B.deveui
LEFT JOIN
    `machinemax-prod-635d.google_cloud_postgresql_public.fotaweb_device` FD on CAST(FD.imei AS STRING) = DT_B.deveui
LEFT JOIN 
    `machinemax-prod-635d.google_cloud_postgresql_public.latest_status_teltonika` LST on LST.source_id = DT_B.source_id
WHERE
    DA.organisation_id = '{customer}'
    AND DA.date >= DATE_SUB(CURRENT_DATE, INTERVAL 2 DAY)
    AND DA.date <= CURRENT_DATE
    AND M.archived IS NULL
GROUP BY
    DA.machine_id, DT_A.source_id, DT_B.deveui, M.asset_id, FD.model;
"""

    try:
        query_job = bigquery_client.query(query)
        results = query_job.result()  # Waits for the job to complete.

        # Process the results
        data = [{"machine_id": row.machine_id,
                 "asset_id": row.asset_id,
                 "source_id": row.source_id,
                 "model": row.model,
                 "deveui": row.deveui,
                 "last_updated_at": row.last_updated_at,
                 "data_completeness":row.data_completeness,
                 "status":row.status,
                 } for row in results]


        return jsonify({'report':data})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
