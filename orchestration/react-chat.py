# Business: Conversational Agents to answer complex questions by calling external APIs
# Problem : Convert natural language into API calls
# Solution : reAct
# https://www.promptingguide.ai/techniques/react
# https://python.langchain.com/docs/modules/agents/agent_types/react/
# https://www.comet.com/site/blog/using-the-react-framework-in-langchain/
# https://medium.com/@jainashish.079/build-llm-agent-combining-reasoning-and-action-react-framework-using-langchain-379a89a7e881
# https://www.youtube.com/watch?v=Eug2clsLtFs

# OpenAI Functions vs reAct
# https://www.reddit.com/r/LangChain/comments/178lhnc/openai_functions_vs_langchain_react_agents/

import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import AzureChatOpenAI
from orchestration.tools import service_history, scheduling, knowledge, get_product_id, query_record_by_name

load_dotenv()

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-eastus.openai.azure.com",
                      api_key=os.getenv("AZURE_OPENAI_0125_API_KEY"),
                      deployment_name="SMAX-AI-Dev-GPT4-0125", openai_api_version="2024-02-15-preview")

tools = [service_history, scheduling, knowledge, get_product_id, query_record_by_name]
prompt = hub.pull("hwchase17/react-chat")
agent = create_react_agent(llm, tools, prompt)
# print(prompt.template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# https://servicemax.atlassian.net/wiki/spaces/PROD/pages/3951984679/Copilot+Chat+Examples
question = "What’s on my calendar today ?"

# What’s on my calendar today ?
# Appointment: [WO-00000155] Princess Margaret Hospital on April 10, 2024 2pm and Appointment: [WO-00008627] United Oil & Gas Corp on April 10, 2024 at 4pm
#
# Who was was the last tech for first appointment and when is its next appointment and how to fix first appointment's red light flashing ?
# Last Tech : John Doe
# Next Appointment : April 12, 2024
# Fix Red light : Restart the machine

answer = agent_executor.invoke({"input": question,"chat_history": ""},{"metadata": {"agent-type": "react-chat"}})

print("Question : " + answer['input'])
print("Answer   : " + answer['output'])
