from langchain_core.tools import tool


@tool
def get_work_order_id_by_name(work_order_name: str) -> str:
    """API for getting the work order id given work order name like WO-00000000"""
    payload = '''{"tool_name":"get_work_order_id_by_name","parameters":{"work_order_name":"%s"}}''' % (work_order_name)
    return input(payload + ' > enter answer : ')


@tool
def get_work_order_for_installed_product(installed_product_name: str) -> str:
    """API for getting work order for installed product name eg: Ultrasound Logic series 2"""
    payload = '''{"tool_name":"get_work_order_for_installed_product","parameters":{"installed_product_name":"%s"}}''' % (
        installed_product_name)
    return input(payload + ' > enter answer : ')


@tool
def get_installed_product_for_work_order_id(work_order_name: str) -> str:
    """API for getting installed product id given work order name like WO-00000000"""
    payload = '''{"tool_name":"get_installed_product_for_work_order_id","parameters":{"work_order_name":"%s"}}''' % (
        work_order_name)
    return input(payload + ' > enter answer : ')


@tool
def get_product_id_for_installed_product_id(installed_product_id: str) -> str:
    """API for getting product id given installed product id"""
    payload = '''{"tool_name":"get_product_id_for_installed_product_id","parameters":{"installed_product_id":"%s"}}''' % (
        installed_product_id)
    return input(payload + ' > enter answer : ')


@tool
def get_service_history_for_work_order_id(work_order_id: str, question: str) -> str:
    """API for getting Service History about work order id which must start with must start with a2D and of length 15 digit a2De0000005gpjGEAQ"""
    payload = '''{"tool_name":"get_service_history_for_work_order_id","parameters":{"work_order_id":"%s", question":"%s"}}''' % (
        work_order_id, question)
    return input(payload + ' > enter answer : ')


@tool
def get_service_history_for_installed_product_id(installed_product_id: str, question: str) -> str:
    """API for getting Service History about installed product id"""
    payload = '''{"tool_name":"get_service_history_for_installed_product_id","parameters":{"installed_product_id":"%s", question":"%s"}}''' % (
        installed_product_id, question)
    return input(payload + ' > enter answer : ')


@tool
def query_records_by_name(name: str) -> str:
    """API for searching records given name"""
    payload = '''{"tool_name":"query_records_by_name","parameters":{"name":"%s"}}''' % (name)
    return input(payload + ' > enter answer : ')


@tool
def get_product_id_by_name(product_name: str) -> str:
    """API for getting product id given product name"""
    payload = '''{"tool_name":"get_product_id_by_name","parameters":{"product_name":"%s"}}''' % (
        product_name)
    return input(payload + ' > enter answer : ')


@tool
def get_knowledge_access(product_id: str, question: str) -> str:
    """API for Knowledge and help documentation"""
    payload = '''knowledge access endpoint {"user_message":{"role":"user","message":"%s"},"context":{"entity":"%s","entity_resource":"Product2"}}''' % (
        question, product_id)
    return input(payload + ' > enter answer : ')


@tool
def schedule_management(question: str) -> str:
    """API for Schedule Management"""
    payload = '''schedule_management endpoint {"user_message":{"role":"user","message":"%s"}}''' % (question)
    return input(payload + ' > enter answer : ')


