from langchain_core.tools import tool


@tool
def query_record_by_name(record_name: str) -> str:
    """API for fetching the record given record name"""
    return input('Query Record Question > ' + record_name)


@tool
def service_history(question: str) -> str:
    """API for Service History"""
    return input('service_history > question = ' + question + ' > enter Answer >> ')


@tool
def scheduling(question: str) -> str:
    """API for Schedule Management"""
    return input('scheduling > question = ' + question + ' > enter Answer >> ')


@tool
def get_product_id(product_name: str) -> str:
    """API for fetching the product id give the product name"""
    return input('get_product_id > product_name = ' + product_name + ' > enter Answer >> ')


@tool
def knowledge(product_id: str) -> str:
    """API for Product Documentation provided Product id"""
    return input('knowledge > product_id = ' + product_id + ' > enter Answer >> ')
