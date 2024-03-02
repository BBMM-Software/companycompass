from flask import Blueprint
from .controllers.chat_controller import chat
from .controllers.script_controller import script

api = Blueprint('api', __name__)

api.register_blueprint(chat, url_prefix='/chat')
api.register_blueprint(script, url_prefix='/script')
