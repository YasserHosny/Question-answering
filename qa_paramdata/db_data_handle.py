import cx_Oracle

dsn = cx_Oracle.makedsn(host='qa-ora.cbt3zdgittrj.us-east-1.rds.amazonaws.com', port='1521', service_name='ORCL')

def load_data_from_db(rowsCount):
    # Execute the SQL query
    query = f"""
    SELECT *
    FROM (SELECT *
        FROM VIEW_DATA_PART
        ORDER BY COM_ID) table_data
    FETCH FIRST {rowsCount} ROWS ONLY
    """
    #print("query: " + query)
    # Create a cursor
    connection = cx_Oracle.connect(user='SCFM', password='SCFM', dsn=dsn)
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
    #replace semicolon with space
    query = query.replace(";", " ")
    query = query.replace("?", " ")

    # Create a cursor
    connection = cx_Oracle.connect(user='SCFM', password='SCFM', dsn=dsn)
    cursor = connection.cursor()

    cursor.execute(query)
    # Fetch the data
    csvRows = cursor.fetchall()
    # Get the column names
    columns = [column[0] for column in cursor.description]

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return csvRows