from flask_jwt import jwt_required
from flask import request
from .validation.validator import Validator
from .service import Service
from app.infra.cache import CacheManager

cache = CacheManager()


@jwt_required()
@cache.caching.cached(timeout=cache.timeout, query_string=True)
def bill(number):
    period = request.args.get('period')

    return Service().get(data={'phone_number': number, 'period': period}, validation=Validator())
