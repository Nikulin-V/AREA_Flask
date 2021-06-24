#  Nikulin Vasily (c) 2021
import random
import string


def generate_string(values=None, str_size=8, allowed_chars=string.ascii_letters + string.digits):
    if values is None:
        values = []
    res = ''.join(random.choice(allowed_chars) for _ in range(str_size))
    while res in values:
        res = ''.join(random.choice(allowed_chars) for _ in range(str_size))
    return str(res)
