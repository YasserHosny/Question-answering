from transformers import Conversation, pipeline
from transformers import Conversation, ConversationalPipeline, AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import chardet

with open('dataset.csv', 'rb') as f:
    result = chardet.detect(f.read())
encoding = result['encoding']

# Read the CSV file using the detected encoding
data = pd.read_csv('dataset.csv')

# Fine-tune the pipeline on the new dataset
conversations = []
for _, row in data.iterrows():
    conversation = Conversation()
    conversation.add_user_input(row['User Input'])
    conversation.add_user_input(row['Bot Response'])
    conversations.append(conversation)

# Create a pipeline for conversational AI
chatbot_pipeline = pipeline("conversational") 

# # Train the conversational pipeline
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# chatbot_pipeline = ConversationalPipeline(model=model, tokenizer=tokenizer)
# chatbot_pipeline.train(conversations)

# Save the new model and tokenizer
chatbot_pipeline.model.save_pretrained("new_model/")
chatbot_pipeline.tokenizer.save_pretrained("new_tokenizer/")
