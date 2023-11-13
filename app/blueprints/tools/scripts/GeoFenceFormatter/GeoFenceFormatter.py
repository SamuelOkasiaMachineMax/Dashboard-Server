import time

import pandas as pd
import re
def main(file_path):
    df = pd.read_csv(file_path)

    try:
        df['coordinates'] = df['coordinates'].apply(transform_coordinates)
    except:
        df = pd.read_csv(file_path, header=None)
        # df.loc[-2] = ['dummy', 'dummy']  # adding a row
        # df.index = df.index + 1  # shifting index
        # df = df.sort_index()  # sorting by index

        df.iloc[:, 1] = df.iloc[:, 1].apply(transform_coordinates)
        print(df.iloc[0,:])
        df.drop(index=df.index[0], axis=0, inplace=True)



    df.to_csv(file_path, index=False)




def transform_coordinates(coord_str):
    # Ensure the input is a string
    if not isinstance(coord_str, str):
        raise ValueError(f"Expected a string, got {type(coord_str)}: {coord_str}")

    matches = re.findall(r'\(([^)]+)\)', coord_str)
    transformed_coords = []

    for match in matches:
        try:
            lat, lon = map(float, match.split(','))
            transformed_coords.append([lon, lat])
        except Exception as e:
            print(f"Error processing match {match}: {e}")
            # Handle or raise the exception as appropriate for your use case.

    return transformed_coords