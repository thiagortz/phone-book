from app.api.ivalidation.schema import IValidation
from flask import abort
from http import HTTPStatus
from datetime import datetime
from app.utils.formats import PERIOD, PERIOD_REX, PHONE_NUMBER_REX
import re


class Validator(IValidation):

    def validate(self, **kwargs):

        self._valid_phone_number(kwargs.get('phone_number'))
        self._valid_pattern_period(kwargs.get('period'))
        self._valid_period(kwargs.get('period'))

    def _valid_phone_number(self, number):
        if re.compile(PHONE_NUMBER_REX).match(number) is None:
            abort(HTTPStatus.BAD_REQUEST, 'phone number must be at least 10 digits and at most 11')

    def _valid_pattern_period(self, period):
        if period is not None and re.compile(PERIOD_REX).match(period) is None:
            abort(HTTPStatus.BAD_REQUEST, 'the format of the period should be "01/2012" month/year')

    def _valid_period(self, period):
        if period is not None:
            today = datetime.now()
            period = datetime.strptime(period, PERIOD)

            if today.month == period.month and today.year == period.year:
                abort(HTTPStatus.BAD_REQUEST, 'You can only receive a phone bill after the end'
                                              ' of the reference period.')
