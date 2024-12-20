import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI #langserve
from langserve import add_routes #langserve
import uvicorn #application intialization


_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-3.5-turbo")

parser = StrOutputParser()

#system prompt tempalte
system_template = "Translate the following into {language}:"
 
#create the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

#create a chain LCEL
chain = prompt_template | llm | parser

#Syntax for fastapi
app = FastAPI(
  title="SimpleTranslator",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

#pass objects to the add_routes
add_routes(
    app,
    chain,
    path="/chain",
)

#initialize the application
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)