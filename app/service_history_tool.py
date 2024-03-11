from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import tool
from langchain import hub

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-apim-us.azure-api.net",
                      api_key="66681daf47e14be3a1c3966d62d17b5a",
                      deployment_name="SMAX-AI-Dev-GPT4-32", openai_api_version="2023-07-01-preview")

db = SQLDatabase.from_uri("sqlite:///ai.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-tools-agent")

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, toolkit.get_tools(), prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=toolkit.get_tools(), verbose=True)

@tool
def service_history_tool(question) -> str:
    """API for Service History pass the entire user input"""

    result = agent_executor.invoke({"input": question})

    print("**TOOL** Service History, Question = " + question + " Answer = " + result['output'])

    return result['output']
