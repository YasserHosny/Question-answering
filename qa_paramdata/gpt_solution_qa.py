import openai
import pandas as pd
import json
from dotenv import load_dotenv
import os
from db_data_handle import load_data_from_db, exec_query_over_db

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY2')

jsonRows, csvRows, columns = load_data_from_db(1)

def apply_gpt_model(query):
    prompt = """Please regard the following table: {}

    The table name is VIEW_DATA_PART. Use ' as the quote character. Quote column aliases with ". Write a SQL query to answer the following question: {}""".format(jsonRows, query)
    print(prompt)

    request = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=3500
    )
    sql_query = request.choices[0].text

    print("===> {}: {}\n".format(query, sql_query)) 

    result = exec_query_over_db(sql_query)

    return result
