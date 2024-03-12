import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
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

loader = CSVLoader(
    file_path="/Users/muahmed/MT/ai/aig-design-july/resources/metadata.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["ObjectName","FieldName","Metadata"],
    },
)
metadata_documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
splitData = text_splitter.split_documents(metadata_documents)

db = Chroma.from_documents(splitData,
                               embeddings,
                               collection_name="metadata_collection",
                               persist_directory="/Users/muahmed/MT/ai/aig-design-july/resources/metadata_collection"
                               )
db.persist()