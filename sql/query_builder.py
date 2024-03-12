import os
from langchain.chains import create_sql_query_chain
from langchain.sql_database import SQLDatabase
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv

question = "Who was the last technician for WO-00000450 ?"
question = "What is the most common Line Type of Work Order Line"
question = "Who was the last technician for WO-00000450 ?"
question = "What are the Line Types for WO-00000450 ?"
question = "How many work order exists ?"
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
    dict.get(object).append(field)

service_order = ""
for e in dict.get("SVMXC__Service_Order__c"):
    service_order += "\"" + e + "\" VARCHAR, \n"
# print(service_order)

service_order_line = ""
for e in dict.get("SVMXC__Service_Order_Line__c"):
    service_order_line += "\"" + e + "\" VARCHAR, \n"
# print(service_order_line)

group_members = ""
for e in dict.get("SVMXC__Service_Group_Members__c"):
    group_members += "\"" + e + "\" VARCHAR, \n"
# print(group_members)

installed_product = ""
for e in dict.get("SVMXC__Installed_Product__c"):
    installed_product += "\"" + e + "\" VARCHAR, \n"
# print(installed_product)

_PROMPT_TEMPLATE = """
You are an agent designed to interact with a SQLLite database.

You must follow these instructions strictly :
1. Don't use the tools sql_db_list_tables and sql_db_schema
2. Use this information when you have to use sql_db_list_tables
    Action: sql_db_list_tables
    Action Input: 
    Observation: 
        SVMXC__Service_Order__c, SVMXC__Service_Order_Line__c, SVMXC__Service_Group_Members__c
3. Use this information when you have to use sql_db_schema
    Action: sql_db_schema
    Action Input: SVMXC__Service_Order__c, SVMXC__Service_Order_Line__c, SVMXC__Service_Group_Members__c
    Observation: 
        CREATE TABLE "SVMXC__Service_Order__c" (
            "Id" VARCHAR UNIQUE,        
            "Name" VARCHAR,
            "SVMXC__Group_Member__c" VARCHAR,
            %s
        )
        CREATE TABLE "SVMXC__Service_Order_Line__c" (
            "Id" VARCHAR UNIQUE,        
            "Name" VARCHAR,
            "SVMXC__Group_Member__c" VARCHAR,
            %s
        )
        CREATE TABLE "SVMXC__Service_Group_Members__c" (
            "Id" VARCHAR UNIQUE,
            "Name" VARCHAR,
            %s
        )
        CREATE TABLE "SVMXC__Installed_Product__c" (
            "Id" VARCHAR UNIQUE,
            "Name" VARCHAR,
            %s
        )
4. The SVMXC__Service_Order__c table contains data referred to as Work Order or Job
5. The SVMXC__Service_Order_Line__c table contains data referred to as Work Order Details or Details Lines
6. The SVMXC__Group_Member__c refers to technician lookup to SVMXC__Service_Group_Members__c column Id
7. If User question input contains something like this WO-00000001 then it refers to a record in 
SVMXC__Service_Order__c where Name = 'WO-00000001'
8. If User is asking anything from SVMXC__Service_Order_Line__c table with context in the format WO-00000001 then 
you can join the SVMXC__Service_Order_Line__c column SVMXC__Service_Order__c with SVMXC__Service_Order__c column Id 
and filter SVMXC__Service_Order__c using column Name = 'WO-00000001'

Never query for all the columns from a specific table, only ask for the relevant columns given the question.

You have access to tools for interacting with the database.

Only use the below tools. Only use the information returned by the below tools to construct your final answer. You 
MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and 
try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

{input}
""" % (service_order, service_order_line, group_members, installed_product)

db = SQLDatabase.from_uri("sqlite:////Users/muahmed/MT/ai/aig-design-july/resources/sample.db")

PROMPT = PromptTemplate(
    input_variables=[], template=_PROMPT_TEMPLATE
)

llm = AzureChatOpenAI(deployment_name="SMAX-AI-Dev-GPT4-32")

chain = create_sql_query_chain(llm, db, prompt=PROMPT)

sql_query = chain.invoke({"question": question})

print(sql_query)