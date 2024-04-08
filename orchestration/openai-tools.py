# Business: Conversational Agents to answer complex questions by calling external APIs
# Problem : Convert natural language into API calls
# Solution : OpenAI Function-Calling
# https://platform.openai.com/docs/guides/function-calling
# https://www.promptingguide.ai/applications/function_calling
# https://www.promptingguide.ai/techniques
# https://python.langchain.com/docs/modules/agents/agent_types/openai_tools
# https://www.promptingguide.ai/research/llm-agents

# Notes
# OpenAI termed the capability to invoke a single function as functions, and the capability to invoke one or more functions as tools.
# If you’re creating agents using OpenAI models, you should be using this OpenAI Tools agent rather than the OpenAI functions agent.
# Using tools allows the model to request that more than one function will be called upon when appropriate.
# In some situations, this can help significantly reduce the time that it takes an agent to achieve its goal.

# OpenAI Functions vs reAct
# https://www.reddit.com/r/LangChain/comments/178lhnc/openai_functions_vs_langchain_react_agents/

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from orchestration.tools import service_history, scheduling, knowledge, get_product_id, query_record_by_name

load_dotenv()
llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")

PROMPT_PREFIX = (
    "You are an AI system designed to select tools to answer from user's question. You task is:\n"
    "- to answer questions about the service history of an Installed Product (a machine or piece of equipment)."
    "The service history records consist of Work Orders, Work Details, Installed Products, and assigned technicians etc,"
    " which can help a field technician for trouble-shooting based on the past records related to an asset. "
    "A Work Order or a Job is created on issues related to an Installed Product."
    "A technician named {user_name} is chatting with you. This technician was initially querying information about {context_entity_label} of ID {context_entity}"
    "Let's think step by step.")
prefix = (PROMPT_PREFIX.format(
    user_name="Tom",
    context_entity_label="Work Order",
    context_entity="WO-0000450"))
prompt = hub.pull("hwchase17/openai-tools-agent")
system_prompt = prompt.messages[0]
system_prompt.prompt.template = prefix + "\n\n" + system_prompt.prompt.template

tools = [service_history, scheduling, knowledge, get_product_id, query_record_by_name]

agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

context = "WO-00000450"
question = "Can you schedule next preventative work order maintenance of this Asset"
question = "Can you tell me who has mostly worked on the Asset Xerox Printer"
question = "Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset Xerox Printer"
question = "How to fix this asset Xerox Printer"

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
