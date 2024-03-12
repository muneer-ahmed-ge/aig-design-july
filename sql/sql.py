# https://python.langchain.com/docs/integrations/toolkits/sql_database
# Good Article
# https://medium.com/@lucnguyen_61589/revolutionize-your-data-exploration-unveiling-the-power-of-langchain-bd9f18d97532

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_community.chat_models import AzureChatOpenAI

db = SQLDatabase.from_uri("sqlite:////Users/muahmed/MT/ai/aig-design-july/resources/sample.db")

chat = AzureChatOpenAI(deployment_name="SMAX-AI-Dev-GPT4-32")

toolkit = SQLDatabaseToolkit(db=db, llm=chat)

# Define prompt
prefix = """
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
            "Name" VARCHAR,
            "SVMXC__Group_Member__c" VARCHAR,
            UNIQUE ("Id")
        )
        CREATE TABLE "SVMXC__Service_Order_Line__c" (
            "SVMXC__Service_Order__c" VARCHAR,
            "SVMXC__Line_Status__c" VARCHAR, 
            "SVMXC__Line_Type__c" VARCHAR 
        )
        CREATE TABLE "SVMXC__Service_Group_Members__c" (
            "Id" VARCHAR UNIQUE,
            "Name" VARCHAR
        )
4. The SVMXC__Service_Order__c table contains data referred to as Work Order or Job
5. The SVMXC__Service_Order_Line__c table contains data referred to as Work Order Details or Details Lines
6. The SVMXC__Group_Member__c refers to technician lookup to SVMXC__Service_Group_Members__c column Id
7. If User question input contains something like this WO-00000001 then it refers to a record in 
SVMXC__Service_Order__c where Name = 'WO-00000001'
8. If User is asking anything from SVMXC__Service_Order_Line__c table with context in the format WO-00000001 then 
you can join the SVMXC__Service_Order_Line__c column SVMXC__Service_Order__c with SVMXC__Service_Order__c column Id 
and filter SVMXC__Service_Order__c using column Name = 'WO-00000001'

Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 20 results

Never query for all the columns from a specific table, only ask for the relevant columns given the question.

You have access to tools for interacting with the database.

Only use the below tools. Only use the information returned by the below tools to construct your final answer. You 
MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and 
try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
"""

agent_executor = create_sql_agent(
    llm=chat,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prefix=prefix
)

question = "Find out WO-00000450 total Work Order Lines of Line Type = 'Labor' ?"
question = "What are the Line Types for WO-00000450 ?"
question = "Who was the last technician for WO-00000450 ?"
question = "What is the most common Line Type of Work Order Line"
question = "How many work order exists ?"

agent_executor.invoke({'input': question})