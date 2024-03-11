import json
import requests
from langchain_core.tools import tool

# nathan.ma@verify.com / Svmx1243

@tool
def schedule_management_tool(question) -> str:
    """API for Schedule Management pass the entire user input"""
    url = "https://aig-int.servicemax-api.com/v1/chat/completions"
    request_body = """
    {
        "user_message": {
            "talker_id": "1",
            "role": "user",
            "message": "%s",
            "timestamp": "2023-09-28T17:23:55Z"
        },
        "conversation": [],
        "context": {
            "conversation_id": 1,
            "entity_name": ""
        }
    }        
    """ % question
    json_data = json.loads(request_body)
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Type": "Salesforce",
        "X-Auth-Origin": "Production",
        "Authorization": "Bearer 00D1U0000013dOX!ARYAQE0dFdIlvO3.NeqtT60L78BV92_qX9St_KMdRLFpGA12daysmmtGN3WhBf_B8HulH_63CndltZxMEPclFwopXJ6bzvpe",
    }
    response = requests.post(url,
                             headers=headers,
                             json=json_data,
                             verify=False
                             )
    answer = response.text
    print("**TOOL** Schedule Skills, Question = " + question + " Answer = " + answer)
    return answer
