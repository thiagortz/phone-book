from app.api.idao.entity_dao import IDao
from app.api.config.entity import EntityManager
from app.api.model.record import TypeCall, RecordStart, RecordEnd
from app.infra.logger import LoggerManager
from sqlalchemy.exc import IntegrityError

logger = LoggerManager(__name__)


class RecordDao(IDao):
    foreign_key_violation = '23503'
    unique_violation = '23505'

    def __init__(self, entity_manager=EntityManager()):
        self.manager = entity_manager

    def add(self, **kwargs):
        try:
            self.manager.em.session.add(kwargs.get('record'))
            self.manager.em.session.commit()
        except IntegrityError as err:
            logger.exception(str(err))
            if err.orig.pgcode == self.foreign_key_violation:
                raise Exception('There is no start record with this call_id')
            elif err.orig.pgcode == self.unique_violation:
                raise Exception("The equal call_id record already exists on the base")
            else:
                raise Exception('could not save record')
        except Exception as ex:
            logger.exception(str(ex))
            raise Exception('could not save record')

    def find(self, **kwargs):
        try:
            record = kwargs.get('record')
            type_record = kwargs.get('type')

            if type_record == TypeCall.START:
                return self.manager.em.session.query(RecordStart).filter_by(call_id=record.call_id).first()
            else:
                return self.manager.em.session.query(RecordEnd).filter_by(call_id=record.call_id).first()

        except Exception as ex:
            logger.exception(str(ex))
            raise Exception('could not fetch record')

    def find_all(self, **kwargs):
        pass
