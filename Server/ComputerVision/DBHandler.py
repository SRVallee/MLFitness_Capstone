import pymysql as pm

def connect_to_db():
    connection = pm.connect(host='localhost',
                            user='root',
                            password='FitnessPassword@123',
                            database='db',
                            cursorclass=pm.cursors.DictCursor)
    
    return connection

def select_exercise(conn, name):
    with conn.cursor as cursor:
        sql = "SELECT * FROM 'exercise' WHERE 'exercise'=%s"
        cursor.execute(sql, name)
        results = cursor.fetchone()
        print(results)
    return results