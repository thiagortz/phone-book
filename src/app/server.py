from http import HTTPStatus
from flask import Flask
from app.config import PORT, DEBUG_MODE, SECRET_KEY, BLUEPRINT_VERSION, DB
from .utils.response import BaseResponse
from datetime import timedelta
from flask_jwt import JWT
from .api.model.user import User
from .infra.logger import LoggerManager
from .infra.cache import CacheManager
from .api.record.blueprint import RecordBluePrint
from .api.bill.blueprint import BillBluePrint
from app.api.config.entity import EntityManager

logger = LoggerManager(__name__)


class Server:
    def __init__(self):
        self._app = Flask(__name__)
        self._app.response_class = BaseResponse
        self._entity_manager = EntityManager()
        self._jwt = None

    def start(self, host='0.0.0.0', port=PORT, debug=DEBUG_MODE):
        self._register_blueprints()
        self._set_configs()
        self._init_jwt()
        self._init_cache()
        self._init_db()
        self._errors_handler()
        self._app.run(host=host, port=port, debug=debug)

    def _register_blueprints(self):
        self._app.register_blueprint(RecordBluePrint().blueprint)
        self._app.register_blueprint(BillBluePrint().blueprint)

    def _set_configs(self):
        self._app.config['SECRET_KEY'] = SECRET_KEY
        self._app.config['SQLALCHEMY_DATABASE_URI'] = DB['url']
        self._app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
        self._app.config['JWT_AUTH_URL_RULE'] = '{}/auth'.format(BLUEPRINT_VERSION)

    def _init_jwt(self):
        self._jwt = JWT(self._app, User.authenticate, User.identity)

    def _init_cache(self):
        CacheManager().init(self._app)

    def _init_db(self):
        with self._app.app_context():
            self._entity_manager.init(self._app)

    def _errors_handler(self):
        app = self._app
        jwt = self._jwt

        @jwt.jwt_error_handler
        @app.errorhandler(HTTPStatus.UNAUTHORIZED)
        def unauthorized(error):
            logger.error(error.description)
            return {'errors': [{'message': error.description}]}, HTTPStatus.UNAUTHORIZED

        @app.errorhandler(HTTPStatus.BAD_REQUEST)
        def bad_request(error):
            logger.error(error)
            return {'errors': [{'message': error.description}]}, HTTPStatus.BAD_REQUEST

        @app.errorhandler(HTTPStatus.NOT_FOUND)
        def not_found(error):
            logger.error(error)
            return {'errors': [{'message': error.description}]}, HTTPStatus.NOT_FOUND

        @app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
        def method_not_allowed(error):
            logger.error(error)
            return {'errors': [{'message': error.description}]}, HTTPStatus.METHOD_NOT_ALLOWED

        @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
        def internal_server_error(error):
            logger.error(error)
            return {'errors': [{'message': error.description}]}, HTTPStatus.INTERNAL_SERVER_ERROR

        @app.errorhandler(Exception)
        def internal_server_error_exception(error):
            logger.exception(error)
            return {'errors': [{'message': HTTPStatus.INTERNAL_SERVER_ERROR._name_}]}, HTTPStatus.INTERNAL_SERVER_ERROR
