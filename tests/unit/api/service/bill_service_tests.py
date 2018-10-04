from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from datetime import datetime
from app.api.bill.service import Service
from app.utils.formats import PERIOD


class BillServiceTests(TestCase):

    def setUp(self):
        self.bill = Service()

    @patch("app.api.bill.service.relativedelta")
    @patch("app.api.bill.service.datetime")
    def test_build_period(self, datetime, relativedelta):
        datetime.return_value = Mock(year=2018, month=3, day=31)
        datetime.strptime.return_value = Mock(year=2018, month=3, day=1)
        period = '12/2012'
        self.bill._build_period(period)

        datetime.strptime.assert_called_once_with(period, PERIOD)
        relativedelta.assert_called_once_with(months=+1)

    def test_build_period_none(self):
        start, end = self.bill._build_period(None)

        self.assertIsInstance(start, datetime)
        self.assertIsInstance(end, datetime)

    @patch("app.api.bill.service.BillDao.find")
    @patch("app.api.bill.service.Service._build_period")
    def test_get(self, build_period, find):
        period_start = datetime(year=2018, month=3, day=1)
        period_end = datetime(year=2018, month=3, day=31)
        telephone_bill = Mock()
        telephone_bill.is_valid.return_value = True
        telephone_bill.build_billing.return_value = {}
        find.return_value = telephone_bill
        build_period.return_value = period_start, period_end

        result = self.bill.get(validation=Mock(), data={'phone_number': 'TEST', 'period': 'TEST'})
        self.assertIsInstance(result, dict)
        find.assert_called_once_with(phone_number='TEST', period_start=period_start, period_end=period_end)
        telephone_bill.is_valid.assert_called_once_with()
        self.assertTrue(telephone_bill.build_billing.called)
