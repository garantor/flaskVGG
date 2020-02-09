# Please Ignore


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
