from flask_caching import Cache
from app.config import CACHE
from app.utils.singleton import Singleton


class CacheManager(metaclass=Singleton):

    def __init__(self, config=CACHE["config"], timeout=CACHE["timeout"]):
        self.timeout = timeout
        self.caching = Cache(config=config)

    def init(self, app):
        self.caching.init_app(app)

    def clear(self):
        self.caching.clear()
