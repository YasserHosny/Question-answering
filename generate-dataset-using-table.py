import csv
import pyodbc
import json
import os

# Connect to the database
# Replace with your SQL Server name
server = 'transimdb-prod.be2231f9be26.database.windows.net'
database = 'MOVE_VP_New'  # Replace with your database name
username = os.getenv('MSSQL_USERNAME')  # Replace with your username
password = os.getenv('MSSQL_PASSWORD')  # Replace with your password
driver = '{ODBC Driver 17 for SQL Server}'  # Replace with your driver name

# Create the connection string
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Connect to the database
conn = pyodbc.connect(conn_str)

cursor = conn.cursor()

# Execute the SQL query
query = """
SELECT TOP 2 pn, mfr_name, plp.part_description, f.feat_name,
    CASE WHEN f.is_numeric = 1 THEN CAST(pfn.feat_number AS VARCHAR(400))
         ELSE pft.feat_text
    END AS feat_value
FROM vp.parts p
INNER JOIN [vp].[manufacturers] man ON p.mfr_id = man.mfr_id
INNER JOIN vp.product_line_parts plp ON p.part_id = plp.part_id
INNER JOIN vp.product_line_features plf ON plp.pl_id = plf.pl_id
INNER JOIN vp.features f ON plf.feat_id = f.feat_id
OUTER APPLY (
    SELECT TOP 1 *
    FROM vp.part_features_numeric pfn
    WHERE plp.plp_id = pfn.plp_id AND f.is_numeric = 1
) pfn
OUTER APPLY (
    SELECT TOP 1 *
    FROM vp.part_features_text pft
    WHERE plp.plp_id = pft.plp_id AND f.is_numeric = 0
) pft
WHERE p.part_id = 89597
"""

cursor.execute(query)
data = cursor.fetchall()

# Format the data as input-output pairs
dataset = []
pnList = []
mfr_nameList = []
part_descriptionList = []
feat_nameList = []
feat_valueList = []

for row in data:
    pn, mfr_name, part_description, feat_name, feat_value = row
    pnList.append(pn)
    mfr_nameList.append(mfr_name)
    part_descriptionList.append(part_description)
    feat_nameList.append(feat_name)
    feat_valueList.append(feat_value)

# Write the dictionary to a file
with open('dataset.json', 'w') as file:
    json.dump({
        "part number": pnList,
        "manufacture name": mfr_nameList,
        "part description": part_descriptionList,
        "feature name": feat_nameList,
        "feature value": feat_valueList
    }, file)

# Load the dictionary from the file
with open('dataset.json', 'r') as file:
    data = json.load(file)

print(data)

# Close the database connection
cursor.close()
conn.close()
