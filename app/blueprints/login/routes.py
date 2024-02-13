from flask import Blueprint, jsonify, request, current_app
from flask_httpauth import HTTPBasicAuth

login_blueprint = Blueprint('login', __name__)


auth = HTTPBasicAuth()

@login_blueprint.route('/loginn', methods=['POST'])
def login():
    username = ''
    password = ''

    try:
        username = request.json.get('internalmmax')
        password = request.json.get('maxmachineinteral')
        print(username, password)

    except Exception as e:
        print(e)
    # Replace the next line with your authentication logic
    if username == 'admin' and password == 'password':
        print('nice')
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401