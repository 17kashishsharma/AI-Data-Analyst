#build app
#extract schema , to database connect
from sqlalchemy import create_engine, inspect
import json
#to remove the thiniking process which comes in between 
import re 
import sqlite3

db_url="sqlite:///amazon.db"

def extract_schema(db_url):
    engine=create_engine(db_url)

#schema retrieve or extract in main.py file
    inspector=inspect(engine)
    schema={}


    for table_name in inspector.get_table_names():
        columns=inspector.get_columns(table_name)
        schema[table_name]=[col['name'] for col in columns]
    return json.dumps(schema)
#json.dumps- python object to json string 
    
#step 2 TEXT TO SQL USING DEEPSEAK WITH OLLAMA 
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
def text_to_sql(schema , prompt):
    SYSTEM_PROMPT="""
you are an expert sql generator. given a database schema and a user prompt , 
generate a valid sql query that answers the prompt . only use the tables and columns provided in the schema . 
ensure the sql syntax is correct and avoid using any unsupported features. 
output only the sql as your response will be directly used to query data from the database .
no preamble please .
 """

    prompt_template=ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user" , "Schema:\n{schema}\n\nQuestion:{user_prompt}\n\nSQL Query:")

    ])

    model=OllamaLLM(model="deepseek-r1:8b")
    chain =prompt_template | model

# then you have to create LangChain - You create a pipeline (chain) that handles the steps in order.
    raw_response = chain.invoke({
    "schema": schema,
    "user_prompt": prompt
})

    cleaned_response = re.sub(
    r"<think>.*?</think>",
    "",
    str(raw_response),
    flags=re.DOTALL
    ).strip()

    return cleaned_response

if __name__ == "__main__":

    schema = extract_schema(db_url)

    prompt = "tell me the name of all the customers"

    sql_query = text_to_sql(schema, prompt)

    print(sql_query)
 

schema = extract_schema(db_url)

prompt = "tell me the name of all the customers"

sql_query = text_to_sql(schema, prompt)

print("Generated SQL:")
print(sql_query)

conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

try:
    results = cursor.execute(sql_query)
    print("RESULTS:", results.fetchall())
except Exception as e:
    print("SQL ERROR:", e)
finally:
    conn.close()

