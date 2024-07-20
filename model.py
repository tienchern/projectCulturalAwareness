from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain.vectorstores import FAISS

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

    def __init__(self, country: str, name: str, age: int):
        self.set_parameters(country)
        self._name = name
        self._age = age

        self._llm = OctoAIEndpoint(
            model="meta-llama-3-70b-instruct",
            max_tokens=1024,
            presence_penalty=0,
            temperature=0.1,
            top_p=0.9,
        )

        self._history = ChatMessageHistory()

    def __str__(self) -> str:
        return self._name
    
    def set_parameters(self, country: str):
        self._country = country

        self._retriever = get_context(self._country)
        self._template = """You are a person called {name} from the different culture of {country}. You are {age} years old. You are interacting with the user to teach them about your culture. Be friendly and open, using the provided context as information about your culture. Additionally, the user may reference earlier conversations so use the provided messages as information about earlier conversations.
        Context about {country}: {context}
        
        Continue this conversation:"""

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

        response = chain.invoke(user_input).strip()

        self._history.add_user_message(user_input)
        self._history.add_ai_message(response)
        
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