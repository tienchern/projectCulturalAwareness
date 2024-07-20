

from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate

load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

class Person:
    _country = None
    _name = None
    _model = None
    _llm = None
    _template = None
    _prompt = None

    def __init__(self, country: str, name: str):
        self.set_parameters(country)
        self._name = name

        self._llm = OctoAIEndpoint(
        model="meta-llama-3-70b-instruct",
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9,
        )

    def __str__(self) -> str:
        return self._name
    
    def set_parameters(self, country: str):
        self._country = country

        self._template = """You are a person from the different culture of {country}. You are {age} years old. You are interacting with the user to teach them about your culture. Be friendly and open, using the provided context as information about your culture.
        Question: {question}
        Context: {context}
        Answer:"""
        self._prompt = ChatPromptTemplate.from_template(self._template)

    def say_hi(self) -> str:
        return "Hi there!"

    def respond(self, user_input: str) -> str:
        chain = (
        {"question": RunnablePassthrough(), "country": lambda x: self._country, "context": lambda x: "blank", "age": lambda x: "25"}
        | self._prompt
        | self._llm
        | StrOutputParser()
        )

        return chain.invoke(user_input)