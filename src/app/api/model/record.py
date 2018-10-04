from app.api.config.entity import manager
from app.api.model.enums.enum import TypeCall
from app.utils.formats import TIMESTAMP
from datetime import datetime


class Record:

    @staticmethod
    def build(data):

        timestamp = datetime.strptime(data.get('timestamp'), TIMESTAMP)
        call_id = data.get('call_id')

        if data.get('type') == TypeCall.START.value:
            return RecordStart(timestamp=timestamp,
                               call_id=call_id,
                               source=data.get('source'),
                               destination=data.get('destination'))
        else:
            return RecordEnd(timestamp=timestamp,
                             call_id=call_id)


class RecordStart(manager.Model):
    __tablename__ = 'recordstart'

    id = manager.Column(manager.Integer, primary_key=True)
    timestamp = manager.Column(manager.DateTime, nullable=False)
    call_id = manager.Column(manager.Integer, nullable=False, unique=True)
    source = manager.Column(manager.String(11), nullable=True)
    destination = manager.Column(manager.String(11), nullable=True)
    record_end = manager.relationship("RecordEnd", uselist=False, back_populates="record_start")


class RecordEnd(manager.Model):
    __tablename__ = 'recordend'

    id = manager.Column(manager.Integer, primary_key=True)
    timestamp = manager.Column(manager.DateTime, nullable=False)
    call_id = manager.Column(manager.Integer, manager.ForeignKey('recordstart.call_id'), unique=True, nullable=False)
    record_start = manager.relationship("RecordStart", back_populates="record_end")
