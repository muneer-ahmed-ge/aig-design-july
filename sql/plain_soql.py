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


load_dotenv()
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_EMBEDDING_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_EMBEDDING_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
    openai_api_version="2023-07-01-preview",
)

_PROMPT_TEMPLATE = """
You are an agent designed to generate SOQL(Salesforce Object Query Language) queries.

Here are the list of objects 
Object Name, Description
SVMXC__Installed_Product__c,Installed Products
SVMXC__Service_Order__c,Work Orders
SVMXC__Service_Order_Line__c,Work Details
SVMXC__Service_Group_Members__c,Technicians

The schema of SVMXC__Installed_Product__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Installed Product ID,,String,,
SVMXC__Product_Name__c,Product Name,Name of the product associated with the Installed Product,string
SVMXC__Date_Installed__c,Date Installed,Date on which the product was installed at the customer location,date
SVMXC__Serial_Lot_Number__c,Serial/Lot Number,Unique identification of this product. This information is Required if the product’s tracking is Serialized or Lot/Batch Tracked in the product record,string

The schema of SVMXC__Service_Order__c is described in CVS format.
Name,Label,Description,Type,Reference,RelationshipName
Id,Record ID,,String,,
Name,Work Order Number,,String,,
SVMXC__Purpose_of_Visit__c,Purpose of Visit,If the Order Type is Field Service, specific reason for the field visit,string,,
SVMXC__Problem_Description__c,Problem Description,Detailed description of the problem as reported by the customer,string,,
SVMXC__Root_Cause__c,Root Cause,Root cause of the failure,string,,
SVMXC__Scheduled_Date_Time__c,Scheduled Date Time,,datetime,,
SVMXC__Work_Performed__c,Work Performed,Details of work performed to address/resolve the service order,string,,
SVMXC__Symptom__c,Symptom,Symptom that was noted before the failure,string,,
SVMXC__Order_Status__c,Order Status, Current status of the service order,string,,
SVMXC__Group_Member__c,Technician,Name of the group member working on the service order. This does not imply that this member has the ownership of service order record,SVMXC__Service_Group_Members__c,SVMXC__Group_Member__r
SVMXC__Component__c,Component,,Serial number of the component for which the customer is seeking support. Is a lookup to an existing installed product record in ServiceMax,SVMXC__Installed_Product__c,SVMXC__Component__r
SVMXC__Top_Level__c,Component,,Serial number of the component for which the customer is seeking support. Is a lookup to an existing installed product record in ServiceMax,SVMXC__Installed_Product__c,SVMXC__Component__r

The schema of SVMXC__Service_Order_Line__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Line Number,,String,,
SVMXC__Service_Order__c,Work Order,Service order number. Is a lookup to an existing service order in ServiceMax,SVMXC__Service_Order__c,SVMXC__Service_Order__r
SVMXC__Activity_Type__c,Activity Type,Indicates the type of activity performed. Usually applicable for labor line types,string,,
SVMXC__Start_Date_and_Time__c,Start Date and Time,Start date and time if the line type is Labor,dateTime,,
SVMXC__End_Date_and_Time__c,End Date and Time,End date and time if the line type is Labor,dateTime,,
SVMXC__Group_Member__c,Technician,Name of the group member working on the service order. This does not imply that this member has the ownership of service order record,SVMXC__Service_Group_Members__c,SVMXC__Group_Member__r
SVMXC__Serial_Number__c,IB Serial Number,,,SVMXC__Installed_Product__c,SVMXC__Serial_Number__r
SVMXC__Actual_Quantity2__c,Line Qty,Number of units consumed. This is context-sensitive based on line type,string,,

The schema of SVMXC__Service_Group_Members__c is described in CVS format.
Name,Label,Description,Type
Id,Record ID,,String,Reference,RelationshipName
Name,Member Name,,String,,

Every SOQL query against SVMXC__Service_Order__c must include this filter SVMXC__Scheduled_Date_Time__c<=Today in its where clause.

Every SOQL query against SVMXC__Service_Order_Line__c must include this filter SVMXC__Line_Type__c = 'Parts' or SVMXC__Line_Type__c = 'Labor' in its where clause.

Every SOQL query against SVMXC__Installed_Product__c must include this filter Id = 'a0PDK000003H0Xj2AK'

When the question refers to this machine it means SVMXC__Installed_Product__c

When the question refers to most recent then add LIMIT 1

Always use the RelationshipName to query related objects.

Return the result as a SOQL Query only with no other text.

{input}
"""

def execute_query(query: str) -> dict:
    headers = {
        'Authorization': 'Bearer 00D0v0000009Vlf!AR4AQNgWpjBh18.I1DrOaKG.BB539Obuiz'
                         '.mcLO1M7TbuFHh9zhq6T24NWzAWMGo0E7p49zXfjvMhsgvVPA5XyzAlWb7lZwY'
    }
    response = httpx.get("https://d0v0000009vlfeae--part2.sandbox.my.salesforce.com/services/data/v55.0/query/?q="
                         + query, headers=headers)
    response.raise_for_status()
    # print(f"query-result = {str(response.json())}")
    return response.json()

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

question = "Summarize all the work orders in the last five years."

sql_query = chain.invoke({"input": question})
print("generated soql_query = " + sql_query)
sql_query = sql_query.replace('\n', ' ')
# print("executing soql_query = " + sql_query)
response = execute_query(sql_query)
output = str(response)
output = output.partition(output[-80:])
print(output[1])
