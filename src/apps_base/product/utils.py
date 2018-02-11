import uuid

def generate_sku():
    return uuid.uuid4().hex[:8].upper()