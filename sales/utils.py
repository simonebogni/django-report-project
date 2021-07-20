import uuid

def generate_transaction_id():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code