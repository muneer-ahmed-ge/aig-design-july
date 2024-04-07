from langchain_core.tools import tool

@tool
def query_record_by_name(record_name: str) -> str:
    """API for fetching the record given record name"""
    print("**tool query_record_by_name**, Input Record Name = " + record_name)
    return "{'tech' : 'tom'}"


@tool
def service_history(history_question: str) -> str:
    """API for Service History pass the entire user input"""
    print("**tool service_history** Service History Skills, Input Question = " + history_question)
    return "Tom"


@tool
def scheduling(scheduling_question: str) -> str:
    """API for Schedule Management pass the entire user input"""
    print("**tool scheduling ** Scheduling Skills, Input Question = " + scheduling_question)
    return "Done"


@tool
def get_product_id(product_name: str) -> str:
    """API for fetching the product id give the product name"""
    print("**tool get_product_id**, Input Product Name = " + product_name)
    return "PR-007"


@tool
def knowledge(product_id: str) -> str:
    """API for Product Documentation provided Product id, first fetch the product id and then come here"""
    print("**TOOL** knowledge, Input Product Id = " + product_id)
    return "Remove the jammed papers and restart the machine"
