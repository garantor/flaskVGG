from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///vgg.db'
db = SQLAlchemy(app)



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

    def __repr__(self):
        return f"Actions('{self.project_id}', '{self.description}')"




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
                'message':'User Found',
                'token':ad,
                'status_code':200,
                
            })
        else:
            return jsonify({'users':username, 'status_code':400, 'message':'User not found'})



class CreateProjects(Resource):
    def post(self, name, desc, completed):
        check =Projects.query.filter_by(name=name).first()
        try:
            projectName=check.name
            if name == projectName:
                return jsonify({
                    'message':'Projects all Created',
                    'status_code':401})
            else:
                pass
        except AttributeError as NoneType:
            newProjects = Projects(name=name, description=desc, completed=completed)
            db.session.add(newProjects)
            db.session.commit()
            return jsonify({
                'message':f'Projects {name} has been added',
                'status_code': 200,
            })

class AllProjects(Resource):
    def get(self):
        allProjects = Projects.query.all()
        ad = allProjects
        print(ad)
        for a in ad:
            allnames = a.name
            print(a)
            print(allnames)
            return jsonify({
                'names': allnames
            }) 
     
class GetById(Resource):
    def get(self, projectId):
        check =Projects.query.filter_by(id=projectId).first()
        if check:
            return jsonify({
                    'projectName':check.name,
                    'PorjectDescription': check.description
                })


class updateProject(Resource):
    def put(self, projectId, name, desc, status):
        
        try:
            check = Projects.query.filter_by(id=projectId).first()
            checkId = check.id
            if projectId == checkId:
                check.name = name
                check.description= desc
                check.completed=status
                db.session.commit()
                return jsonify({
                    'message': 'Projects Updated',
                    'status_code': 200
                })
        except AttributeError as NoneType:
            return jsonify({
                'Error': 'Bad Id',
                'Status': 401
            })

class patchProject(Resource):
    def patch(self, projectId, name, desc, status):
            try:
                check = Projects.query.filter_by(id=projectId).first()
                checkId = check.id
                if projectId == checkId:
                    check.name = name
                    check.description= desc
                    check.completed=status
                    db.session.commit()
                    return jsonify({
                        'message': 'Projects Updated',
                        'status_code': 200
                    })
            except AttributeError as NoneType:
                return jsonify({
                    'Error': 'Bad Id',
                    'Status': 401
                })
class deleteProject(Resource):
    def delete(self, projectId):
        try:
            check = Projects.query.filter_by(id=projectId).first()
            newId = check.id
            if projectId == newId:
                Projects.query.filter_by(id=projectId).delete()
                db.session.commit()
                return jsonify({
                            'message': 'Projects Updated',
                            'status_code': 200
                        })
        except AttributeError as NoneType:
            return jsonify({
                    'Error': 'Bad Id',
                    'Status': 401
                })

@app.route('/')
def indexpage():
    return jsonify({'test':'Hello world'})


api.add_resource(deleteProject, '/api/projects/<int:projectId>')
api.add_resource(patchProject, '/api/projects/<int:projectId>/<string:name>/<string:desc>/<int:status>')
api.add_resource(updateProject, '/api/projects/<int:projectId>/<string:name>/<string:desc>/<int:status>')
api.add_resource(GetById, '/api/projects/<string:projectId>')
api.add_resource(AllProjects, '/api/projects')
api.add_resource(CreateProjects, '/api/projects/<string:name>/<string:desc>/<int:completed>')
api.add_resource(authenticate,'/api/users/auth/<string:username>/<string:password>')
api.add_resource(RegUsers, '/api/users/register/<string:username>/<string:password>')


if __name__ == "__main__":
    app.run(debug=True)
# get all project no working yet