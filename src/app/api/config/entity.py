from flask_sqlalchemy import SQLAlchemy
from app.utils.singleton import Singleton

manager = SQLAlchemy()


class IManager(object):

    def init(self, app):
        raise NotImplementedError()


class EntityManager(IManager, metaclass=Singleton):

    def __init__(self):
        self.em = manager

    def init(self, app):
        self.em.init_app(app)
        self._map_entitys()
        self.em.create_all()

    def _map_entitys(self):
        import app.api.model.record
