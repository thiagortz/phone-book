from app.api.iservice.business_service import IBusinessService
from .dao.dao import BillDao
from app.api.model.bill import Bill
from app.infra.logger import LoggerManager
from datetime import timedelta, datetime
from flask import abort
from http import HTTPStatus
from app.utils.formats import PERIOD, DATE
from dateutil.relativedelta import relativedelta

logger = LoggerManager(__name__)


class Service(IBusinessService):

    def __init__(self):
        self.dao = BillDao()

    def post(self, **kwargs):
        raise NotImplementedError()

    def get(self, **kwargs):
        validator = kwargs.get('validation')
        validator.validate(**kwargs.get('data'))

        phone_number = kwargs.get('data').get('phone_number')

        period_start, period_end = self._build_period(kwargs.get('data').get('period'))

        telephone_bill = self.dao.find(phone_number=phone_number, period_start=period_start, period_end=period_end)

        if not telephone_bill.is_valid():
            abort(HTTPStatus.NOT_FOUND,
                  'no phone bill for the number {} in the period {} - {}'.format(phone_number,
                                                                                 period_start.strftime(DATE),
                                                                                 (period_end - timedelta(
                                                                                     days=1)).strftime(DATE)))
        bill = telephone_bill.build_billing(Bill())

        return bill

    def _build_period(self, period):
        start = None
        end = None

        if period is None:
            end = datetime.today().replace(day=1)
            start = (end - timedelta(days=1)).replace(day=1)
        else:
            start = datetime.strptime(period, PERIOD)
            end = start + relativedelta(months=+1)

        return start, end
