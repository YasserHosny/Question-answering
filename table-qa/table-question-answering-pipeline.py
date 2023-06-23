from transformers import pipeline
import pandas as pd
import chardet
import json

oracle = pipeline(model="google/tapas-base-finetuned-wtq")
# table = {
#     "Repository": ["Transformers", "Datasets", "Tokenizers"],
#     "Stars": ["36542", "4512", "3934"],
#     "Contributors": ["651", "77", "34"],
#     "Programming language": ["Python", "Python", "Rust, Python and NodeJS"],
# }


# Load the dictionary from the file
with open('dataset.json', 'r') as file:
    table = json.load(file)

print(table)

# Example usage
while True:
    user_input = input('user: ')
    if(user_input == "exit"):
        break
    bot_response = oracle(query=user_input, table=table)
    print("ChatGPT: ", bot_response)