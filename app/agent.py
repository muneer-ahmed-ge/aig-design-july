from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import AzureChatOpenAI

from app.knowledge_tool import knowledge_tool
from app.schedule_tool import schedule_management_tool
from app.service_history_tool import service_history_tool

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-apim-us.azure-api.net",
                      api_key="66681daf47e14be3a1c3966d62d17b5a",
                      deployment_name="SMAX-AI-Dev-GPT4-32", openai_api_version="2023-07-01-preview")

tools = [service_history_tool, schedule_management_tool, knowledge_tool]

prompt = hub.pull("hwchase17/react-chat")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

question = "What is the order type and turn around time for WO-00000450 and what is WO-00009920 schedule and " \
           "I have spent 4 years how much PTO will I get ?"

answer = agent_executor.invoke(
    {
        "input": question,
        "chat_history": "",
    }
)
print("Question : " + answer['input'])
print("Answer   : " + answer['output'])

