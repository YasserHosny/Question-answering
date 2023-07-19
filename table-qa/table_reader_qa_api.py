from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from transformers import pipeline, TapasTokenizer, TapasForQuestionAnswering
import torch
import json
from table_reader_qa import get_answer_from_table

app = Flask(__name__)
CORS(app)

model_name = "google/tapas-base-finetuned-wtq"
# load the tokenizer and the model from huggingface model hub
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name, local_files_only=False)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# load the model and tokenizer into a question-answering pipeline
pipe = pipeline("table-question-answering",  model=model, tokenizer=tokenizer, device=device)

with open('table.json', 'r') as file:
    data = json.load(file)

@app.route('/tapas', methods=['POST'])
@cross_origin()
def tapas():
    json = request.get_json()
    user_input = json['user_input']
    print(user_input)
    bot_response = get_answer_from_table(table=data, query=user_input)
    print(bot_response)
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
