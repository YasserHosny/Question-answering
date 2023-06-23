from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Load the pre-trained GPT2 model and tokenizer
model_name = 'gpt2'  # or 'gpt2-medium', 'gpt2-large', 'gpt2-xl' for larger models
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Read the dataset from the CSV file
dataset_path = 'dataset.csv'
dataset = TextDataset(tokenizer=tokenizer, file_path=dataset_path, block_size=128)

# Prepare the data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./model_output',
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=8,
    save_steps=1000,
    save_total_limit=2
)

# Create the Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Train the model
trainer.train()

# Save the fine-tuned model
output_dir = './fine_tuned_model'
trainer.save_model(output_dir)
tokenizer.save_pretrained('fine_tuned_model')  # Save the tokenizer

