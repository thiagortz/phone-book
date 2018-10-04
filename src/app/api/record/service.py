from app.api.iservice.business_service import IBusinessService
from flask import abort
from http import HTTPStatus
from .dao.record_dao import RecordDao
from app.api.model.record import Record


class Service(IBusinessService):
    def __init__(self):
        self.dao = RecordDao()

    def post(self, **kwargs):
        validator = kwargs.get('validation')

        is_valid = validator.validate(**kwargs.get('data'))

        if not is_valid:
            return abort(HTTPStatus.BAD_REQUEST, 'source and destination must be at least 10 digits and at most 11')

        try:
            record = Record.build(kwargs.get('data'))
            self.dao.add(record=record)

            return {'message': 'registration saved successfully'}, HTTPStatus.CREATED

        except Exception as ex:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(ex))
