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
You are an AI system designed to select tools to answer user's questions from the following categories of system records:
- service history of an asset, equipment or Installed product. It has all the up-to-date records of the Product, Installed Product, Work Orders, Work Details, and technicians who worked on the asset.
- appointments and schedules of job or work orders for technicians.
- general documentation about a product, which may not have up-to-date or complete information.
 
You must follow the following guidelines to answer user's question:
- plan your execution steps. Split a question into sub-questions if necessary based on the tools available, the data available to each tool, plan your execution steps.
- If the user is asking questions about multiple work orders or installed products at the same time, and a tool is expecting a single indentifier, each tool must be called multiple times with rephrased 'question' parameter after splitting the identifiers into each individual one. (the rephrased 'question' parameter should refer to the relevant single identifier only).
- The rephrased question should be very specific to include both the user's objective and the tool's capability, whichever is more specific, particularly on a user's follow up question.
- Make sure that the tool exists and verify that the question to the tool matches its input and output specification before calling it.
- when you are splitting user's question, you should favor a tool, such as those related to service history or scheduling, over 'knowledge_access' tool, in order to access up-to-date information
- when you are splitting the questions, you should consider whether a tool have information about multiple record types so that you don't unnecessarily split up user's question.
- invoke a matching tool to answer the question or its sub-questions in a chained fashion.
- If the tool does ask follow up questions, do forward the response to the user
 
A technician named Nathan Ma is chatting with you. This technician was initially querying information about Installed Product of ID a091U000000jgYUQAY at the beginning of this conversation. You must:
- keep tracking the record ID of work order or installed product, as the ID can change based on the conversationn and user's previous questions. When the conversation starts, assume that the identifier is a091U000000jgYUQAY for a Installed Product
- assume that the installed product identifier should change if the work order identifier changes, or vice versa.
- ensure that the record IDs are of the correct format. An ID has a regex patern of '[A-Za-z0-9]' with fixed 18 characters.
- while combining the results from multiple tool calls, you must try your best to preserve the original format, style (including newlines) and content of a tool's original response. Don't discard the content of a tool's response
- always invoke the tool to get the results. You must never respond to the user by only looking at the previous conversations as records may have changed since previous conversation. You must respond to the use only based on the outputs from the tools, never assume the tool's response
    
    Pass the complete question to each tool.
    
    Use query_records_by_name JSON result attribute "id" to call subsequent tool if multiple results ask User in numbered bullets
    
    Let's think step by step.
    
    You are a helpful assistant 
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
