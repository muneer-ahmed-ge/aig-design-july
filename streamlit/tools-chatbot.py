import random

import requests
import streamlit as st

# run the chatbot
# /Users/muahmed/MT/ai/aig-design-july/venv/bin/python -m streamlit run /Users/muahmed/MT/ai/aig-design-july/streamlit/tools-chatbot.py

# https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
# requirements.txt: requests streamlit
# Demo Org
# david.lambert@5544trial.com / Service1

# Nathan Org
# nathan.ma@verify.com / Svmx1243

TOKEN = "00DHo000001ZYE2!AQsAQMxrZk1xljr2DAXZqN3usip8CqBtKdwaz3DiQFE1_JimSBBeJ1GfdbZ6WgaP5a2TEYRV9eTzrhuX.3Jp4kLTSNP5Nsdl"

with st.sidebar:
    work_order = st.text_input("Work Order ID", key="work_order", value="a1gHo0000027UAnIAM")
    installed_product = st.text_input("Installed Product ID", key="installed_product", value="")
    org_type = st.text_input("Org Type", key="org_type", value="Production")
    access_token = st.text_input("Access Token", key="access_token", value=TOKEN)
    aig_url = st.text_input("AIG URL", key="aig_url", value="http://localhost:8000/v1/agent")

st.title("💬 Chatbot")

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []
    st.session_state["conversation_id"] = random.randint(1, 2_000_000_000)

for msg in st.session_state["conversation"]:
    st.chat_message(msg["role"]).write(msg["message"])

user_message = {
    "talker_id": "me",
    "role": "user",
    "timestamp": "2024-03-15T11:00:00"
}

if user_question := st.chat_input():
    if not access_token:
        st.info("missing access token")
        st.stop()
    # if not work_order and not installed_product:
    #     st.info("missing entity")
    #     st.stop()

    st.session_state["conversation"].append({
        "talker_id": "me",
        "role": "user",
        "message": user_question,
        "timestamp": "2024-03-15T11:00:00"
    })
    user_message["message"] = user_question
    st.chat_message("user").write(user_question)

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'X-Auth-Origin': org_type,
        'X-Auth-Type': 'salesforce',
        'x-conversation-id': str(st.session_state["conversation_id"]),
        'from': 'SvmxPtc@4450'
    }
    body = {
        "user_message": user_message,
        "conversation": st.session_state.conversation,
        "context": {
            "entity": work_order or installed_product,
            "entity_resource": "SVMXC__Service_Order__c" if work_order else "SVMXC__Installed_Product__c",
            "conversation_id": st.session_state["conversation_id"]
        }
    }
    response = requests.post(aig_url, headers=headers, json=body, timeout=300)
    if response.status_code != 200:
        st.info(f"error response: {response.text}")
    else:
        response_message = response.json()["message"]
        st.session_state["conversation"].append({
            "talker_id": "ai",
            "role": "ai",
            "message": response_message,
            "timestamp": "2024-03-15T11:00:00"
        })

        st.chat_message("ai").write(response_message)
