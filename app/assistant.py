# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant?source=recommendations

from langchain.agents import AgentExecutor
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

from app.knowledge_tool import knowledge_tool
from app.schedule_tool import schedule_management_tool
from app.service_history_tool import service_history_tool

tools = [service_history_tool, schedule_management_tool, knowledge_tool]

assistant = OpenAIAssistantRunnable.create_assistant(
    name="Service, Scheduling and Benefits Knowledge Base Copilot",
    instructions="You are a Service, Scheduling and Benefits Knowledge Base Copilot",
    tools=tools,
    model="gpt-4",
    as_agent=True
)

agent_executor = AgentExecutor(agent=assistant, tools=tools, verbose=True)

question = "What is the order type and turn around time for WO-00000450 and what is WO-00009920 schedule and " \
           "I have spent 4 years how much PTO will I get ?"
answer = agent_executor.invoke(
    {
        "content": question
    }
)
print("Question : " + answer['content'])
print("Answer   : " + answer['output'])

