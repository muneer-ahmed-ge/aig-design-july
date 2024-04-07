# https://python.langchain.com/docs/modules/agents/agent_types/openai_tools/

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import AzureChatOpenAI

from orchestration.tools import service_history, scheduling, knowledge, get_product_code, query_record_by_name

load_dotenv()

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")

tools = [service_history, scheduling, knowledge, get_product_code, query_record_by_name]

prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(tools=tools, llm=llm, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

context = "WO-00000450"
question = "How to fix this asset Xerox Printer"
question = "Can you schedule next preventative work order maintenance of this Asset"
question = "Can you tell me who has mostly worked on the Asset Xerox Printer"
question = "Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset Xerox Printer"

answer = agent_executor.invoke({"input": question},{"metadata": {"agent-type": "openai-tools-agent"}})

print("Question : " + answer['input'])
print("Answer   : " + answer['output'])
