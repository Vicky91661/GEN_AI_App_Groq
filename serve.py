from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import os 
from dotenv import load_dotenv
load_dotenv()

from langserve import add_routes

groq_api_key = os.getenv("GROQ_KEY")
model = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


#1. Create prompt template
system_template = "Translate the following info {language}:"
prompt_template = ChatPromptTemplate.from_message([
    ('system',system_template),
    ('user','{text}')
])

## Create the parser

parser = StrOutputParser()

## Create chain

chain = prompt_template|model|parser

## Define the App
app = FastAPI(title = "Langchain Server",
              version="1.0",
              description = "A simple API server using Langchain runnable interfaces"
              )
## Adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)

## Hit the url at => /docs

## By default, many API get created
# 1. /chain/output_schema (GET)
# 2. /chain/config_schema (GET)
# 3. /chain/invoke (POST)
# 4. /chain/batch  (POST)
# 5. /chain/stream  (POST)
# 6. /chain/stream_log  (POST)
# 7. /chain/stream_events  (POST)
# 8. /chain/input_schema (GET)