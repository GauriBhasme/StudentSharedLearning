import Blueprint from flask
import Request from models

request_bp = Blueprint("api/request",__name__)

request_bp.route('/all')
def get_all_requests():
