from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///vgg.db'
db = SQLAlchemy(app)

# user = db.Table('Users', db.metadata, autoload=True, autoload_with=db.engine)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"Users('{self.username}', '{self.password}')"

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=True)
    action = db.relationship('Actions', backref='owner')

    def __repr__(self):
        return f"Projects('{self.name}', '{self.description}')"


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(100), nullable=False)



class RegUsers(Resource):
    def post(self,username, password):

        check = Users.query.filter_by(username=username).first()
        if check:
            return jsonify({'message':'This Users already exists', 'status_code':400})
        else:
            adf = Users(username=username, password=password)
            db.session.add(adf)
            db.session.commit()
            return jsonify({'users':username, 'status_code':200, 'message':'User Added'})


class authenticate(Resource):
    def post(self, username, password):
        status = Users.query.filter_by(username=username, password=password).first()
        if status:
            ad = secrets.token_hex(16)
            return jsonify({
                'message':'User Found'
                'token':ad,
                'status_code':200,
                
            })
        else:
            return jsonify({'users':username, 'status_code':400, 'message':'User not found'})





@app.route('/')
def indexpage():
    return jsonify({'test':'Hello world'})



api.add_resource(authenticate,'/api/users/auth/<string:username>/<string:password>')
api.add_resource(RegUsers, '/api/users/register/<string:username>/<string:password>')


if __name__ == "__main__":
    app.run(debug=True)
