import os
from jsonschema import ValidationError, Draft4Validator, FormatChecker
import json
from app.api.ivalidation.schema import IValidation
from flask import abort
from http import HTTPStatus
from app.api.model.enums.enum import TypeCall
from app.utils.formats import PHONE_NUMBER_REX
import re


class Validator(IValidation):
    def __init__(self):
        self._name = 'record'

    def validate(self, **kwargs):
        if kwargs.get('type') == TypeCall.START.value:
            source = self._is_valid_phone_number(kwargs.get('source'))
            destination = self._is_valid_phone_number(kwargs.get('destination'))

            return source and destination
        else:
            return True

    def draft4_validate(self, **kwargs):
        try:
            Draft4Validator(self._schema(), format_checker=FormatChecker()).validate(kwargs.get('data'))
        except ValidationError as ex:
            abort(HTTPStatus.BAD_REQUEST, ex.message)

    def _schema(self):
        file_path = "{}/{}".format(os.path.dirname(__file__), self._name)
        with open(file_path, 'r', encoding="utf-8") as file_obj:
            data = file_obj.read()

        return json.loads(data)

    def _is_valid_phone_number(self, number):
        return number is not None and re.compile(PHONE_NUMBER_REX).match(number)
