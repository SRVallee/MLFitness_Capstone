import pymysql as pm

def connect_to_db():
    connection = pm.connect(host='localhost',
                            user='root',
                            password='FitnessPassword123',
                            database='db',
                            cursorclass=pm.cursors.DictCursor)
    
    return connection

def select_exercise(conn):
    return