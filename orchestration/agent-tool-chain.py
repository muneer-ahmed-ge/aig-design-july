from langchain import hub
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import AzureChatOpenAI

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-apim-us.azure-api.net",
                      api_key="66681daf47e14be3a1c3966d62d17b5a",
                      deployment_name="SMAX-AI-Dev-GPT4-32", openai_api_version="2023-07-01-preview")


@tool
def service_history(question) -> str:
    """API for Service History pass the entire user input"""
    print("**TOOL** Service History Skills, Question = " + question)
    return ""


@tool
def scheduling(question) -> str:
    """API for Schedule Management pass the entire user input"""
    print("**TOOL** Scheduling Skills, Question = " + question)
    return ""


@tool
def knowledge(question) -> str:
    """API for Benefits Documentation pass the entire user input"""
    print("**TOOL** Knowledge Skills, Question = " + question)
    return ""


tools = [service_history, scheduling, knowledge]

prompt = hub.pull("hwchase17/react-chat")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

question = "Can you schedule next preventative work order maintenance of this Asset"
question = "Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset "

answer = agent_executor.invoke(
    {
        "input": question,
        "chat_history": "",
    }
)
print("Question : " + answer['input'])
print("Answer   : " + answer['output'])
