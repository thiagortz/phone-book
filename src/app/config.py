import os

APP_NAME = 'Phone_Book'
BLUEPRINT_VERSION = '/v1'
VERSION = '1.0.0'

PORT = int(os.environ.get('PORT', 8080))
DEBUG_MODE = os.environ.get('DEBUG', False)
SECRET_KEY = os.environ.get('{}_SECRET_KEY', '7ghzgwkLGV3JTiJM5LJSz3YuS8zUCBjG')

CACHE = {
    "config": {
        'CACHE_TYPE': os.environ.get('{}_CACHE_TYPE'.format(APP_NAME), 'simple'),
    },
    "timeout": int(os.environ.get('{}_TIMEOUT_CACHE_IN_SECONDS'.format(APP_NAME), 1800))
}

DB = {
    'url': os.environ.get('{}_DB_URL'.format(APP_NAME)),
}
