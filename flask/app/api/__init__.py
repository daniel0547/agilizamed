from flask import jsonify, Blueprint

api = Blueprint('api', __name__, template_folder='templates', static_folder='../static')

@api.route('/teste', methods=['POST'])
def get_token():
    return jsonify(success=True, message='Hello World!')