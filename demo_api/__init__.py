from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

from demo_api.config import DevConfig
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
JWTManager(app)

migrate = Migrate(app, db)

from demo_api.views import api_blueprint as api
app.register_blueprint(api)