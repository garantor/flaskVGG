from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from decouple import config as env_getter


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= f"mysql+pymysql://{env_getter('AWS_DB_USER')}:{env_getter('AWS_DB_PASSWORD')}@{env_getter('AWS_DB_HOST')}:3306/{env_getter('AWS_DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

parser = reqparse.RequestParser()


#===============================================================================
#  Users Model(Scheme)
#===============================================================================

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"Users('{self.username}', '{self.password}')"



#===============================================================================
#  projects Model(Scheme)
#===============================================================================

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=True)
    action = db.relationship('Actions', backref='owner')

    def __repr__(self):
        return f"Projects('{self.name}', '{self.description}')"


#===============================================================================
#  Actions Model(Scheme)
#===============================================================================

class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Actions('{self.project_id}', '{self.description}')"


#===============================================================================
#  # Serilizating the Action Class using Marshemellow 
#===============================================================================

class ActionsSchema(Schema):
    project_id = fields.Integer()
    description = fields.Str()
    note = fields.Str()

class projectSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    completed = fields.Boolean()