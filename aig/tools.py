from langchain_core.tools import tool


# System Tools

@tool
def query_record_by_name(name: str) -> str:
    """API for searching records given name"""
    return input('query_record_by_name, name = ' + name + ' > enter answer : ')


@tool
def get_work_order_by_name(name: str) -> str:
    """API for getting the work order given name"""
    return input('get_work_order_by_name, name = ' + name + ' > enter answer : ')


@tool
def get_work_order_by_installed_product(name: str) -> str:
    """API for getting work order given installed product"""
    return input(
        'get_work_order_by_installed_product, name = ' + name + ' > enter answer : ')


@tool
def get_installed_product_by_work_order(name: str) -> str:
    """API for getting installed product given work order"""
    return input(
        'get_installed_product_by_work_order, name = ' + name + ' > enter answer : ')


@tool
def get_product_by_name(name: str) -> str:
    """API for getting product given name"""
    return input('get_product_by_name, name = ' + name + ' > enter Answer >> ')


# Service History Tools
@tool
def get_service_history_about_work_order(work_order: str, question: str) -> str:
    """API for getting Service History given the work order"""
    return input(
        'get_service_history_about_work_order, work_order = ' + work_order + ' question = '
        + question + ' > enter answer : ')


@tool
def get_service_history_about_installed_product(installed_product: str, question: str) -> str:
    """API for getting Service History given the installed product"""
    return input(
        'get_service_history_about_installed_product installed_product = ' + installed_product
        + ' question = ' + question + ' > enter answer : ')


# Schedule Management Tools
@tool
def get_schedule_management(question: str) -> str:
    """API for Schedule Management"""
    return input(
        'schedule_management schedule_management_question = ' + question + ' > enter answer : ')


# Knowledge Access Skills Tools

@tool
def get_knowledge_access(product: str) -> str:
    """API for Products Knowledge and help documentation give product"""
    return input('knowledge_access > product = ' + product + ' > enter Answer >> ')
