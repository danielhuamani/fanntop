import uuid

def generate_code_favorite():
    return 'favorite-' + uuid.uuid4().hex[:8].lower()