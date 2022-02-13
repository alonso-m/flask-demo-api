from flask_restx import Namespace, Resource, fields
from flask import request
from demo_api.models.users import User
import validators
from demo_api import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token

auth = Namespace("Auth", path="/auth", validate=True)

auth_register_request = auth.model('AuthRequestModel', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
    })

auth_register_response = auth.model('AuthRequestModel', {
    'username': fields.String,
    'email': fields.String,
    })

auth_login_request = auth.model('AuthRequestModel', {
    'username': fields.String,
    'email': fields.String,
    })

auth_login_response = auth.model('AuthResponseModel', {
    'access_token': fields.String,
    'username': fields.String,
    'email': fields.String
    })

@auth.route('/register')
class AuthRegister(Resource):
    @auth.doc(description='Register a user')
    @auth.expect(auth_register_request)
    @auth.marshal_with(auth_register_response)
    @auth.response(400, 'Validation error')
    def post(self):

        try:
            email = request.json['email']
            username = request.json['username']
            password = request.json['password']

            if not validators.email(email):
                auth.abort(400, 'Email is invalid')

            if User.query.filter_by(email=email).first() is not None:
                auth.abort(409, 'Email already exists')

            if User.query.filter_by(username=username).first() is not None:
                auth.abort(409, 'Username already exists')

            pwd_hash = generate_password_hash(password)

            user = User(username=username, password=pwd_hash, email=email)
            db.session.add(user)
            db.session.flush()
            db.session.commit()

            return {"username": username, "email": email}, 200

        except KeyError:
            auth.abort(400, "Email, username and password are required")

@auth.route('/login')
class AuthLogin(Resource):
    @auth.doc(description='Login a user')
    @auth.expect(auth_login_request)
    @auth.marshal_with(auth_login_response)
    @auth.response(400, 'Validation error')
    def post(self):
        try:
            password = request.json['password']
            email = request.json['email']

            user = User.query.filter_by(email=email).first()
            if user:
                is_pass_correct = check_password_hash(user.password, password)

                if is_pass_correct:
                    access_token = create_access_token(identity=user.id)
                    return {'access_token': access_token, 'username': user.username, 'email': user.email}, 200
                else:
                    auth.abort(400, "Password or user is incorrect")
            else:
                auth.abort(400, "Password or user is incorrect")
        except KeyError:
            auth.abort(400, "Email and password are required")


@auth.route('/me')
class AuthMe(Resource):
    @auth.doc(description='Get logged in users details')
    @auth.marshal_with(auth_register_response)
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()

        return {"username": user.username,"email": user.email}, 200