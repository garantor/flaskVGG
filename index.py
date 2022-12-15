import secrets
from models import *

# ===============================================================================
#  Creating flask_restful based class to handle api call
# ===============================================================================


class RegUsers(Resource):  # Create Users Class
    def post(self):
        parser.add_argument(
            "username", required=True, type=str, help="Username required"
        )
        parser.add_argument(
            "password", required=True, type=str, help="password required"
        )
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        check = Users.query.filter_by(username=username).first()
        if check:
            return jsonify({"message": "This Users already exists", "status_code": 400})
        else:
            adf = Users(username=username, password=password)
            db.session.add(adf)
            db.session.commit()
            return jsonify(
                {"username": username, "status": "add successfully", "status_code": 200}
            )


class authenticate(Resource):  # Authenticate and send secret token after authentication
    def post(self):
        parser.add_argument(
            "username", required=True, type=str, help="Username required"
        )
        parser.add_argument(
            "password", required=True, type=str, help="password required"
        )
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        user_exist = Users.query.filter_by(username=username, password=password).first()
        if user_exist:
            ad = secrets.token_hex(16)
            return jsonify(
                {
                    "message": "User Found",
                    "token": ad,
                    "status_code": 200,
                }
            )
        else:
            return jsonify(
                {"users": username, "status_code": 402, "message": "User not found"}
            )


class CreateProjects(Resource):  # Create project Class
    def post(self):
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("description", required=True, type=str)
        parser.add_argument(
            "completed",
            type=int,
            help="Take int 0 for not completed and 1 for completed",
        )
        args = parser.parse_args()
        username = args["name"]
        description = args["description"]
        completed = args["completed"]
        check = Projects.query.filter_by(name=username).first()
        try:
            projectName = check.name
            if username == projectName:
                return jsonify(
                    {"message": "Projects already Created", "status_code": 400}
                )
            else:
                pass
        except AttributeError as NoneType:
            newProjects = Projects(
                name=username, description=description, completed=completed
            )
            db.session.add(newProjects)
            db.session.commit()
            return jsonify(
                {
                    "message": f"Projects {username} has been added",
                    "status_code": 200,
                }
            )


class AllProjects(Resource):  # Class to Return all project
    def get(self):
        check = Projects.query.all()
        schema = projectSchema()
        result = schema.dump(check, many=True)
        return result


class GetById(Resource):  # Get a specific project by it Id
    def get(self, projectId):
        check = Projects.query.filter_by(id=projectId).first()
        if check:
            return jsonify(
                {"projectName": check.name, "PorjectDescription": check.description}
            )

        elif check == None:
            return jsonify(
                {"message": "This id is not found or incorrect", "status_code": 402}
            )
        else:
            pass


class updateProject(Resource):  # Update a specific project by id
    def put(self, projectId):
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("description", required=True, type=str)
        parser.add_argument(
            "completed",
            type=int,
            help="Take int 0 for not completed and 1 for completed",
        )
        args = parser.parse_args()
        username = args["name"]
        description = args["description"]
        completed = args["completed"]
        try:
            check = Projects.query.filter_by(id=projectId).first()
            checkId = check.id
            if projectId == checkId:
                check.name = username
                check.description = description
                check.completed = completed
                db.session.commit()
                return jsonify(
                    {
                        "message": f"Projects {username} has been Updated",
                        "status_code": 200,
                    }
                )
        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, project not found", "Status": 402})


class patchProject(Resource):  # Patch project/Update
    def patch(self, projectId):
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("description", required=True, type=str)
        parser.add_argument(
            "completed",
            type=int,
            help="Take int 0 for not completed and 1 for completed",
        )
        args = parser.parse_args()
        username = args["name"]
        description = args["description"]
        completed = args["completed"]
        try:
            check = Projects.query.filter_by(id=projectId).first()
            checkId = check.id
            if projectId == checkId:
                check.name = username
                check.description = description
                check.completed = completed
                db.session.commit()
                return jsonify({"message": "Projects Updated", "status_code": 200})
        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, project not Found", "Status": 402})


class deleteProject(Resource):  # Delete a specific project when given it Id
    def delete(self, projectId):
        try:
            check = Projects.query.filter_by(id=projectId).first()
            newId = check.id
            if projectId == newId:
                Projects.query.filter_by(id=projectId).delete()
                db.session.commit()
                return jsonify({"message": "Projects Deleted", "status_code": 200})
        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, project not found", "Status": 402})


class createActionProject(Resource):  # Create Action under a project
    def post(self, ProjectId):
        parser.add_argument("description", required=True, help=None)
        parser.add_argument("note", required=True)
        args = parser.parse_args()
        desc = args["description"]
        note = args["note"]
        try:
            check = Projects.query.filter_by(id=ProjectId).first()
            newId = check.id
            if newId:
                addAction = Actions(project_id=ProjectId, description=desc, note=note)
                db.session.add(addAction)
                db.session.commit()
                return jsonify({"message": "Projects Updated", "status_code": 200})
            else:
                print(check.id)
                return jsonify({"Error": "Project Not Found"})

        except AttributeError as NoneType:
            return jsonify(
                {"Error": "Bad Id, Project or Action Id not found", "Status": 402}
            )


class GetActionsAll(Resource):  # Return list of all actions when query
    def get(self):
        check = Actions.query.all()
        schema = ActionsSchema()
        result = schema.dump(check, many=True)
        return result


class ProjectsAllActions(Resource):  # Return all action that belong to a specific Id
    def get(self, projectId):
        try:
            check = Projects.query.filter_by(id=projectId).first()
            GetAction = check.action
            schema = ActionsSchema()
            result = schema.dump(GetAction, many=True)
            return result

        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, project not found", "Status": 402})


class GetAction(Resource):  # Get a specific action by it Id
    def get(self, actionId):
        act = Actions.query.filter_by(id=actionId).first()
        if act:
            return jsonify(
                {
                    "Project_id": act.project_id,
                    "description": act.description,
                    "note": act.note,
                }
            )
        else:
            return jsonify({"Error": "Bad Id, action not Found", "Status": 402})


class SingleActionByID(Resource):  # Single by it project if
    def get(self, projectId, actionId):
        ac = Projects.query.filter_by(id=projectId).first()
        ad = ac.action
        getAction = ad[actionId]
        schema = ActionsSchema()
        result = schema.dump(getAction)
        return result


class putSingle(Resource):  # Put class to add to an action that belongs to an Id
    def put(self, projectId, actionId):
        parser.add_argument("description", required=True, type=str)
        parser.add_argument("note", required=True, type=str)
        args = parser.parse_args()
        description = args["description"]
        note = args["note"]

        try:
            check_project = Projects.query.filter_by(id=projectId).first()
            if check_project:
                check_action = Actions.query.filter_by(id=actionId).first()
                check_action.description = description
                check_action.note = note
                db.session.commit()
                return jsonify({"message": "Projects Updated", "status_code": 200})

            else:
                return jsonify(
                    {"Error": "Bad Id, Project id Not found", "Status code ": 402}
                )
        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, Action Id is incorrect", "Status": 402})


class deleteActions(Resource):  # Class to delete actions
    def delete(self, projectId, actionId):
        try:
            check = Projects.query.filter_by(id=projectId).first()
            print(check.id)
            act = Actions.query.filter_by(id=actionId).first()
            print(act)
            newId = check.id
            newAct = act.id
            print(newId, newAct)
            if projectId == newId and actionId == newAct:
                Actions.query.filter_by(id=actionId).delete()
                db.session.commit()
                return jsonify({"message": "Projects Updated", "status_code": 200})

            else:
                return jsonify({"Error": "Bad Id, action Id not found", "Status": 402})
        except AttributeError as NoneType:
            return jsonify({"Error": "Bad Id, Project id not found", "Status": 402})


@app.route("/")  # Welcome route
def indexpage():
    data = [
        {
            "Register": {
                "endpoint": "/api/users/register/",
                "description": "register user",
            },
            "Authenticate": {
                "endpoint": "/api/users/auth/",
                "description": "Authenticate and confirm user",
            },
            "CreateProjects": {
                "endpoint": "/api/projects",
                "description": "create all project",
            },
            "AllProjects": {
                "endpoint": "/api/projects",
                "description": "return all project",
            },
            "Get project ": {
                "endpoint": "/api/projects/<int:projectId>",
                "description": "Get a single project by it ID",
            },
            "Update project": {
                "endpoint": "/api/projects/<int:projectId>",
                "description": "update project by ID",
            },

            "patchProject": {
                "endpoint": "/api/projects/<int:projectId>",
                "description": "Patch method to update the entire property of a project",
            },"deleteProject": {
                "endpoint": "/api/projects/<int:projectId>",
                "description": "Delete project by ID",
            },"createActionProject": {
                "endpoint": "/api/projects/<int:ProjectId>/actions",
                "description": "Create action under a specific project",
            },"GetAction": {
                "endpoint": "/api/actions/<int:actionId>",
                "description": "Return json list of all available action",
            },"SingleActionByID": {
                "endpoint": "/api/projects/<int:projectId>/actions/<int:actionId>",
                "description": " Get a single action by ID",
            },
            "putSingle":{
                "endpoint":"/api/projects/<int:projectId>/actions/<int:actionId>",
                "description":"/api/projects/<int:projectId>/actions/<int:actionId>"
            },
            "deleteActions":{"endpoint":"/api/projects/<int:projectId>/actions/<int:actionId>", "description":"Delete an action that belong to a project by action ID"}}
        
    ]
    return jsonify({"test": "Hello world", "endpoints": data})


api.add_resource(
    deleteActions, "/api/projects/<int:projectId>/actions/<int:actionId>"
)  # Delete an action that belong to a project by action ID
api.add_resource(
    putSingle, "/api/projects/<int:projectId>/actions/<int:actionId>"
)  # Put/Update a project particular Action by it id
api.add_resource(
    SingleActionByID, "/api/projects/<int:projectId>/actions/<int:actionId>"
)  # Get a single action by ID
api.add_resource(
    GetAction, "/api/actions/<int:actionId>"
)  # Get a single action by action Id
api.add_resource(
    ProjectsAllActions, "/api/projects/<int:projectId>/actions"
)  # Retrieve All action for a particlar project by project id
api.add_resource(
    GetActionsAll, "/api/actions"
)  # Return json list of all available action
api.add_resource(
    createActionProject, "/api/projects/<int:ProjectId>/actions"
)  # Create action under a specific project
api.add_resource(deleteProject, "/api/projects/<int:projectId>")
api.add_resource(
    patchProject, "/api/projects/<int:projectId>"
)  # Patch method to update the entire property of a project
api.add_resource(
    updateProject, "/api/projects/<int:projectId>"
)  # Update a specific project by it ID
api.add_resource(
    GetById, "/api/projects/<int:projectId>"
)  # Get a single project by it Id
api.add_resource(AllProjects, "/api/projects")  # return all project
api.add_resource(CreateProjects, "/api/projects")  # create all project
api.add_resource(authenticate, "/api/users/auth/")  # Authenticate and confirm user
api.add_resource(RegUsers, "/api/users/register/")  # Register New Users


if __name__ == "__main__":
    app.run(debug=True)
