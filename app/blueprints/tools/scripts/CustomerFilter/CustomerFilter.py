import pandas as pd
def main(file_path, org_list):
    # org_list = str(org_list).split(',')
    print(org_list)

    try:
        df = pd.read_csv(file_path)
    except:
        df = pd.read_excel(file_path)

    mask = df['Org Name'].isin(org_list)

    filtered_df = df[mask].copy()

    filtered_df.loc[:, 'Date'] = pd.to_datetime(filtered_df['Date']).dt.strftime('%Y-%m-%d')

    filtered_df.to_csv(file_path, index=False)
