import os
from langchain_core.tools import tool
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv

loader = PyPDFLoader("/Users/muahmed/MT/ai/aig-design-july/resources/benefits.pdf")
pdfData = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
splitData = text_splitter.split_documents(pdfData)

collection_name = "benefits_collection"
local_directory = "benefits_vect_embedding"
persist_directory = "/Users/muahmed/MT/ai/aig-design-july/resources/benefits_vect_embedding"

load_dotenv()
azure_ada_open_ai_end_point = os.getenv("AZURE_EMBEDDING_OPENAI_ENDPOINT")
azure_ada_open_ai_key = os.getenv("AZURE_EMBEDDING_OPENAI_API_KEY")
azure_ada_deployment_name = os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME")
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=azure_ada_open_ai_end_point,
    openai_api_key=azure_ada_open_ai_key,
    azure_deployment=azure_ada_deployment_name,
    openai_api_version="2023-07-01-preview",
)

vectDB = Chroma.from_documents(splitData,
                               embeddings,
                               collection_name=collection_name,
                               persist_directory=persist_directory
                               )
vectDB.persist()

ks = ConversationalRetrievalChain.from_llm(AzureChatOpenAI(deployment_name="SMAX-AI-Dev-GPT4"), vectDB.as_retriever())


@tool
def knowledge_tool(question) -> str:
    """API for Benefits Documentation pass the entire user input"""

    chat_history = []
    response = ks({"question": question, "chat_history": chat_history})
    answer = response["answer"]
    print("**TOOL** Knowledge Skills, Question = " + question + " Answer = " + answer)

    return answer
