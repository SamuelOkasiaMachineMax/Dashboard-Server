# from flask import jsonify
# from app import create_app  # Import your Flask app instance
# from app.models import Customer, Machine, Sensor, Overview
# from prettytable import PrettyTable
# import pandas as pd
# import openpyxl.styles
# from flask import send_file
# from datetime import datetime
# import os
#
#
# def Completeness_Report(action):
#
#     customer = Customer.query.filter_by(name='US Sugar').first()
#
#     if not customer:
#         print('Customer not found!')
#         exit()
#
#     sensors = Sensor.query.filter_by(customer_id=customer.id).all()
#     result = [sensor.as_dict() for sensor in sensors]
#     df = pd.DataFrame(result)
#
#     overview = Overview.query.filter_by(customer_id=customer.id).all()
#     overview_result = [over.as_dict() for over in overview]
#     df_overview = pd.DataFrame(overview_result)
#
#     # Sort the DataFrame by 'source_status' and then by 'device_model'
#     sorted_df = df.sort_values(by=['source_status', 'source_name'], ascending=[False, True])
#     sorted_df_overview = df_overview
#
#     current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
#     filename = f"Completeness_Report_{current_time}.xlsx"
#     writer = pd.ExcelWriter(filename, engine='openpyxl')
#
#     sorted_df.to_excel(writer, sheet_name='Sheet1', index=False)
#     sorted_df_overview.to_excel(writer, sheet_name='Sheet2', index=False)
#
#
#     workbook = writer.book
#     worksheet = writer.sheets['Sheet1']
#
#     red_fill = openpyxl.styles.PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
#     green_fill = openpyxl.styles.PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
#     amber_fill = openpyxl.styles.PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
#
#
#     for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):  # starting from 2 to skip the header
#         source_status_cell = row[4]  # Adjust the index (2) if 'source_status' is not the third column
#         if source_status_cell.value == 'UNRESPONSIVE':
#             if action == 'view':
#                 source_status_cell.value = source_status_cell.value + ' red'
#             source_status_cell.fill = red_fill
#
#         elif source_status_cell.value == 'RESPONSIVE':
#             if action == 'view':
#                 source_status_cell.value = source_status_cell.value + ' green'
#             source_status_cell.fill = green_fill
#
#         source_name_cell = row[1]
#         battery_voltage_cell = row[5]  # Adjust the index (2) if 'source_status' is not the third column
#
#         if int(battery_voltage_cell.value) < 2700 and source_name_cell.value == "MaxActive - Cellular":
#             if action == 'view':
#                 battery_voltage_cell.value = battery_voltage_cell.value + ' red'
#             battery_voltage_cell.fill = red_fill
#
#         elif int(battery_voltage_cell.value) < 10000 and source_name_cell.value == "MaxTracker":
#             if action == 'view':
#                 battery_voltage_cell.value = battery_voltage_cell.value + ' red'
#             battery_voltage_cell.fill = red_fill
#
#         battery_status_cell = row[6]
#         if battery_status_cell.value == "DEAD" or battery_status_cell.value == "DISCONNECTED":
#             if action == 'view':
#                 battery_status_cell.value = battery_status_cell.value + ' red'
#             battery_status_cell.fill = red_fill
#
#     worksheet_overview = writer.sheets['Sheet2']
#     for row in worksheet_overview.iter_rows(min_row=2, max_row=worksheet_overview.max_row):  # starting from 2 to skip the header
#         data_completion_cell = row[18]  # Adjust the index (2) if 'source_status' is not the third column
#         if int(str(data_completion_cell.value).replace(':','')) <=  30000:
#             if action == 'view':
#                 data_completion_cell.value = data_completion_cell.value + ' red'
#             data_completion_cell.fill = red_fill
#
#         elif int(str(data_completion_cell.value).replace(':', '')) <= 713000:
#             if action == 'view':
#                 data_completion_cell.value = data_completion_cell.value + ' amber'
#             data_completion_cell.fill = amber_fill
#
#         elif int(str(data_completion_cell.value).replace(':', '')) >= 713000:
#             if action == 'view':
#                 data_completion_cell.value = data_completion_cell.value + ' green'
#             data_completion_cell.fill = green_fill
#
#
#     writer.close()
#
#     if action == "download":
#         response = send_file(filename, as_attachment=True)
#         os.remove(filename)  # Delete the file after sending it
#         return response
#
#     elif action == 'view':
#         #df = pd.read_excel(filename)
#         #df = df.fillna("NULL")  # Replace NaN values with the string "NULL"
#         #os.remove(filename)  # Delete the file after reading its contents
#         #return jsonify(df.to_dict(orient='records'))
#         df1 = pd.read_excel(filename, sheet_name='Sheet1')
#         df2 = pd.read_excel(filename, sheet_name='Sheet2')
#
#         df1 = df1.fillna("NULL")
#         df2 = df2.fillna("NULL")
#
#         os.remove(filename)
#
#         # Convert both DataFrames to dictionaries
#         data1 = df1.to_dict(orient='records')
#         data2 = df2.to_dict(orient='records')
#
#         # Return combined data
#         return jsonify({
#             "Sheet1": data1,
#             "Sheet2": data2
#         })
#
#
# def US_Sugar_main(name,action):
#     if name == "Completeness Report":
#         return(Completeness_Report(action))
#     elif name == "Example2Report":
#         return(Completeness_Report(action))
#
#

sorted_results = sorted(results, key=sort_key)

current_row = 2
status_col_index = 4  # Adjust as per your Excel sheet
data_completeness_col_index = 5  # Adjust as per your Excel sheet

for row in sorted_results:
    last_updated_at_naive = convert_to_naive_utc(row.last_updated_at)
    row_data = [row.deveui, row.model, row.machine_id, row.asset_id, row.status, row.data_completeness]
    ws.append(row_data)

    # Apply coloring based on 'status'
    if row.status == 'Unresponsive':
        ws.cell(row=current_row, column=status_col_index).fill = PatternFill(start_color="FFC7CE",
                                                                             end_color="FFC7CE",
                                                                             fill_type="solid")
    elif row.status == 'Responsive':
        ws.cell(row=current_row, column=status_col_index).fill = PatternFill(start_color="C6EFCE",
                                                                             end_color="C6EFCE",
                                                                             fill_type="solid")

    # Apply coloring based on 'data_completeness'
    print(row.data_completeness)
    data_completeness_value = float(row.data_completeness)
    if data_completeness_value > 71.3:
        ws.cell(row=current_row, column=data_completeness_col_index).fill = PatternFill(start_color="C6EFCE",
                                                                                        end_color="C6EFCE",
                                                                                        fill_type="solid")
    elif data_completeness_value > 3.1:
        ws.cell(row=current_row, column=data_completeness_col_index).fill = PatternFill(start_color="FFEB9C",
                                                                                        end_color="FFEB9C",
                                                                                        fill_type="solid")
    else:
        ws.cell(row=current_row, column=data_completeness_col_index).fill = PatternFill(start_color="FFC7CE",
                                                                                        end_color="FFC7CE",
                                                                                        fill_type="solid")

    current_row += 1