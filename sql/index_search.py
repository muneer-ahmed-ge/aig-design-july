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

question = "Who was the last technician for WO-00000450 ?"
question = "Who was the last technician for WO-00000450 ?"
question = "Find out WO-00000450 total Work Order Lines of Line Type = 'Labor' ?"
question = "How many work order exists ?"  # SELECT COUNT(*) FROM SVMXC__Service_Order__c
question = "What is the most common Line Type of Work Order Line"  # SELECT SVMXC__Line_Type__c, COUNT(*) as count FROM SVMXC__Service_Order_Line__c GROUP BY SVMXC__Line_Type__c ORDER BY count DESC LIMIT 1
question = "What are the Line Types for WO-00000450 ?"

docs = db.similarity_search(query=question, k=5)

dict = {'SVMXC__Service_Order__c': [], 'SVMXC__Service_Order_Line__c':[],
        'SVMXC__Service_Group_Members__c':[], 'SVMXC__Installed_Product__c' : []}
for d in docs:
    e = d.page_content
    idx1 = e.find("ObjectName: ")
    idx2 = e.find("FieldName: ")
    object = e[idx1 + len("FieldName: ") + 1: idx2]
    object = object.replace("\n", "")
    idx1 = e.find("FieldName: ")
    idx2 = e.find("Metadata:")
    field = e[idx1 + len("FieldName: "): idx2]
    field = field.replace("\n", "")
    dict.get(object).append(field)

service_order = ""
for e in dict.get("SVMXC__Service_Order__c"):
    service_order += "\"" + e + "\" VARCHAR, \n"
print(service_order)

service_order_line = ""
for e in dict.get("SVMXC__Service_Order_Line__c"):
    service_order_line += "\"" + e + "\" VARCHAR, \n"
print(service_order_line)

group_members = ""
for e in dict.get("SVMXC__Service_Group_Members__c"):
    group_members += "\"" + e + "\" VARCHAR, \n"
print(group_members)

installed_product = ""
for e in dict.get("SVMXC__Installed_Product__c"):
    installed_product += "\"" + e + "\" VARCHAR, \n"
print(installed_product)