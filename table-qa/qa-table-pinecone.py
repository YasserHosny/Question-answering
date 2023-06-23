from datasets import load_dataset
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import pinecone
from tqdm.auto import tqdm

def _preprocess_tables(tables: list):
    processed = []
    # loop through all tables
    for table in tables:
        # convert the table to csv and 
        processed_table = "\n".join([table.to_csv(index=False)])
        # add the processed table to processed list
        processed.append(processed_table)
    return processed


# load the dataset from huggingface datasets hub
data = load_dataset("ashraq/ott-qa-20k", split="train")
print(data[2])


# store all tables in the tables list
tables = []
# loop through the dataset and convert tabular data to pandas dataframes
for doc in data:
    table = pd.DataFrame(doc["data"], columns=doc["header"])
    tables.append(table)

print(tables[2]) 

# set device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# load the table embedding model from huggingface models hub
retriever = SentenceTransformer("deepset/all-mpnet-base-v2-table", device=device)
print(retriever)

# format all the dataframes in the tables list
processed_tables = _preprocess_tables(tables)
# display the formatted table
print(processed_tables[2])


# connect to pinecone environment
pinecone.init(
    api_key="43e24b08-35dd-4765-8738-7768d6eea866",
    environment="asia-southeast1-gcp-free"
)

# you can choose any name for the index
index_name = "table-qa"

# check if the table-qa index exists
if index_name not in pinecone.list_indexes():
    # create the index if it does not exist
    pinecone.create_index(
        index_name,
        dimension=768,
        metric="cosine"
    )

# connect to table-qa index we created
index = pinecone.Index(index_name)
# print(index)


# we will use batches of 64
batch_size = 64

for i in tqdm(range(0, len(processed_tables), batch_size)):
    # find end of batch
    i_end = min(i+batch_size, len(processed_tables))
    # extract batch
    batch = processed_tables[i:i_end]
    # generate embeddings for batch
    emb = retriever.encode(batch).tolist()
    # create unique IDs ranging from zero to the total number of tables in the dataset
    ids = [f"{idx}" for idx in range(i, i_end)]
    # add all to upsert list
    to_upsert = list(zip(ids, emb))
    # upsert/insert these records to pinecone
    _ = index.upsert(vectors=to_upsert)

# check that we have all vectors in index
print(index.describe_index_stats())



def query_pinecone(query):
    # generate embedding for the query
    xq = retriever.encode([query]).tolist()
    # query pinecone index to find the table containing answer to the query
    result = index.query(xq, top_k=1)
    # return the relevant table from the tables list
    return tables[int(result["matches"][0]["id"])]


def get_answer_from_table(table, query):
    # run the table and query through the question-answering pipeline
    answers = pipe(table=table, query=query)
    return answers

from transformers import pipeline, TapasTokenizer, TapasForQuestionAnswering
import torch

model_name = "google/tapas-base-finetuned-wtq"
# load the tokenizer and the model from huggingface model hub
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForQuestionAnswering.from_pretrained(model_name, local_files_only=False)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# load the model and tokenizer into a question-answering pipeline
pipe = pipeline("table-question-answering",  model=model, tokenizer=tokenizer, device=device)
query = "which car manufacturers produce cars with a top speed of above 180 kph?"
table = query_pinecone(query)
print(table)


print(get_answer_from_table(table, query))