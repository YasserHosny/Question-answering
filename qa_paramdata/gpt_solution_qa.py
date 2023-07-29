import openai
import pandas as pd
import json
from dotenv import load_dotenv
import os
from db_data_handle import load_data_from_db, exec_query_over_db, parse_sql_query

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY2')

jsonRows, csvRows, columns = load_data_from_db(1)

def apply_gpt_model(query):
    prompt = """Ignore any previous conversations. Please regard the following table columns: {}

    The table name is VIEW_DATA_PART. Use ' as the quote character. Quote column aliases with ". Write a MS SQL Server query to answer the following question: 
    ''
    {}
    ''
    """.format(columns, query)
    print(prompt)

    sql_query = getQueryFromChatGPT(prompt)

    print("===> {}: {}\n".format(query, sql_query)) 

    try:
        rows, cols = exec_query_over_db(sql_query)
    except Exception as e:
        # Handle the exception
        print(f"An error occurred(gpt_solution_qa): {str(e)}")
        rows = []
        cols = []
        # Retry get query from ChatGPT
        sql_query = getQueryFromChatGPT(prompt)
        rows, cols = exec_query_over_db(sql_query)

    return rows, cols, sql_query

def getQueryFromChatGPT(prompt):
    request = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=3500
    )
    sql_query = request.choices[0].text
    print(request)

    # Remove any characters before the "SELECT" word in the SQL query
    select_index = sql_query.find("SELECT")
    if select_index != -1:
        sql_query = sql_query[select_index:]

    return sql_query

def convert_to_table(rows, cols):
    # Start building the HTML table
    html_table = "<table>\n"

    # Add the table header
    html_table += "  <tr>\n"
    for column in cols:
        html_table += f"    <th>{column}</th>\n"
    html_table += "  </tr>\n"

    # Loop through the rows
    for row in rows:
        html_table += "  <tr>\n"
        for value in row:
            html_table += f"    <td>{value}</td>\n"
        html_table += "  </tr>\n"

    # Close the HTML table
    html_table += "</table>"

    return html_table
