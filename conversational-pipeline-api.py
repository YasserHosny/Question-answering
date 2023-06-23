from transformers import pipeline, Conversation
from flask import Flask, request

app = Flask(__name__)

# Create a pipeline for conversational AI
chatbot_pipeline = pipeline("conversational")

# Define the API endpoint for interacting with the chatbot
@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = request.form["user_input"]
    conversation_history = request.form['conversation_history']
    print(user_input)
    print(conversation_history)

    if conversation_history is not None:
        conversation = Conversation(conversation_history)
        conversation.add_user_input(user_input)
        response = chatbot_pipeline(conversation)
    else:
        response = chatbot_pipeline(user_input)

    bot_response = response.generated_responses[-1]
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)