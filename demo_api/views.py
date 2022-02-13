from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)

api = Api(
    api_blueprint,
    title="App for demonstration purposes",
    description="This is an app to showcase in an interview",
    contact="Miguel Alonso",
    contact_email="malonso.inbox@gmail.com"
)

from demo_api.namespaces.auth import auth
api.add_namespace(auth)