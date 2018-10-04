from flask import Blueprint
from .controller import bill


class BillBluePrint:
    def __init__(self):
        blueprint = Blueprint('bill', __name__, url_prefix='/v1')
        blueprint.add_url_rule('/telephone/<number>/bill', methods=['GET'], view_func=bill)
        self.blueprint = blueprint
