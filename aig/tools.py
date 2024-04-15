from langchain_core.tools import tool


# Service Tools
@tool
def get_service_history(question: str) -> str:
    """API for getting Service History"""
    return input('get_service_history, question = ' + question + ' > enter answer : ')


@tool
def get_schedule_management(question: str) -> str:
    """API for Schedule Management"""
    return input(
        'get_schedule_management question = ' + question + ' > enter answer : ')


@tool
def get_knowledge_access(question: str) -> str:
    """API for Knowledge and help documentation"""
    return input('get_knowledge_access > question = ' + question + ' > enter Answer >> ')


@tool
def get_service_history_for_work_order_id(work_order_id: str, question: str) -> str:
    """API for getting Service History about work order id which must start with must start with a2D and of length 15 digit a2De0000005gpjGEAQ"""
    payload = '''{"entity_resource": "SVMXC__Service_Order__c","entity": "%s"}''' % (work_order_id)
    return input('get_service_history_for_work_order, ' + payload + ' question = '
                 + question + ' > enter answer : ')


@tool
def get_service_history_for_installed_product_id(installed_product_id: str, question: str) -> str:
    """API for getting Service History about installed product id"""
    payload = '''{"entity_resource": "SVMXC__Installed_Product__c","entity": "%s"}''' % (installed_product_id)
    return input(
        'get_service_history_for_installed_product_id, ' + payload + ' question = ' + question + ' > enter answer : ')


@tool
def get_knowledge_access(product: str, question: str) -> str:
    """API for Knowledge and help documentation"""
    return input(
        'get_knowledge_access, product = ' + product
        + ' question = ' + question + ' > enter answer : ')


# System Tools

@tool
def query_records_by_name(name: str) -> str:
    """API for searching records given name"""
    return input('query_records_by_name, name = ' + name + ' > enter answer : ')


@tool
def get_work_order_id_by_name(work_order_name: str) -> str:
    """API for getting the work order id given work order name like WO-00000000"""
    return input('get_work_order_id_by_name, work_order_name = ' + work_order_name + ' > enter answer : ')


@tool
def get_work_order_for_installed_product(installed_product_name: str) -> str:
    """API for getting work order for installed product name eg: Ultrasound Logic series 2"""
    return input(
        'get_work_order_for_installed_product, installed_product_name = ' + installed_product_name + ' > enter answer : ')


@tool
def get_installed_product_for_work_order(work_order_name: str) -> str:
    """API for getting installed product given work order name like WO-00000000"""
    return input(
        'get_installed_product_for_work_order, work_order_name = ' + work_order_name + ' > enter answer : ')


@tool
def get_product_by_name(product_name: str) -> str:
    """API for getting product given product name"""
    return input('get_product_by_name, product_name = ' + product_name + ' > enter Answer >> ')