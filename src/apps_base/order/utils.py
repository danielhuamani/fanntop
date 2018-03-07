import uuid

def generate_code_order():
    return 'order-' + str(uuid.uuid4()).replace("-", "")