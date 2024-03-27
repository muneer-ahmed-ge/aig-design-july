import os
import sqlite3
import httpx
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough


question = "Who was the last technician for WO-00000450 ?"
question = "The last field tech working on the machine was who?"
question = "How many work order exists ?"
question = "Who was the last technician for WO-00000450 ?"
question = "What are the Line Types for WO-00000450 ?"
question = "Find out WO-00000450 total Work Order Lines of Line Type = 'Labor' ?"

load_dotenv()
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_EMBEDDING_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_EMBEDDING_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
    openai_api_version="2023-07-01-preview",
)

persist_directory = "/Users/muahmed/MT/ai/aig-design-july/resources/metadata_collection"
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name="metadata_collection")

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
    meta = e[idx2 + len("Metadata: "): len(e)]
    dict.get(object).append(field+',,'+meta+',String,,,')

service_order = ""
for e in dict.get("SVMXC__Service_Order__c"):
    service_order += e + "\n"
print(f"SVMXC__Service_Order__c semantic fields = {service_order}")

service_order_line = ""
for e in dict.get("SVMXC__Service_Order_Line__c"):
    service_order_line += e + "\n"
print(f"SVMXC__Service_Order_Line__c semantic fields = {service_order_line}")

group_members = ""
for e in dict.get("SVMXC__Service_Group_Members__c"):
    group_members += e + "\n"
print(f"SVMXC__Service_Group_Members__c semantic fields = {group_members}")

installed_product = ""
for e in dict.get("SVMXC__Installed_Product__c"):
    installed_product += e + "\n"
print(f"SVMXC__Installed_Product__c semantic fields = {installed_product}")

def execute_query(query: str) -> dict:
    headers = {
        'Authorization': 'Bearer 00De0000005T6vw!AQIAQMUP9jC3Nr0BalOQjO5I8Y85ZpoCGWmCFH0VBbWXISMtndaCAjWlE3B1oMa6iBXhJh62oIFIcBYAXSKQ84oKe1DhZFqG'
    }
    response = httpx.get("https://mydomainsg--part2.sandbox.my.salesforce.com/services/data/v55.0/query/?q=" + query, headers=headers)
    response.raise_for_status()
    print(f"query-result = {str(response.json())}")
    return response.json()

_PROMPT_TEMPLATE = """
You are an agent designed to generate SOQL(Salesforce Object Query Language) queries.

Here are the list of objects SVMXC__Service_Order__c, SVMXC__Service_Order_Line__c, SVMXC__Service_Group_Members__c

The schema of SVMXC__Service_Order__c is described in CVS format.
Name,Label,Description,Type,Reference,RelationshipName
Id,Record ID,,String,,
Name,Work Order Number,,String,,
SVMXC__Group_Member__c,Technician,Name of the group member working on the service order. This does not imply that this member has the ownership of service order record,SVMXC__Service_Group_Members__c,SVMXC__Group_Member__r
SVMXC__Component__c,Component,,Serial number of the component for which the customer is seeking support. Is a lookup to an existing installed product record in ServiceMax,SVMXC__Installed_Product__c,SVMXC__Component__r
SVMXC__Top_Level__c,Component,,Serial number of the component for which the customer is seeking support. Is a lookup to an existing installed product record in ServiceMax,SVMXC__Installed_Product__c,SVMXC__Component__r
%s

The schema of SVMXC__Service_Order_Line__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Line Number,,String,,
SVMXC__Service_Order__c,Work Order,Service order number. Is a lookup to an existing service order in ServiceMax,SVMXC__Service_Order__c,SVMXC__Service_Order__r
%s

The schema of SVMXC__Service_Group_Members__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Member Name,,String,,
%s

The schema of SVMXC__Installed_Product__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Installed Product ID,,String,,
%s

Always use the RelationshipName to query related objects.

Return the result as a SOQL Query only with no other text.

{input}
""" % (service_order, service_order_line, group_members, installed_product)
print(f"Prompt with semantic fields = {_PROMPT_TEMPLATE}")

prompt = PromptTemplate(
    input_variables=[], template=_PROMPT_TEMPLATE
)

llm = AzureChatOpenAI(deployment_name="SMAX-AI-Dev-GPT4-32")

output_parser = StrOutputParser()

chain = (
    {"input": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

sql_query = chain.invoke({"input": question})
print("sql_query = " + sql_query)

response = execute_query(sql_query)
