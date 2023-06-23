from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask import Flask, request

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
chat_history_ids = None

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_history_ids
    if request.method == "POST":
        user_input = request.form["user_input"]
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response
    return '''
        <form method="post">
            <label for="user_input">User:</label>
            <input type="text" id="user_input" name="user_input"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
