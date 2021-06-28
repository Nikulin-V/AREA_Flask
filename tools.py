#  Nikulin Vasily (c) 2021
import random
import string

from flask import request, abort

from config import HOST


def generate_string(values=None, str_size=8, allowed_chars=string.ascii_letters + string.digits):
    if values is None:
        values = []
    res = ''.join(random.choice(allowed_chars) for _ in range(str_size))
    while res in values:
        res = ''.join(random.choice(allowed_chars) for _ in range(str_size))
    return str(res)


def use_subdomains(subdomains=None):
    if subdomains is None:
        subdomains = ['area']

    def subdomains_decorator(func):

        def wrapper(*args, **kwargs):
            subdomain = get_subdomain()
            if subdomain in subdomains:
                return func(*args, **kwargs, subdomain=subdomain)
            else:
                abort(404)

        return wrapper

    return subdomains_decorator


def get_subdomain():
    host = request.host
    if host == HOST:
        return 'area'
    elif host.endswith(HOST):
        return host.split('.')[0]
