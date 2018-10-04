from datetime import timedelta
from app.utils.formats import DATE, TIME


class IBill:
    def build(self, records):
        raise NotImplementedError()


class Bill(IBill):

    def __init__(self, standing_charge=0.36, call_charge=0.09):
        self.standing_charge = standing_charge
        self.call_charge = call_charge
        self.standard_time_call = (timedelta(hours=6), timedelta(hours=22))
        self.calls = []
        self.total = 0

    def build(self, records):
        for record in records:
            price = self._calculate_call(record)

            self.calls.append({
                'destination': record.destination,
                'start': record.timestamp.strftime(DATE),
                'time': record.timestamp.strftime(TIME),
                'duration': self._duration_the_call(record),
                'price': price

            })
            self.total += price

        return {'calls': self.calls, 'total': round(self.total, 2)}

    def _calculate_call(self, record):

        record_start_time = self._datetime_to_deltatime(record.timestamp)
        record_end_time = self._datetime_to_deltatime(record.record_end.timestamp)
        start_call = self._is_standard_time(record_start_time)
        end_call = self._is_standard_time(record_end_time)

        if start_call and end_call:
            minutes = self._minutes_between(start=record.record_end.timestamp, end=record.timestamp)
            return self._calculate(self.standing_charge, minutes, self.call_charge)
        elif start_call:
            minutes = self._minutes_between(start=self.standard_time_call[1], end=record_start_time)
            return self._calculate(self.standing_charge, minutes, self.call_charge)
        elif end_call:
            minutes = self._minutes_between(start=record_end_time, end=self.standard_time_call[0])
            return self._calculate(self.standing_charge, minutes, self.call_charge)

        return self.standing_charge

    def _is_standard_time(self, time):
        return self.standard_time_call[0] <= time <= self.standard_time_call[1]

    def _minutes_between(self, start, end):
        seconds = (start - end).total_seconds()
        return seconds // 60

    def _calculate(self, standing_charge, minutes, call_charge):
        return round(standing_charge + minutes * call_charge, 2)

    def _datetime_to_deltatime(self, datetime):
        return timedelta(seconds=datetime.second, minutes=datetime.minute, hours=datetime.hour)

    def _duration_the_call(self, record):
        duration = record.record_end.timestamp - record.timestamp
        return '{}h{}m'.format(duration.seconds // 3600, duration.seconds // 60 % 60)


class TelephoneBill:
    def __init__(self, records):
        self.records = records

    def build_billing(self, bill=Bill()):
        return bill.build(self.records)

    def is_valid(self):
        return len(self.records) > 0
