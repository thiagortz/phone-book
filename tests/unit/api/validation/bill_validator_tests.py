from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from app.api.bill.validation.validator import Validator
from app.utils.formats import PHONE_NUMBER_REX, PERIOD_REX, PERIOD


class BillValidadorTests(TestCase):

    def setUp(self):
        self.validador = Validator()

    @patch("app.api.bill.validation.validator.re")
    def test_valid_phone_number(self, re):
        pattern = Mock()
        pattern.match.return_value = object()
        re.compile.return_value = pattern

        phone_number = '21945568909'
        self.validador._valid_phone_number(phone_number)
        re.compile.assert_called_once_with(PHONE_NUMBER_REX)
        pattern.match.assert_called_once_with(phone_number)

    @patch("app.api.bill.validation.validator.re")
    def test_valid_pattern_period(self, re):
        pattern = Mock()
        pattern.match.return_value = object()
        re.compile.return_value = pattern

        period = '12/2012'
        self.validador._valid_pattern_period(period)
        re.compile.assert_called_once_with(PERIOD_REX)
        pattern.match.assert_called_once_with(period)

    @patch("app.api.bill.validation.validator.datetime")
    def test_valid_period(self, datetime):
        datetime.now.return_value = Mock(year=2018, month=5)
        datetime.strptime.return_value = Mock(year=2018, month=3)
        self.validador._valid_period('09/2018')
        datetime.now.assert_called_once_with()
        datetime.strptime.assert_called_once_with('09/2018', PERIOD)

    @patch("app.api.bill.validation.validator.Validator._valid_period")
    @patch("app.api.bill.validation.validator.Validator._valid_pattern_period")
    @patch("app.api.bill.validation.validator.Validator._valid_phone_number")
    def test_validate(self, phone_number, pattern, period):
        self.validador.validate(phone_number='21950505050', period='09/2018')
        phone_number.assert_called_once_with('21950505050')
        pattern.assert_called_once_with('09/2018')
        period.assert_called_once_with('09/2018')
