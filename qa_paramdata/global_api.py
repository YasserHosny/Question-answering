from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json as jsn
from tapas_reader_qa import get_answer_from_table
from gpt_solution_qa import apply_gpt_sql_query, apply_gpt_sql_elastic_query, apply_gpt_sql_elastic_translate_query


app = Flask(__name__)
# CORS(app, resources={r"/qa": {"origins": "http://localhost:4200"}})
CORS(app)


@app.route('/api/qa', methods=['POST'])
# @cross_origin()
def qa():
    json = request.get_json()
    model_name = json['model_name']
    user_input = json['user_input']
    print(user_input)
    if model_name == "tapas":
        bot_response = get_answer_from_table(user_input)
    elif model_name == "gpt_sql":
        bot_response = apply_gpt_sql_query(user_input)
    elif model_name == "gpt_elastic":
        bot_response = apply_gpt_sql_elastic_translate_query(user_input, "VIEW_DATA_PART")
    
    #print(bot_response)
    response = jsonify({'bot_response': bot_response})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)