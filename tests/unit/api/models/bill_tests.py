from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
from datetime import timedelta, datetime
from app.api.model.bill import Bill


class BillTests(TestCase):

    def setUp(self):
        self.bill = Bill()

    def test_datetime_to_deltatime(self):
        now = datetime.now()
        result = self.bill._datetime_to_deltatime(now)
        self.assertIsInstance(result, timedelta)

    def test_calculate(self):
        price = self.bill._calculate(10, 10, 10)

        self.assertEqual(price, 110)
        self.assertIsInstance(price, int)

    def test_minutes_between(self):
        minutes = self.bill._minutes_between(timedelta(hours=23), timedelta(hours=22))
        self.assertIsInstance(minutes, float)
        self.assertEqual(minutes, 60.0)

    def test_is_standard_time(self):
        is_standard = self.bill._is_standard_time(timedelta(hours=12))
        self.assertIsInstance(is_standard, bool)
        self.assertEqual(is_standard, True)

    def test_duration_the_call(self):
        record_end = Mock(timestamp=datetime.strptime('Jun 1 2018  2:33PM', '%b %d %Y %I:%M%p'))
        record = Mock(record_end=record_end, timestamp=datetime.strptime('Jun 1 2018  1:33PM', '%b %d %Y %I:%M%p'))
        result = self.bill._duration_the_call(record)

        self.assertIsInstance(result, str)
        self.assertEqual(result, '1h0m')

    @patch("app.api.model.bill.Bill._datetime_to_deltatime", return_value=timedelta(hours=12))
    @patch("app.api.model.bill.Bill._is_standard_time", return_value=True)
    @patch("app.api.model.bill.Bill._minutes_between", return_value=60.0)
    @patch("app.api.model.bill.Bill._calculate", return_value=5.76)
    def test_calculate_call(self, _calculate, _minutes_between, _is_standard_time, _datetime_to_deltatime):
        record_end = Mock(timestamp=datetime.strptime('Jun 1 2018  2:33PM', '%b %d %Y %I:%M%p'))
        record = Mock(record_end=record_end, timestamp=datetime.strptime('Jun 1 2018  1:33PM', '%b %d %Y %I:%M%p'))

        result = self.bill._calculate_call(record)
        _is_standard_time.assert_called_with(timedelta(hours=12))
        _minutes_between.assert_called_once_with(start=record.record_end.timestamp, end=record.timestamp)
        _calculate.assert_called_once_with(0.36, 60.0, 0.09)

        self.assertIsInstance(result, float)
        self.assertEqual(result, 5.76)

    @patch("app.api.model.bill.Bill._duration_the_call", return_value='1h0m')
    @patch("app.api.model.bill.Bill._calculate_call", return_value=5.76)
    def test_build(self, _duration_the_call, _calculate_call):
        response = {'calls': [{
            'destination': 'TESTE',
            'start': '2018-06-01',
            'time': '13:33:00',
            'duration': '1h0m',
            'price': 5.76

        }], 'total': 5.76}

        record_end = Mock(timestamp=datetime.strptime('Jun 1 2018  2:33PM', '%b %d %Y %I:%M%p'))
        record = Mock(destination='TESTE', record_end=record_end,
                      timestamp=datetime.strptime('Jun 1 2018  1:33PM', '%b %d %Y %I:%M%p'))

        result = self.bill.build([record])
        self.assertIsInstance(result, dict)
        self.assertDictEqual(result, response)
