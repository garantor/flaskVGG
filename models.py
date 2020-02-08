
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

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






# def connecting_to_sqlite(database):
#     conn = None
#     try:
#         conn = sqlite3.connect(database)
#         return conn
#     except Error as e:
#         print(e)
 
#     return conn
 
 
# def tabelcreation(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)
 
 
# def main():
#     database = r"\vgg.db"

 
#     create_user_table = """ CREATE TABLE IF NOT EXISTS Users (
#                                         id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#                                         username text NOT NULL UNIQUE,
#                                         password text NOT NULL
#                                     ); """

#     create_project_table = """ CREATE TABLE IF NOT EXISTS Projects(
#                                             id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#                                             name text NOT NULL UNIQUE,
#                                             description string NOT NULL,
#                                             completed ); 
#     """
#     create_actions_table = """ CREATE TABLE IF NOT EXISTS Actions (
#                                             id integer ANTOINCREMENT,
#                                             project_id NUMERIC NOT NULL, 
#                                             description text NOT NULL,
#                                             note text NOT NULL,
#                                             FOREIGN KEY(project_id) REFERENCES Projects(id)
#     );"""



#     # create a database connection
#     conn = connecting_to_sqlite(database)
 
#     # create tables
#     if conn is not None:
#         tabelcreation(conn, create_user_table)
#         tabelcreation(conn, create_project_table)
#         tabelcreation(conn, create_actions_table)
#     else:
#         print("Error! cannot create the database connection.")
 
 
# # if __name__ == '__main__':
# #     main()

# main()
# CRUD
# create
# Retrieve
# Update
# delete
# Create users
def insertDB(email, password):
    conn = sqlite3.connect(r'\vgg.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO Users(username, password)VALUES (?,?)", (email, password))
    conn.commit()
    conn.close()

def Retrieve(email, password):
    conn = sqlite3.connect(r'\vgg.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE username = ? AND password= ?",([email, password]))
    data = cur.fetchall()
    return data
    conn.close()


# ad = Retrieve('afolabi', 'test')
# print(ad)