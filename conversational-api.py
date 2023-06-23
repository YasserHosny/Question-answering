from transformers import pipeline, Conversation
from flask import Flask, request

app = Flask(__name__)
chatbot = pipeline(model="microsoft/DialoGPT-large")
step = 0
conversation = Conversation() 

@app.route("/", methods=["GET", "POST"])
def chat():
    global step
    global conversation
    if request.method == "POST":
        user_input = request.form["user_input"]
        if step == 0:
            conversation = Conversation(user_input)
        elif user_input != "exit":
            print('here')
            conversation.add_user_input(user_input)
        else:
            return "Conversation ended."
        step+=1
        conversation = chatbot(conversation)
        return conversation.generated_responses[-1]
    return '''
        <form method="post">
            <label for="user_input">User:</label>
            <input type="text" id="user_input" name="user_input"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
