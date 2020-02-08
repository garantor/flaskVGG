from index import *
from flask import jsonify
check = Projects.query.filter_by(id=1).first()
print(check.id)
newId = check.id
projectId = 1
# print(projectId)
if projectId == newId:
    Projects.query.filter_by(id=1).delete()
    db.session.commit()

