import sqlite3
from sqlite3 import Error
 
 
def connecting_to_sqlite(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def tabelcreation(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
 
 
def main():
    database = r"\vgg.db"

 
    create_user_table = """ CREATE TABLE IF NOT EXISTS Users (
                                        id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        username text NOT NULL UNIQUE,
                                        password text NOT NULL
                                    ); """

    create_project_table = """ CREATE TABLE IF NOT EXISTS Projects(
                                            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                                            name text NOT NULL UNIQUE,
                                            description string NOT NULL,
                                            completed ); 
    """
    create_actions_table = """ CREATE TABLE IF NOT EXISTS Actions (
                                            id integer ANTOINCREMENT,
                                            project_id NUMERIC NOT NULL, 
                                            description text NOT NULL,
                                            note text NOT NULL,
                                            FOREIGN KEY(project_id) REFERENCES Projects(id)
    );"""



    # create a database connection
    conn = connecting_to_sqlite(database)
 
    # create tables
    if conn is not None:
        tabelcreation(conn, create_user_table)
        tabelcreation(conn, create_project_table)
        tabelcreation(conn, create_actions_table)
    else:
        print("Error! cannot create the database connection.")
 
 
# if __name__ == '__main__':
#     main()

main()