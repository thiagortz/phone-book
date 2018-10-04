from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from app.api.record.validation.validator import Validator
from app.utils.formats import PHONE_NUMBER_REX


class RecordValidadorTests(TestCase):

    def setUp(self):
        self.validador = Validator()

    @patch("app.api.record.validation.validator.re")
    def test_is_valid_phone_number(self, re):
        pattern = Mock()
        pattern.match.return_value = object()
        re.compile.return_value = pattern

        phone_number = '21945568909'
        self.validador._is_valid_phone_number(phone_number)
        re.compile.assert_called_once_with(PHONE_NUMBER_REX)

    @patch("app.api.record.validation.validator.Validator._schema")
    @patch("app.api.record.validation.validator.FormatChecker")
    @patch("app.api.record.validation.validator.Draft4Validator")
    def test_draft4_validate(self, draft4, format, schema):
        draft4.validate.return_value = None
        self.validador.draft4_validate(data={})
        draft4.assert_called_once_with(schema(), format_checker=format())
