from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, TrainingArguments
from transformers import pipeline, Conversation


chatbot_pipeline = pipeline('conversational')


def chat_with_bot(user_input, conversation_history=None):
    if conversation_history is not None:
        response = chatbot_pipeline(user_input, conversation_history[-1], attention_mask=True)
    else:
        response = chatbot_pipeline(user_input)
    return response.generated_responses[-1]

# Example usage
while True:
    user_input = input('user: ')
    if(user_input == "exit"):
        break
    conversation = Conversation(user_input)
    bot_response = chat_with_bot(conversation)
    print("ChatGPT: ", bot_response)