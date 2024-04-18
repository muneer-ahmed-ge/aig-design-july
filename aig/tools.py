from langchain_core.tools import tool


@tool
def get_work_order_id_by_name(work_order_name: str) -> str:
    """API for getting the work order id given work order name like WO-00000000"""
    return print_tool("get_work_order_id_by_name", "work_order_name", work_order_name)


@tool
def get_installed_product_id_by_name(installed_product_name: str) -> str:
    """API for getting work order for installed product name eg: Ultrasound Logic series 2"""
    return print_tool("get_installed_product_id_by_name", "installed_product_name", installed_product_name)


@tool
def get_work_order_ids_for_installed_product_id(installed_product_id: str) -> str:
    """API for getting work order ids for installed product id"""
    return print_tool("get_work_order_ids_for_installed_product_id", "installed_product_id", installed_product_id)


@tool
def get_installed_product_id_for_work_order_id(work_order_id: str) -> str:
    """API for getting installed product id given work order id"""
    return print_tool("get_installed_product_id_for_work_order_id", "work_order_id", work_order_id)


@tool
def get_product_id_for_installed_product_id(installed_product_id: str) -> str:
    """API for getting product id given installed product id"""
    return print_tool("get_product_id_for_installed_product_id", "installed_product_id", installed_product_id)


@tool
def get_service_history_for_work_order_id(work_order_id: str, question: str) -> str:
    """API for getting Service History given work order id"""
    return print_tool("get_service_history_for_work_order_id", "work_order_id", work_order_id, question)


@tool
def get_service_history_for_installed_product_id(installed_product_id: str, question: str) -> str:
    """API for getting Service History given installed product id"""
    return print_tool("get_service_history_for_installed_product_id", "installed_product_id", installed_product_id,
                      question)


@tool
def query_records_by_name(name: str) -> str:
    """API for searching records given name"""
    return print_tool("query_records_by_name", "name", name)


@tool
def get_product_id_by_name(product_name: str) -> str:
    """API for getting product id given product name"""
    return print_tool("get_product_id_by_name", "product_name", product_name)


@tool
def knowledge_access(product_id: str, question: str) -> str:
    """API for Knowledge and help documentation"""
    return print_tool("knowledge_access", "product_id", product_id, question)


@tool
def schedule_management(question: str) -> str:
    """API for Schedule Management"""
    return print_tool("schedule_management", "", "", question)


def print_tool(tool_name: str, parameter_name: str, parameter_value: str, question=None) -> str:
    payload = '''tool_name=%s, parameters %s=%s > Rephrased Question = %s\n''' % (tool_name, parameter_name, parameter_value, question)
    # payload = "tool_name=%s " % tool_name
    # if parameter_name is not None:
    #     payload += " parameters %s=%s" % (parameter_name, parameter_value)
    # if question is not None:
    #     payload += " Rephrased Question=%s" % (question)
    return input(payload + 'Answer (enter) : ')
