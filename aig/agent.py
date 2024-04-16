# Goal :https://servicemax.atlassian.net/wiki/spaces/AE/pages/3968860163/Agent+Tools
# Reference : https://servicemax.atlassian.net/wiki/spaces/PROD/pages/3951984679/Copilot+Chat+Examples
# Subject Identification : https://servicemax.atlassian.net/browse/AIG-519
# Service History Tools : https://servicemax.atlassian.net/browse/AIG-617

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from aig.tools import get_work_order_id_by_name, get_work_order_for_installed_product, \
    get_installed_product_for_work_order_id, get_product_id_for_installed_product_id, \
    get_service_history_for_work_order_id, get_service_history_for_installed_product_id, query_records_by_name, \
    get_product_id_by_name, get_knowledge_access, schedule_management

load_dotenv()
llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")
PROMPT_PREFIX = """
    You are an AI system designed to manage Field Service Assets like equipments installed at a location.
    Technicians interact with you enquiring about Asset Service History, their schedule and will ask help for 
    trouble-shooting issues with Assets.
    You are provided with a set of tools to get Asset Service History and Scheduling and Help information.
    Select appropriate tools based on your question's intent.

    A technician named {user_name} is chatting with you now.

    The Asset Service history records consist of Work Orders, Work Details, Installed Products, and assigned technicians
    
    Pass the complete question to each tool.
    
    Use query_records_by_name JSON result attribute "id" to call subsequent tool if multiple results ask User in numbered bullets
    
    Let's think step by step.
"""

prefix = (PROMPT_PREFIX.format(user_name="Tom"))
prompt = hub.pull("hwchase17/openai-tools-agent")
system_prompt = prompt.messages[0]
system_prompt.prompt.template = prefix + "\n\n" + system_prompt.prompt.template

tools = [
    get_work_order_id_by_name, get_work_order_for_installed_product,
    get_installed_product_for_work_order_id, get_product_id_for_installed_product_id,
    get_service_history_for_work_order_id, get_service_history_for_installed_product_id,
    query_records_by_name, get_product_id_by_name, get_knowledge_access, schedule_management
]

agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, stream_runnable=False)

question = ""
chat_history = []
user_input = input('Question > ')
while user_input != 'exit':
    response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    print("Answer = " + response['output'])
    chat_history.append(HumanMessage(content=response['input']))
    chat_history.append(AIMessage(content=response['output']))
    user_input = input('Question > ')
