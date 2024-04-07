# Business: Conversational Agents to answer complex questions by calling external APIs
# Problem : Convert natural language into API calls
# Solution : OpenAI Function-Calling
# https://platform.openai.com/docs/guides/function-calling
# https://www.promptingguide.ai/applications/function_calling
# https://www.promptingguide.ai/techniques
# https://python.langchain.com/docs/modules/agents/agent_types/openai_tools

# Notes
# OpenAI termed the capability to invoke a single function as functions, and the capability to invoke one or more functions as tools.
# If you’re creating agents using OpenAI models, you should be using this OpenAI Tools agent rather than the OpenAI functions agent.
# Using tools allows the model to request that more than one function will be called upon when appropriate.
# In some situations, this can help significantly reduce the time that it takes an agent to achieve its goal.

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import AzureChatOpenAI

from orchestration.tools import service_history, scheduling, knowledge, get_product_id, query_record_by_name

load_dotenv()

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")

tools = [service_history, scheduling, knowledge, get_product_id, query_record_by_name]

prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

context = "WO-00000450"
question = "Can you schedule next preventative work order maintenance of this Asset"
question = "Can you tell me who has mostly worked on the Asset Xerox Printer"
question = "Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset Xerox Printer"
question = "How to fix this asset Xerox Printer"

answer = agent_executor.invoke({"input": question},{"metadata": {"agent-type": "openai-tools-agent"}})

print("Question : " + answer['input'])
print("Answer   : " + answer['output'])
