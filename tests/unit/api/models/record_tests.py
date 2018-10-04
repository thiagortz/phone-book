from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from app.api.model.record import Record, RecordStart, RecordEnd
from app.utils.formats import TIMESTAMP


class RecordTests(TestCase):

    def setUp(self):
        pass

    @patch("app.api.model.record.datetime")
    def test_build_start(self, datetime):
        datetime.strptime.return_value = Mock(year=2018, month=3, day=1)
        result = Record.build({
            'type': 1,
            'timestamp': 'TEST',
            'call_id': 'TEST',
            'source': 'TEST',
            'destination': 'TEST'
        })

        self.assertIsInstance(result, RecordStart)
        datetime.strptime.assert_called_once_with('TEST', TIMESTAMP)

    @patch("app.api.model.record.datetime")
    def test_build_end(self, datetime):
        datetime.strptime.return_value = Mock(year=2018, month=3, day=1)
        result = Record.build({
            'type': 2,
            'timestamp': 'TEST',
            'call_id': 'TEST',
        })

        self.assertIsInstance(result, RecordEnd)
        datetime.strptime.assert_called_once_with('TEST', TIMESTAMP)

