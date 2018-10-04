from app.api.idao.entity_dao import IDao
from app.api.config.entity import EntityManager
from app.api.model.record import RecordStart, RecordEnd
from app.api.model.bill import TelephoneBill
from app.infra.logger import LoggerManager

logger = LoggerManager(__name__)


class BillDao(IDao):
    def __init__(self, entity_manager=EntityManager()):
        self.manager = entity_manager

    def find(self, **kwargs):
        try:

            period_start = kwargs.get('period_start')
            period_end = kwargs.get('period_end')
            phone_number = kwargs.get('phone_number')
            result = self.manager.em.session.query(RecordStart).filter(RecordStart.source == phone_number,
                                                                       RecordStart.call_id == RecordEnd.call_id,
                                                                       RecordEnd.timestamp >= period_start,
                                                                       RecordEnd.timestamp < period_end).all()

            return TelephoneBill(result)

        except Exception as ex:
            logger.exception(str(ex))
            raise Exception('Could not fetch the bill')
