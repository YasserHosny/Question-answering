import cx_Oracle
import json
import csv
import pandas as pd
from db_data_handle import load_data_from_db_VIEW_DATA_PART

jsonRows, csvRows, columns = load_data_from_db_VIEW_DATA_PART()

# Save the data as JSON
with open('VIEW_DATA_PART.json', 'w') as file:
    json.dump(jsonRows, file)

# Write the data to a CSV file
with open('VIEW_DATA_PART.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)  # Write the column names as the first row
    writer.writerows(csvRows)    # Write the data rows
