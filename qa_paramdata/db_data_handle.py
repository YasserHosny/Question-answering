import pyodbc

# Connect to the database
server = 'transimdb-stage.be2231f9be26.database.windows.net' # Replace with your SQL Server name
database = 'Test_AI' # Replace with your database name
username = 'transim-contributor' # Replace with your username
password = 'K0oLT0ols5473Ng%NEER' # Replace with your password
driver= '{ODBC Driver 17 for SQL Server}' # Replace with your driver name



def load_data_from_db(rowsCount):
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

    try:
        cursor.execute(query)
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {str(e)}")

    # Fetch the data
    csvRows = cursor.fetchall()
    # Get the column names
    columns = [column[0] for column in cursor.description]

    # Convert tuples to lists
    csvRows = [list(t) for t in csvRows]

    # print(csvRows)
    # print(columns)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return csvRows, columns