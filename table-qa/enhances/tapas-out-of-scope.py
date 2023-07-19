from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
import json
import torch

model_name = "google/tapas-base-finetuned-wtq"
model = TapasForQuestionAnswering.from_pretrained(model_name)
tokenizer = TapasTokenizer.from_pretrained(model_name)

with open('table.json', 'r') as file:
    data = json.load(file)

table = pd.DataFrame.from_dict(data)
print(table)

while True:
    user_input = input('user: ')
    if(user_input == "exit"):
        break

    # column_weights=[0.5, 0.5, 0.5, 0.5, 0.5]  # Adjust the weights for each column here,

    encoded_input = tokenizer(table=table, queries=user_input, padding="max_length", return_tensors="pt")
    outputs = model(**encoded_input)
    attention_mask = encoded_input["attention_mask"].squeeze().tolist()
    print(attention_mask)
    # Access the logits
    logits = outputs.logits

    # Apply softmax to get match scores (probabilities)
    probs = torch.softmax(logits, dim=-1)

    # Get the match score for each column
    match_scores = probs[0]

    # Convert the match scores to a Python list
    match_scores = match_scores.tolist()
    answer_coordinates = torch.argmax(outputs.logits, dim=-1)
    print("answer_coordinates[0]: ", answer_coordinates[0])

    # # Print the match scores for each column
    # for col_idx, score in enumerate(match_scores):
    #     print(f"Match Score for Column {col_idx}: {score}")

    if outputs.logits[0].argmax() < 100:
        print("Predicted answer: " + "out of scope")
    else:
        predicted_answer_coordinates, predicted_aggregation_indices = tokenizer.convert_logits_to_predictions(
            encoded_input, outputs.logits.detach(), outputs.logits_aggregation.detach()
        )
        print(predicted_answer_coordinates, predicted_aggregation_indices)

        # let's print out the results:
        id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
        aggregation_predictions_string = [id2aggregation[x] for x in predicted_aggregation_indices]

        answers = []
        for coordinates in predicted_answer_coordinates:
            if len(coordinates) == 1:
                # only a single cell:
                answers.append(table.iat[coordinates[0]])
            else:
                # multiple cells
                cell_values = []
                for coordinate in coordinates:
                    cell_values.append(table.iat[coordinate])
                answers.append(", ".join(cell_values))


        print("")
        # for query, answer, predicted_agg in zip(user_input, answers, aggregation_predictions_string):
        print(user_input)
        if aggregation_predictions_string[0] == "NONE":
            print("Predicted answer: " + answers[0])
        else:
            print("Predicted answer: " + aggregation_predictions_string[0] + " > " + answers[0])