import pandas as pd
import json
import os

def viewDataStatusReport():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    customerMany2One = os.path.join(script_dir, 'customersMany2One.json')
    with open(customerMany2One) as file:
        mapping_dict = json.load(file)


    script_dir_Device_Status = os.path.dirname(os.path.abspath(__file__))
    Device_Status_Report = os.path.join(script_dir_Device_Status, 'Device_Status_Report_2023-11-07_000002.csv')

    df = pd.read_csv(Device_Status_Report)
    df['Customer'] = df['Org Name'].map(mapping_dict)


    # If a key doesn't exist in the dictionary, use the value from 'Other Column'
    df['Customer'].fillna(df['Org Name'], inplace=True)



    customerDStoCustomerSS = os.path.join(script_dir, 'customerDStoCustomerSS.json')
    with open(customerDStoCustomerSS) as file:
        customerDStoCustomerSSDict = json.load(file)

    df = df[df['Customer'].isin(customerDStoCustomerSSDict)]

    summary_df = df.groupby(['Customer']).agg({
        'Source Status': [('count_responsive', lambda x: (x == 'Responsive').sum()),
                          ('count_unresponsive', lambda x: (x == 'Unresponsive').sum())],
        'Sensor Model': [
            ('CELLULAR', lambda x: (x == 'CELLULAR').sum()),
            ('FMT100', lambda x: (x == 'FMT100').sum()),
            ('FMTC130', lambda x: (x == 'FMTC130').sum()),
        ]
    }).reset_index()

    # Now, rename the columns
    summary_df['Customer'] = summary_df['Customer'].map(customerDStoCustomerSSDict)

    summary_df.columns = ['Customer', 'Responsive', 'Unresponsive', 'CELLULAR', 'FMT100', 'FMTC130']



    summary_data_json = summary_df.to_dict(orient='records')



    return summary_data_json


import pandas as pd
import json
import os

#------------------------------------------------------------------
def viewDataStatusReport2():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    customerMany2One = os.path.join(script_dir, 'customersMany2One.json')
    with open(customerMany2One) as file:
        mapping_dict = json.load(file)


    script_dir_Device_Status = os.path.dirname(os.path.abspath(__file__))
    Device_Status_Report = os.path.join(script_dir_Device_Status, 'Device_Status_Report_2023-11-07_000002.csv')

    df = pd.read_csv(Device_Status_Report)
    df['Customer'] = df['Org Name'].map(mapping_dict)


    # If a key doesn't exist in the dictionary, use the value from 'Other Column'
    df['Customer'].fillna(df['Org Name'], inplace=True)



    customerDStoCustomerSS = os.path.join(script_dir, 'customerDStoCustomerSS.json')
    with open(customerDStoCustomerSS) as file:
        customerDStoCustomerSSDict = json.load(file)

    df = df[df['Customer'].isin(customerDStoCustomerSSDict)]

    # Define a function to count sensor types within a specific status

    # Aggregate data
    def count_sensor_types(group, status):
        sensor_counts = group[group['Source Status'] == status]['Sensor Model'].value_counts()
        return sensor_counts.to_dict()

    # Aggregate data
    summary_df = df.groupby('Customer').apply(lambda x: pd.Series({
        'Responsive Detailed': count_sensor_types(x, 'Responsive'),
        'Unresponsive Detailed': count_sensor_types(x, 'Unresponsive'),
        'Responsive Total': (x['Source Status'] == 'Responsive').sum(),
        'Unresponsive Total': (x['Source Status'] == 'Unresponsive').sum()
    })).reset_index()

    # Now, rename the columns
    summary_df['Customer'] = summary_df['Customer'].map(customerDStoCustomerSSDict)

    summary_df.columns = ['Customer', 'Responsive Detailed', 'Unresponsive Detailed', 'Responsive Total', 'Unresponsive Total']



    summary_data_json = summary_df.to_dict(orient='records')



    return summary_data_json
