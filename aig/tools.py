from langchain_core.tools import tool

# Common Tools
@tool
def query_record_by_name(record_name: str) -> str:
    """API for searching records given record name"""
    return input('query_record_by_name record_name = ' + record_name + ' > enter answer : ')


@tool
def get_work_order_id_by_work_order_name(work_order_name: str) -> str:
    """API for getting the work order record id given work order name"""
    return input('get_work_order_id_by_work_order_name work_order_name = ' + work_order_name + ' > enter answer : ')


@tool
def get_installed_product_id_by_work_order_name(work_order_name: str) -> str:
    """API for getting the installed product record id given work order name"""
    return input(
        'get_installed_product_id_by_work_order_name work_order_name = ' + work_order_name + ' > enter answer : ')


@tool
def get_work_orders_by_installed_product_id(installed_product_id: str) -> str:
    """API for getting the work order ids given installed product id"""
    return input(
        'get_work_orders_by_installed_product_id installed_product_id = ' + installed_product_id + ' > enter answer : ')


@tool
def get_product_id_by_product_name(product_name: str) -> str:
    """API for getting the product id give the product name"""
    return input('get_product_id_by_product_name > product_name = ' + product_name + ' > enter Answer >> ')


# Service History Tools
@tool
def get_service_history_about_work_order_id(work_order_id: str, question: str) -> str:
    """API for getting Service History given the work order id"""
    return input(
        'get_service_history_about_work_order_id work_order_id = ' + work_order_id + ' question = '
        + question + ' > enter answer : ')


@tool
def get_service_history_about_installed_product_id(installed_product_id: str, question: str) -> str:
    """API for getting Service History given the installed product id"""
    return input(
        'get_service_history_about_installed_product_id installed_product_id = ' + installed_product_id
        + ' question = ' + question + ' > enter answer : ')


# Schedule Management Tools
@tool
def schedule_management(schedule_management_question: str) -> str:
    """API for Schedule Management"""
    return input(
        'schedule_management schedule_management_question = '
        + schedule_management_question + ' > enter answer : ')


# Knowledge Access Skills Tools

@tool
def knowledge_access(product_id: str) -> str:
    """API for Products Knowledge and help documentation give product id"""
    return input('knowledge_access > product_id = ' + product_id + ' > enter Answer >> ')
