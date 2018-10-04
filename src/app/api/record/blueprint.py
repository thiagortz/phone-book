from flask import Blueprint
from .controller import record


class RecordBluePrint:
    def __init__(self):
        blueprint = Blueprint('record', __name__, url_prefix='/v1')
        blueprint.add_url_rule('/call/record', methods=['POST'], view_func=record)
        self.blueprint = blueprint
