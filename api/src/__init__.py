from flask import Flask
from flask_cors import CORS
from src.config.config import Config
from dotenv import load_dotenv
from .routes import api


load_dotenv()

config = Config().dev_config()

app = Flask(config.APP_NAME)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.register_blueprint(api, url_prefix="/api")
