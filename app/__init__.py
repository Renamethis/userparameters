from flask import Flask
from config import config
from .extensions import db, celery
import os

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    celery.init_app(app)
    return 