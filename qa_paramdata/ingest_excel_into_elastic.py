import pandas as pd
import pyodbc
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
import openpyxl


# Connect to the database
# Replace with your SQL Server name
server = 'transimdb-stage.be2231f9be26.database.windows.net'
database = 'Test_AI'  # Replace with your database name
username = 'transim-contributor'  # Replace with your username
password = 'K0oLT0ols5473Ng%NEER'  # Replace with your password
driver = '{ODBC Driver 17 for SQL Server}'  # Replace with your driver name


def load_data_from_excel(index_name):
    excel_file = "C:\Work Data\Documents\P5\AI ChatBot\SE_Data_Flat_1K_Filtered.xlsx"
    sheet_name = "Sheet1"  # Replace with the name of your sheet

    data_frame = pd.read_excel(
        excel_file, sheet_name=sheet_name, keep_default_na=False)

    # print("data_frame: ", data_frame[:1])
    # data_frame = data_frame.fillna('')
    print("data_frame: ", data_frame[:1].to_dict(orient='records'))
    actions = generate_actions(data_frame, index_name)
    return data_frame, actions


def generate_actions(data_frame, index_name):
    for index, row in data_frame.iterrows():
        action = {
            "_index": index_name,
            "_source": row.to_dict()
        }
        yield action


def ingest_excel_into_elastic():
    index_name = "se_flat_data"
    data_frame, actions = load_data_from_excel(index_name)
    # Connect to Elasticsearch running on localhost
    es = Elasticsearch(
        hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    # Convert the data to a list of dictionaries for bulk indexing
    documents = data_frame[:1].to_dict(orient='records')
    print('documents: ', documents)

    # Index settings with 'ignore_malformed'
    index_settings = {
        "settings": {
            "mapping": {
                "ignore_malformed": True
            }
        }
    }
    es.indices.create(index=index_name, body=index_settings, ignore=400)  # ignore 400 status (index already exists)
    # Ingest data into the index
    helpers.bulk(es, actions)


    # # Create the index with the specified settings
    # es.indices.create(index=index_name, body=index_settings)

    # # Use the `helpers.bulk` function to perform the bulk indexing
    # for doc in documents:
    #     helpers.bulk(es, index_name, doc)

    # # Create the index with the defined mapping
    # es.indices.create(index=index_name)
    # index = es.indices.get(index=index_name)
    # index.settings(
    #     index={'mapping': {'ignore_malformed': True}}
    # )

    # # Index the data into Elasticsearch
    # for doc in documents:
    #     es.index(index=index_name, document=doc)
    #     # helpers.bulk(es, index_name, doc)
ingest_excel_into_elastic()
