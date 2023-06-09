import string
import random
from api.models import Companies


def generate_token():
    """
    Generates the login token of a particular company.
    :return: company login token.
    """
    while True:
        new_token = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation.replace(" ", ""), k=32))
        if not Companies.objects.filter(token=new_token).exists():
            break
    return new_token
