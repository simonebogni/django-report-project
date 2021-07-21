import uuid
from customers.models import Customer
from profiles.models import Profile

def generate_transaction_id():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_salesman_from_id(id):
    salesman = Profile.objects.get(id=id)
    return salesman.user.username

def get_customer_from_id(id):
    customer = Customer.objects.get(id=id)
    return customer