from flask import Blueprint


bp = Blueprint('user', __name__)


@bp.route('/', methods=['POST'])
def create_user():
    pass
