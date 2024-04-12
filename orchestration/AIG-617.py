from langchain import hub
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key="",
                      deployment_name="SMAX-AI-Dev-GPT4-0125",
                      openai_api_version="2024-02-15-preview")

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

@tool
def getIPByWO(work_order_name: str) -> str:
    """API for getting the installed product for work order"""
    return input('Service History Question (getIPByWO) > ' + work_order_name + ' :  ')

@tool
def getWOByIP(installed_product_id: str) -> str:
    """API for getting the work orders for installed product"""
    return input('Service History Question (getWOByIP) > ' + installed_product_id + ' :  ')

@tool
def getServiceHistoryAboutWO(work_order: str, history_question: str) -> str:
    """API for Service History for the work_order"""
    return input('Service History Question (getServiceHistoryAboutWO) work_order > ' + work_order + ' > ' + history_question + ':  ')

@tool
def getServiceHistoryAboutIP(installed_product: str, history_question: str) -> str:
    """API for Service History for the installed_product"""
    return input('Service History Question (getServiceHistoryAboutIP) installed_product > ' + installed_product + ' > ' + history_question + ':  ')


tools = [getIPByWO, getWOByIP, getServiceHistoryAboutWO, getServiceHistoryAboutIP]

agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

question = "List all the work order for asset of WO-12345 ?"
# question = "What is the installed date of installed product A-1234 ?"
chat_history = []
user_input = question
while user_input != 'exit':
    if user_input != 'exit':
        response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
        print("Question = " + response['input'])
        print("Answer = " + response['output'])
        chat_history.append(HumanMessage(content=response['input']))
        chat_history.append(AIMessage(content=response['output']))
        user_input = input('Question > ')