import os
from langchain_core.tools import tool
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("benefits.pdf")
pdfData = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
splitData = text_splitter.split_documents(pdfData)

collection_name = "benefits_collection"
local_directory = "benefits_vect_embedding"
persist_directory = os.path.join(os.getcwd(), local_directory)

embeddings = OpenAIEmbeddings()
vectDB = Chroma.from_documents(splitData,
                               embeddings,
                               collection_name=collection_name,
                               persist_directory=persist_directory
                               )
vectDB.persist()

ks = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name="gpt-3.5-turbo"), vectDB.as_retriever())


@tool
def knowledge_tool(question) -> str:
    """API for Benefits Documentation pass the entire user input"""

    chat_history = []
    response = ks({"question": question, "chat_history": chat_history})
    answer = response["answer"]
    print("**TOOL** Knowledge Skills, Question = " + question + " Answer = " + answer)

    return answer
