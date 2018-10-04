from app.api.decorators.validate import validate_record
from flask_jwt import jwt_required
from flask import request
from .validation.validator import Validator
from .service import Service


@jwt_required()
@validate_record
def record():

    return Service().post(data=request.json, validation=Validator())
