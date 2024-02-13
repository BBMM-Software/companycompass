from flask import Flask
from flask_cors import CORS
from src.config.config import Config
from dotenv import load_dotenv
from .routes import api

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


config = Config().dev_config()

app.config['ENV'] = config.ENV

app.register_blueprint(api, url_prefix='/api')
