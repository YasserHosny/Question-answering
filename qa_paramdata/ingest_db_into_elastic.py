import pandas as pd
import pyodbc
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import openpyxl
import os



# Connect to the database
server = 'transimdb-stage.be2231f9be26.database.windows.net' # Replace with your SQL Server name
database = 'Test_AI' # Replace with your database name
username = os.getenv('MSSQL_USERNAME') # Replace with your username
password = os.getenv('MSSQL_PASSWORD') # Replace with your password
driver= '{ODBC Driver 17 for SQL Server}' # Replace with your driver name

def load_data_from_db():
    # Establish a connection to MS SQL Server
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    connection = pyodbc.connect(conn_str)

    # SQL query to fetch data from the "VIEW_DATA_PART" table
    sql_query = "SELECT [PART NUMBER], DESCRIPTION, [Product Line], SUPPLIER, MANUFACTURER, DATASHEET, [FEATURE NAME], [FEATURE VALUE], [FEATURE UNIT], [AVG PRICE], [MIN PRICE] FROM VIEW_DATA_PART"

    # Fetch data into a DataFrame using pandas
    data = pd.read_sql_query(sql_query, connection)

    print('sql data: ', data)

    # Preprocess the "FEATURE NAME" column
    data['FEATURE NAME'] = data['FEATURE NAME'].str.lower()
    # Add additional preprocessing steps as needed (e.g., removing punctuation)

    # Close the database connection
    connection.close()
    return data

def ingest_db_into_elastic():
    data = load_data_from_db()
    # Connect to Elasticsearch running on localhost
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    print('elastic connected')

    # Choose an appropriate index name
    index_name = 'view_data_part'

    # Convert the data to a list of dictionaries for bulk indexing
    documents = data.to_dict(orient='records')
    print('documents: ', documents)

    # Index the data into Elasticsearch
    for doc in documents:
        es.index(index=index_name, document=doc)

ingest_db_into_elastic()  

