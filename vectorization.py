#!/usr/bin/env python
# coding: utf-8

# # Summarizing a Shooter's Description

# In[1]:


import os

def loadShooterDesc(directory_path):
   shooter_desc = {}
   
   for filename in os.listdir(directory_path):
      if filename.endswith(".txt"):  # assuming shooter_desc are in .txt files
         file_path = os.path.join(directory_path, filename)

         with open(file_path) as f:
            raw_shooter_desc = f.read()

         filename_without_ext = os.path.splitext(filename)[0]  # remove .txt extension
         shooter_desc[filename_without_ext] = [text.strip() for text in raw_shooter_desc.split('=====')]

   return shooter_desc


# In[2]:


shooter_desc = loadShooterDesc('.')
shooter_desc


# In[3]:


docs = [{'text': filename + ' | ' + section, 'path': filename} for filename, sections in shooter_desc.items() for section in sections]

# Sample the resulting data
docs[:2]


# In[4]:


un = "user1"
pw = "yoominchoi1234A"
cs = "localhost/FREEPDB1"


# In[5]:


import oracledb
connection = oracledb.connect(user=un, password=pw, dsn=cs)


# In[6]:


table_name = 'shooter_desc'

with connection.cursor() as cursor:
    # Create the table
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id NUMBER PRIMARY KEY,
            payload CLOB CHECK (payload IS JSON),
            vector VECTOR
        )"""
    try:
        cursor.execute(create_table_sql)
    except oracledb.DatabaseError as e:
        raise

    connection.autocommit = True    


# In[7]:


from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L12-v2')


# In[8]:


import array

# Define a list to store the data
data = [
    {"id": idx, "vector_source": row['text'], "payload": row}
    for idx, row in enumerate(docs)
]

# Collect all texts for batch encoding
texts = [f"{row['vector_source']}" for row in data]

# Encode all texts in a batch
embeddings = encoder.encode(texts, batch_size=32, show_progress_bar=True)

# Assign the embeddings back to your data structure
for row, embedding in zip(data, embeddings):
    row['vector'] = array.array("f", embedding)


# In[9]:


import json

with connection.cursor() as cursor:
    # Truncate the table
    cursor.execute(f"truncate table {table_name}")
    prepared_data = [(row['id'], json.dumps(row['payload']), row['vector']) for row in data]

    # Insert the data
    cursor.executemany(
        f"""INSERT INTO {table_name} (id, payload, vector)
            VALUES (:1, :2, :3)""", prepared_data)
    
    connection.commit()


# In[10]:


with connection.cursor() as cursor:
    # Define the query to select all rows from a table
    query = f"SELECT * FROM {table_name}"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the rows
    for row in rows[:5]:
        print(row)


# # Vector retrieval and Large Language Model generation
# ## 1) Vectorize the "question"

# In[11]:


topK = 3

sql = f"""select payload, vector_distance(vector, :vector, COSINE) as score
from {table_name}
order by score
fetch approx first {topK} rows only"""


# In[12]:


question = "Combine the each description of the shooter into a paragraph"


# In[13]:


with connection.cursor() as cursor:
    embedding = list(encoder.encode(question))
    vector = array.array("f", embedding)
    
    results  = []
    
    for (info, score, ) in cursor.execute(sql, vector=vector):
        text_content = info.read()
        results.append((score, json.loads(text_content)))


# In[14]:


import pprint
pprint.pp(results)


# ## 2) Create the LLM prompt

# In[15]:


from transformers import LlamaTokenizerFast
import sys

tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")
tokenizer.model_max_length = sys.maxsize

def truncate_string(string, max_tokens):
    # Tokenize the text and count the tokens
    tokens = tokenizer.encode(string, add_special_tokens=True) 
    # Truncate the tokens to a maximum length
    truncated_tokens = tokens[:max_tokens]
    # transform the tokens back to text
    truncated_text = tokenizer.decode(truncated_tokens)
    return truncated_text


# In[16]:


# transform docs into a string array using the "paylod" key
docs_as_one_string = "\n=========\n".join([doc["text"] for doc in docs])
docs_truncated = truncate_string(docs_as_one_string, 1000)


# In[17]:


prompt = f"""\
    <s>[INST] <<SYS>>
    You are a helpful assistant named Oracle chatbot. 
    USE ONLY the sources below and ABSOLUTELY IGNORE any previous knowledge.
    Use Markdown if appropriate.
    Assume the customer needs a clear description.
    <</SYS>> [/INST]

    [INST]
    Respond to PRECISELY to this question: "{question}.",  USING ONLY the following information and IGNORING ANY PREVIOUS KNOWLEDGE.
    Include code snippets and commands where necessary.
    NEVER mention the sources, always respond as if you have that knowledge yourself. Do NOT provide warnings or disclaimers.
    =====
    Sources: {docs_truncated}
    =====
    Answer (One paragraph, maximum 2 sentences, maximum 50 words, 90% spartan):
    [/INST]
    """
print(prompt)  # Print the prompt to verify its formatting


# ## 3) Call the Generative AI Service LLM

# In[18]:


import oci
import logging
from oci.generative_ai_inference.models import LlamaLlmInferenceRequest, GenerateTextDetails, OnDemandServingMode

logging.basicConfig(level=logging.INFO)

compartment_id = 'ocid1.tenancy.oc1..aaaaaaaaj4ccqe763dizkrcdbs5x7ufvmmojd24mb6utvkymyo4xwxyv3gfa'
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('config', CONFIG_PROFILE)

# Service endpoint
endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

# GenAI client
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))


# In[19]:


generate_text_request = oci.generative_ai_inference.models.LlamaLlmInferenceRequest()

generate_text_request.prompt = prompt
generate_text_request.is_stream = False #SDK doesn't support streaming responses, feature is under development
generate_text_request.max_tokens = 1500
generate_text_request.temperature = 0.1
generate_text_request.top_p = 0.7
generate_text_request.frequency_penalty = 0.0

generate_text_detail = oci.generative_ai_inference.models.GenerateTextDetails(
    serving_mode=OnDemandServingMode(model_id="meta.llama-2-70b-chat"),
    compartment_id="ocid1.tenancy.oc1..aaaaaaaaj4ccqe763dizkrcdbs5x7ufvmmojd24mb6utvkymyo4xwxyv3gfa",
    inference_request=generate_text_request

)
generate_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="meta.llama-2-70b-chat")
generate_text_detail.compartment_id = compartment_id
generate_text_detail.inference_request = generate_text_request


# In[20]:


try:
    generate_text_response = generative_ai_inference_client.generate_text(generate_text_detail)
    response = generate_text_response.data.inference_response.choices[0].text
    # logging.info("Full Response: %s", response.strip())
except Exception as e:
    logging.error("Error occurred: %s", str(e))
    response = None
    
if response:
    # response_length = len(response.strip())
    # print(f"Response Length: {response_length}")
    # print("Summary of the shooter:")
    print(response.strip())
else:
    print("No response received or response is empty.")

# print(response.strip())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## (Ignore) For Debugging & Logging

# In[21]:


test_prompt = "Describe the characteristics of a good AI assistant."
generate_text_request.prompt = test_prompt

try:
    generate_text_response = generative_ai_inference_client.generate_text(generate_text_detail)
    response = generate_text_response.data.inference_response.choices[0].text
    print("Test Response:")
    print(response.strip())
except Exception as e:
    print(f"Error: {str(e)}")


# In[ ]:


import logging

logging.basicConfig(level=logging.INFO)

try:
    generate_text_response = generative_ai_inference_client.generate_text(generate_text_detail)
    response = generate_text_response.data.inference_response.choices[0].text
    logging.info("Full Response: %s", response.strip())
except Exception as e:
    logging.error("Error occurred: %s", str(e))


# In[ ]:


if response:
    print("Full Response:")
    print(response.strip())
else:
    print("No response received or response is empty.")


# In[ ]:


response_length = len(response.strip())
print(f"Response Length: {response_length}")
print(response.strip())


# In[ ]:




