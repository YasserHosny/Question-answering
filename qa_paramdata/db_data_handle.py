import pyodbc
import sqlparse

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


import sqlparse

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
