from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate

prompt_template = """
I want you to act as a expert who can answer questions related to Assets Services & Scheduling.
You posses a database of all Assets Service and Schedule related data.
The terms used in Assets Services & Scheduling includes Work Orders, Work Details, Jobs, Schedule etc. 
The work orders are referred with pattern like WO-00000001

But before answering any question you must ask User to first identify the context 
so to fetch right data from the database by asking a question What is the Context ?

{history} \n Human: {input}
"""

prompt = PromptTemplate(input_variables=["history", "input"], template=prompt_template)

chatQA = ConversationChain(
    prompt=prompt,
    llm=AzureChatOpenAI(deployment_name='SMAX-AI-Dev-GPT4'),
    verbose=False,
    memory=ConversationBufferMemory()
)
 # WO-00000450
chat_history = []
question = ""
while question != 'done':
    if question != exit:
        response = chatQA.predict(history=chat_history, input = question)
        print("Answer   = " + response)
        chat_history.append({'User': question, 'Assistant' : response})
        question = input('Question: ')
