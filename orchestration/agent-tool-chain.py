# https://www.comet.com/site/blog/using-the-react-framework-in-langchain

from langchain import hub
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import AzureChatOpenAI

llm = AzureChatOpenAI(azure_endpoint="https://smax-ai-dev-apim-us.azure-api.net",
                      api_key="66681daf47e14be3a1c3966d62d17b5a",
                      deployment_name="SMAX-AI-Dev-GPT4-32", openai_api_version="2023-07-01-preview")


@tool
def query_record_by_name(record_name: str) -> str:
    """API for fetching the record given record name"""
    print("**tool query_record_by_name**, Input Record Name = " + record_name)
    return "{'tech' : 'tom'}"


@tool
def service_history(history_question: str) -> str:
    """API for Service History pass the entire user input"""
    print("**tool service_history** Service History Skills, Input Question = " + history_question)
    return ""


@tool
def scheduling(scheduling_question: str) -> str:
    """API for Schedule Management pass the entire user input"""
    print("**tool scheduling ** Scheduling Skills, Input Question = " + scheduling_question)
    return ""


@tool
def get_product_code(product_name: str) -> str:
    """API for fetching the product code give the product name"""
    print("**tool get_product_code**, Input Product Code = " + product_name)
    return "PR-007"


@tool
def knowledge(product_code: str) -> str:
    """API for Product Documentation provided Product Code, first fetch the product code and then come here"""
    print("**TOOL** knowledge, Input Product Code = " + product_code)
    return "Remove the jammed papers and restart the machine"


tools = [service_history, scheduling, knowledge, get_product_code, query_record_by_name]

prompt = hub.pull("hwchase17/react-chat")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

context = "WO-00000450"
question = "How to fix this asset Xerox Printer"
question = "Can you schedule next preventative work order maintenance of this Asset"
question = "Can you tell me who has mostly worked on the Asset Xerox Printer"
question = "Can you schedule work order WO-00000450 to the tech that has mostly worked on the Asset Xerox Printer"

answer = agent_executor.invoke(
    {
        "input": question,
        "chat_history": "",
    }
)
print("Question : " + answer['input'])
print("Answer   : " + answer['output'])
