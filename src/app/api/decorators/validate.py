from functools import wraps
from flask import request
from app.api.record.validation.validator import Validator as RecordValidator


def validate_record(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        RecordValidator().draft4_validate(data=request.json)
        return func(*args, **kwargs)

    return wrap

