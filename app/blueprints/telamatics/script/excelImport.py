import pandas as pd
# pip install pandas xlrd

# Load the Excel file
def main(file):
    try:
        try:
            df = pd.read_csv(file)
        except:
            pass
        try:
            df = pd.read_excel(file)
        except:
            pass

    except:
        print('Error: Error with file type')
    machine_dict = {}
    # Assume you want to get values from column named 'ColumnName'
    for id,vin in zip(df['AssetID'],df['VIN']):
        # Do something with the value
        machine_dict[vin] = {'AssetID':id}

    return machine_dict



