from langchain_core.tools import tool


# @tool
# def query_record_by_name(record_name: str) -> str:
#     """API for fetching the record given record name"""
#     return input('Query Record Question > ' + record_name + ' :  ')

@tool
def get_installed_product_id_by_work_order_name(work_order_name: str) -> str:
    """API for getting the installed product id for work order names eg: WO-00000450"""
    return input('Service History Question > ' + work_order_name + ' :  ')


@tool
def service_history(installed_product_id: str, history_question: str) -> str:
    """API for Service History provided the installed_product_id"""
    return input('Service History Question installed_product_id > ' + installed_product_id + ' > ' + history_question + ':  ')


@tool
def scheduling(scheduling_question: str) -> str:
    """API for Schedule Management pass the entire user input"""
    return input('Scheduling Skill Question > ' + scheduling_question + ' :  ')


@tool
def get_product_id(product_name: str) -> str:
    """API for fetching the product id give the product name"""
    return input('Get Product Id Question > ' + product_name + ' :  ')


@tool
def knowledge(product_id: str) -> str:
    """API for Product Documentation provided Product id"""
    return input('Knowledge Skill Question > ' + product_id + ' :  ')
