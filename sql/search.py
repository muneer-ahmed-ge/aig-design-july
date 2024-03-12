import os
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_EMBEDDING_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_EMBEDDING_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
    openai_api_version="2023-07-01-preview",
)

persist_directory = "/Users/muahmed/MT/ai/aig-design-july/resources/metadata_collection"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name="metadata_collection")

query = "Who was the last technician for WO-00000450 ?"
docs = db.similarity_search(query=query, k=5)
for d in docs:
    e = d.page_content
    idx1 = e.find("ObjectName: ")
    idx2 = e.find("FieldName: ")
    object = e[idx1 + len("FieldName: ") + 1: idx2]
    idx1 = e.find("FieldName: ")
    idx2 = e.find("Metadata:")
    field = e[idx1 + len("FieldName: "): idx2]
    print(object + "." + field)