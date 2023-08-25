import pyodbc
import sqlparse
import sqlparse
import requests
import os

# Connect to the database
server = 'transimdb-stage.be2231f9be26.database.windows.net' # Replace with your SQL Server name
database = 'Test_AI' # Replace with your database name
username = os.getenv('MSSQL_USERNAME') # Replace with your username
password = os.getenv('MSSQL_PASSWORD') # Replace with your password
driver= '{ODBC Driver 17 for SQL Server}' # Replace with your driver name

# Elasticsearch server URL
elasticsearch_url = 'http://localhost:9200'

# Index name for which to retrieve the mapping
index_name = 'view_data_part'

def load_data_from_db_VIEW_DATA_PART(rowsCount):
    # Create the connection string
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    # Connect to the database
    connection = pyodbc.connect(conn_str)

    # Execute the SQL query
    query = f"""
    SELECT TOP {rowsCount} "PART NUMBER", DESCRIPTION, "Product Line", SUPPLIER, "MANUFACTURER", DATASHEET, "FEATURE NAME", "FEATURE VALUE", "FEATURE UNIT",
    "AVG PRICE", "MIN PRICE"
        FROM VIEW_DATA_PART
        ORDER BY COM_ID ASC
    """
    #print("query: " + query)
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute(query)
    # Fetch the data
    csvRows = cursor.fetchall()
    # Get the column names
    columns = [column[0] for column in cursor.description]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Create a dictionary to store the data
    jsonRows = {}
    for i, row in enumerate(csvRows):
        for j, item in enumerate(row):
            if i == 0:
                jsonRows[columns[j]] = [item]
            else:
                jsonRows[columns[j]].append(item)

    return jsonRows, csvRows, columns

def load_data_from_db_se_flat_data(rowsCount):
    # Create the connection string
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    # Connect to the database
    connection = pyodbc.connect(conn_str)

    # Execute the SQL query
    query = f"""
    SELECT TOP {rowsCount} [Part Number],	[Manufacturer name],	[Description],	[DataSheet],	[Life Cycle],	[ROHS],	[Product Line],	[Taxonomy],	[Inventory],	[Cross Count],	[REPLACEMENT COUNT],	[YEARS EOL],	[LIFECYCLE SCORE],	[LIFECYCLE RISK],	[ROHS SCORE],	[ROHS RISK],	[MULTI SOURCING SCORE],	[MULTI SOURCING RISK],	[AVAILABILITY RISK],	[RISK GRADE],	[REACH],	[CHINA ROHS],	[LAST CHECK DATE],	[OBSOLESCENCE YEAR],	[FAMILY],	[INTRODUCTION RECOMMENDATION],	[ROHS VERSION],	[AUTOMOTIVE],	[INTRODUCTION DATE]
    FROM se_flat_data
    ORDER BY [Part Number] ASC
    """
    #print("query: " + query)
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute(query)
    # Fetch the data
    csvRows = cursor.fetchall()
    # Get the column names
    columns = [column[0] for column in cursor.description]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Create a dictionary to store the data
    jsonRows = {}
    for i, row in enumerate(csvRows):
        for j, item in enumerate(row):
            if i == 0:
                jsonRows[columns[j]] = [item]
            else:
                jsonRows[columns[j]].append(item)

    return jsonRows, csvRows, columns

def load_data_from_elastic():
    # Endpoint for the mapping request
    mapping_endpoint = f'{elasticsearch_url}/{index_name}/_mapping'

    # Send the GET request to Elasticsearch
    response = requests.get(mapping_endpoint)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        mapping_data = response.json()
        properties = mapping_data[index_name]['mappings']['properties']

         # Extract the property names from the mapping
        property_names = list(properties.keys())
        # print('property_names: ', property_names)
        return property_names
    else:
        print(f"Failed to retrieve mapping. Status code: {response.status_code}, Response: {response.text}")
        return None

def exec_query_over_db(query):
    # Create the connection string
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    # Connect to the database
    connection = pyodbc.connect(conn_str)
    
    #replace semicolon with space
    query = query.replace(";", " ")
    query = query.replace("?", " ")

    # Create a cursor
    cursor = connection.cursor()
    csvRows = []

    try:
        # Exec SP to exec query
        sp_query = "Exec usp_ExecQuery N'" + query + "'"
        cursor.execute("{CALL usp_ExecQuery (?)}", (query))

        # Loop through all result sets returned by the stored procedure
        while True:
            # Fetch all rows from the current result set
            csvRows = cursor.fetchall()
            
            # Get the column names
            columns = [column[0] for column in cursor.description]

            # Check if there are more result sets
            if cursor.nextset():
                # Move to the next result set
                continue
            else:
                # No more result sets, break the loop
                break

    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {str(e)}")
        
    

    # Convert tuples to lists
    csvRows = [list(t) for t in csvRows]

    # print(csvRows)
    # print(columns)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return csvRows, columns

import requests

def exec_elasticsearch_search(elastic_query):
    # Endpoint for the search request
    search_endpoint = f"{elasticsearch_url}/{index_name}/_search"
    # print('elastic_query: ', elastic_query)
    elastic_query = elastic_query[elastic_query.find('{'):]

    # Set the headers for the request
    headers = {"Content-Type": "application/json"}
    # Encode the JSON query string to bytes using UTF-8 encoding
    encoded_query = elastic_query.encode('utf-8')
    # Send the GET request to Elasticsearch for the search
    response = requests.request(method='GET', url= search_endpoint, data=encoded_query, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        search_results = response.json()
        # print('search_results: ', search_results)
        columns = []
        rows = []

        if "hits" in search_results and "hits" in search_results["hits"]:
            for hit in search_results["hits"]["hits"]:
                if "_source" in hit:
                    row = list(hit["_source"].values())
                    rows.append(row)

                    for prop_name in hit["_source"].keys():
                        if prop_name not in columns:
                            columns.append(prop_name)

        print('columns: ', columns)
        print('rows: ', rows)
        return rows, columns
    else:
        print(f"Failed to execute search query. Status code: {response.status_code}, Response: {response.text}")
        return [], []

def parse_sql_query(sql_query):
    sql_query = 'SELECT "FEATURE VALUE" FROM VIEW_DATA_PART WHERE "FEATURE VALUE" = 5 OR "FEATURE VALUE" between 20 and 30'
    # Parse the SQL query using sqlparse
    parsed = sqlparse.parse(sql_query)
    
    # Get the first statement (assuming only one query in the input)
    statement = parsed[0]
    
    # Extract the components of the SQL query
    table_name = None
    columns_selected = []
    where_conditions = []
    from_seen = False
    select_seen = False

    for token in statement.tokens:
        print('token: ', token)


    for token in statement.tokens:
        # Check for the FROM keyword to get the table name
        if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == 'FROM':
            from_seen = True            
        elif from_seen and not token.is_whitespace:
            table_name = str(token)
            from_seen = False

        # Check for the SELECT keyword to get the selected columns
        if  token.value.upper() == 'SELECT':
            select_seen = True
            print("select")
        elif select_seen and not token.is_whitespace:
            print("token: ", token)
            print("token.get_identifiers(): ", token.get_identifiers())
            columns_selected = [str(col) for col in token.get_identifiers()]
            select_seen = False


        if isinstance(token, sqlparse.sql.Where):
            # Extract the where conditions after the WHERE keyword
            for item in token.tokens:
                if item.ttype is None and str(item).strip():
                    where_conditions.append(str(item))

    return {
        'Table': table_name,
        'Columns Selected': columns_selected,
        'Where columns': where_conditions
    }
