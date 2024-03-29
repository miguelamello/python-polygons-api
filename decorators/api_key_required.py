from functools import wraps
from flask import request
from appconfig import env

# API-KEYS
API_KEYS = [ env['api-key'] ]


def api_key_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api-key')
        if api_key and api_key in API_KEYS:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid API key. See documentation.'}, 401  # Unauthorized

    return decorated_function
