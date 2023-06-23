# from transformers import pipeline, Conversation

# # Create a pipeline for conversational AI
# chatbot_pipeline = pipeline("conversational")

# # Define a function to interact with the chatbot
# def chat_with_bot(user_input, conversation_history=None):
#     if conversation_history is not None:
#         response = chatbot_pipeline(user_input, conversation_history[-1], attention_mask=True)
#     else:
#         response = chatbot_pipeline(user_input)
#     return response.generated_responses[-1]

# # Example usage
# while True:
#     user_input = input()
#     if(user_input == "exit"):
#         break
#     conversation = Conversation(user_input)
#     bot_response = chat_with_bot(conversation)
#     print("ChatGPT: ", bot_response)



from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large", padding_side="right", truncation_side="left")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

step = 0
while True:
    user_input = input(">> User:")
    if(user_input.endswith("exit")):
        break
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode( user_input + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
    step+=1
    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
