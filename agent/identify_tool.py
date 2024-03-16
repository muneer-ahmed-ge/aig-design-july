from langchain_core.tools import tool

@tool
def knowledge_tool(context) -> str:
    """API for Identifying the Context pass the entire user input"""
    print("**TOOL** Identify Tool is invoked with context = " + context)
    return context
