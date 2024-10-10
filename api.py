from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODICICATIONS'] = False
app.config['SECRET_KEY'] = 'mySecretKey'

db = SQLAlchemy(app)
api = Api(app)

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name Cannot be Blank!') 
user_args.add_argument('email', type=str, required=True, help='Email Cannot be Blank!')

userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()

        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        
        if not user:
            abort(404)
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()

        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        args = user_args.parse_args()
        
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        
        db.session.delete(user)
        db.session.commit()
        
        users = UserModel.query.all()
        return users, 204
        

api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user/<int:id>')

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    
    def __repr__(self):
        return f"User (name = {self.name}, email = {self.email}) "

@app.route('/')
def home():
    return "<h1>Flask API</h1>"