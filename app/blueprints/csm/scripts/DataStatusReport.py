import pandas as pd
import json
import os

def viewDataStatusReport(file_path):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    customerMany2One = os.path.join(script_dir, 'customersMany2One.json')
    with open(customerMany2One) as file:
        mapping_dict = json.load(file)

    # Device_Status_Report = os.path.join(script_dir, 'Device_Status_Report_2023-11-07_000002.csv')
    df = pd.read_csv(file_path)
    df['Customer'] = df['Org Name'].map(mapping_dict)
    df['Customer'].fillna(df['Org Name'], inplace=True)

    customerDStoCustomerSS = os.path.join(script_dir, 'customerDStoCustomerSS.json')
    with open(customerDStoCustomerSS) as file:
        customerDStoCustomerSSDict = json.load(file)

    df = df[df['Customer'].isin(customerDStoCustomerSSDict)]
    # Define sensor types
    sensor_types = ['FMT100', 'CELLULAR', 'LORA', 'FMC225', 'FMC230']

    # Initialize columns for each sensor type
    for sensor in sensor_types:
        for status in ['Responsive', 'Unresponsive']:
            col_name = f'{status}_{sensor}'
            df[col_name] = 0
            df.loc[df['Source Status'] == status, col_name] = df['Sensor Model'].apply(lambda x: 1 if x == sensor else 0)

    df['Total Responsive'] = df['Source Status'].apply(lambda x: 1 if x == 'Responsive' else 0)
    df['Total Unresponsive'] = df['Source Status'].apply(lambda x: 1 if x == 'Unresponsive' else 0)

    # Aggregate data
    agg_funcs = {f'{status}_{sensor}': 'sum' for sensor in sensor_types for status in ['Responsive', 'Unresponsive']}
    agg_funcs['Total Responsive'] = 'sum'
    agg_funcs['Total Unresponsive'] = 'sum'

    summary_df = df.groupby('Customer').agg(agg_funcs).reset_index()

    return summary_df.to_dict(orient='records')
