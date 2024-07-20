from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
import speech_recognition as sr

from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from octoai.util import to_file, from_file
from octoai.client import OctoAI

import warnings

load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

class Person:
    _age = None
    _country = None
    _name = None
    _model = None
    _llm = None
    _template = None
    _prompt = None
    _retriever = None
    _history = None
    _r = None
    _mic = None

    def __init__(self, country: str, name: str, age: int):
        warnings.filterwarnings("ignore")
        self.set_parameters(country)
        self._name = name
        self._age = age

        self._r = sr.Recognizer()

        self._mic = sr.Microphone()

        self._llm = OctoAIEndpoint(
            model="meta-llama-3-70b-instruct",
            max_tokens=1024,
            presence_penalty=0,
            temperature=0.1,
            top_p=0.9,
        )
        
        self._client = OctoAI(
            api_key= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiIxYzliODgxNy0yMGM5LTRkOTEtODZiYi03ZmIyN2E1Yzk5ZmEiLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiIwMWNkMWI5OS1jNmE3LTQyN2QtYTkzMC1mNjE1OTBlZjA0YTgiLCJ1c2VySWQiOiIxOGQ1ODljMi03OTM0LTQ4YjAtYTdjMi01YmUzZjg5NTFiZDUiLCJhcHBsaWNhdGlvbklkIjoiYTkyNmZlYmQtMjFlYS00ODdiLTg1ZjUtMzQ5NDA5N2VjODMzIiwicm9sZXMiOlsiRkVUQ0gtUk9MRVMtQlktQVBJIl0sInBlcm1pc3Npb25zIjpbIkZFVENILVBFUk1JU1NJT05TLUJZLUFQSSJdLCJhdWQiOiIzZDIzMzk0OS1hMmZiLTRhYjAtYjdlYy00NmY2MjU1YzUxMGUiLCJpc3MiOiJodHRwczovL2lkZW50aXR5Lm9jdG8uYWkiLCJpYXQiOjE3MjE0OTY0NDB9.qGjTuLmTfWFxqsGFHTWpsJlTHPPR-w8ucJfP4LmQwUUaB6NVtg2sI23MukS6WOVcfwsWQIy1NieT2fd0XZKogJ5J1-jySHxcFINUbn6i3V2gBUbtlWeeAPp7_aWTs55utvqANIj5jwcfX9s7jaxZyVstfpsSzb-PdGsI1BBliydRwvKDb_qN6OxAYk985O9KAD2T482nRIs3r_0DdKYaQRa3vgQoEeIZ1lL2tGnWEZtByrtAavmBj7lES7OOcYD8bmQ7DtRSjLAkzNx3wqWTYzuPBvP69QSV2k2DdFRDBt0VuNrFKe7GU4IgWYjqwsl5RMUldRZUhPa37lzq5oPtvg"
        )

        self._history = ChatMessageHistory()

    def __str__(self) -> str:
        return self._name
    
    def set_parameters(self, country: str):
        self._country = country

        self._retriever = get_context(self._country)
        self._template = """You are a person called {name} from the different culture of {country}. You are {age} years old. You are interacting with the user to teach them about your culture. Be friendly and open, using the provided context as information about your culture. Additionally, the user may reference earlier conversations so use the provided messages as information about earlier conversations.
        Context about {country}: {context}
        
        Reply to this conversation for the AI only and wait for the human:"""

        self._prompt = ChatPromptTemplate.from_messages([
            ("system", self._template),
            MessagesPlaceholder(variable_name="messages"),
            """
            Human: {question}
            AI:
            """
        ])

    def say_hi(self) -> str:
        return "Hi there!"

    def respond(self, user_input: str) -> str:
        chain = (
            { "question": RunnablePassthrough(),
              "country": lambda x: self._country,
              "context": self._retriever,
              "age": lambda x: self._age,
              "messages": lambda _: self._history.messages,
              "name": lambda _: self._name } 
            | self._prompt
            | self._llm
            | StrOutputParser()
        )

        with self._mic as source:
            self._r.adjust_for_ambient_noise(source)
            print("\n" * 10 + "listening")
            audio = self._r.listen(source)
            print("done")

            user_input = self._r.recognize_google(audio)

        response = chain.invoke(user_input).strip()

        self._history.add_user_message(user_input)
        self._history.add_ai_message(response)
        
        image_resp = ""
        images = ""
        image_resp = self._client.image_gen.generate_sdxl(
            prompt=user_input + '\n' + response
            )
        images = image_resp.images
            
        
        to_file(images[0], "output.jpg")
        
        return response
    
def get_context(country: str):
    url = "https://en.wikipedia.org/wiki/Culture_of_" + country

    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
        ("h4", "Header 4"),
        ("div", "Divider")
    ]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    # for local file use html_splitter.split_text_from_file(<path_to_file>)
    html_header_splits = html_splitter.split_text_from_url(url)
    chunk_size = 1024
    chunk_overlap = 128
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Split
    splits = text_splitter.split_documents(html_header_splits)

    embeddings = OctoAIEmbeddings()

    vector_store = FAISS.from_documents(
    splits,
    embedding=embeddings
)

    retriever = vector_store.as_retriever()

    return retriever