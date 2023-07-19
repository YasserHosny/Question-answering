from transformers import pipeline, TapasTokenizer, TapasForQuestionAnswering
import torch
import json

model_name = "google/tapas-large-finetuned-wtq"
# load the tokenizer and the model from huggingface model hub
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name, local_files_only=False)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# load the model and tokenizer into a question-answering pipeline
pipe = pipeline("table-question-answering",  model=model, tokenizer=tokenizer, device=device)

def get_answer_from_table(table, query):
    answers = pipe(table=table, query=query)
    return answers

# with open('table.json', 'r') as file:
#     data = json.load(file)
#     print(data)
    
# # Example usage
# while True:
#     user_input = input('user: ')
#     if(user_input == "exit"):
#         break
#     bot_response = get_answer_from_table(table=data, query=user_input)
#     print("bot_response: ", bot_response)