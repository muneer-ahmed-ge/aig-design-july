# Goal : https://servicemax.atlassian.net/wiki/spaces/PROD/pages/3951984679/Copilot+Chat+Examples
# Subject Identification : https://servicemax.atlassian.net/browse/AIG-519
# Service History Tools : https://servicemax.atlassian.net/browse/AIG-617

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from aig.tools import query_record_by_name, get_work_order_id_by_work_order_name, \
    get_installed_product_id_by_work_order_name, get_work_orders_by_installed_product_id, \
    get_product_id_by_product_name, get_service_history_about_work_order_id , \
    get_service_history_about_installed_product_id, schedule_management, knowledge_access

load_dotenv()
llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")
PROMPT_PREFIX = """
    You are an AI system designed to manage Field Service Assets like equipments installed at a location.
    Technicians interact with you enquiring about Asset Service History its schedule and will ask help for 
    trouble-shooting issues with Assets.
    You are provided with a set of tools to get Asset Service History and Scheduling and Help information.
    Select appropriate tools based on your question's intent.

    A technician named {user_name} is chatting with you now.

    The Asset Service history records consist of Work Orders, Work Details, Installed Products, and assigned technicians

    Let's think step by step.   
"""

prefix = (PROMPT_PREFIX.format(user_name="Tom"))
prompt = hub.pull("hwchase17/openai-tools-agent")
system_prompt = prompt.messages[0]
system_prompt.prompt.template = prefix + "\n\n" + system_prompt.prompt.template

tools = [query_record_by_name, get_work_order_id_by_work_order_name, get_installed_product_id_by_work_order_name,
         get_work_orders_by_installed_product_id, get_product_id_by_product_name, get_service_history_about_work_order_id ,
         get_service_history_about_installed_product_id, schedule_management, knowledge_access]


agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

"""
Simple Questions
----------------
Question : What is the scheduled end date of work order WO-12345 ?
Answer: 

Composite Questions
-------------------
Conversation # 1
Question : What’s on my calendar today ?
Answer : Appointment: [WO-00000155] Princess Margaret Hospital on April 10, 2024 2pm and Appointment: [WO-00008627] United Oil & Gas Corp on April 10, 2024 at 4pm
Question : Who was was the last tech for first appointment and how to fix first appointment's red light flashing ?
    Question : 
    Answer : John Doe
    Question : 
    Answer : April 12, 2024
    Question : 
    Answer : Restart the machine 
Answer :  Aggregated Answer

Conversation # 2
Question : Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset Xerox Printer ?
"""
# woQ4O000003R29MUAS
# ipg1U000000xYk8QAE
# poHo0000027ToWIAU
# You have a 9:00 AM job at Good Samaritan Hospital WO-12345, a 12:30 PM job at Valley Medical Center, and WO-000789 3:00 PM job at Northridge Health Associates.
# Sure thing. I found several potential times for the job. Please select one of the options (1) February 22nd, 2024 at 9:00 AM (2) February 24th, 2024 at 2:00 PM
question = "what was the scheduled date of work order WO-12345 ?"
question = "What’s on my calendar today?"

chat_history = []
user_input = input('Question > ')
while user_input != 'exit':
    response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    # print("Question = " + response['input'])
    print("Answer = " + response['output'])
    chat_history.append(HumanMessage(content=response['input']))
    chat_history.append(AIMessage(content=response['output']))
    user_input = input('Question > ')
