from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os 

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_KEY")
model = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


#1. Create prompt template
system_template = "Translate the following info {language}:"
prompt_template = ChatPromptTemplate.from_message([
    ('system',system_template),
    ('user','{text}')
])

parser = StrOutputParser()

## Create cahin

chain = prompt_template|model|parser


## Define the App
app = FastAPI(title = "Langchain Server",
              version="1.0",
              description = "A simple API server using Langchain runnale interfaces"
              )
## Adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1")
