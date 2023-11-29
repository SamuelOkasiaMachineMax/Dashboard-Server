from flask import Blueprint, jsonify

FFTools_blueprint = Blueprint('csm', __name__)

@FFTools_blueprint.route('/csm-view/', methods=['GET'])
def FFTools():
    
    pass
