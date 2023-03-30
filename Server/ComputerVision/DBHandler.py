import pymysql as pm


def connect_to_db():
    connection = pm.connect(host='localhost',
                            user='root',
                            password='FitnessPassword@123',
                            database='ml_fitness',
                            cursorclass=pm.cursors.DictCursor,
                            autocommit=True)
    
    return connection


# Selects
def select_one(conn, sql, whereArg):
    with conn.cursor() as cursor:
        if whereArg == None:
            cursor.execute(sql, ())
        else:
            cursor.execute(sql, (whereArg))
        results = cursor.fetchone()
    return results


def select_exercise(conn, name):
    sql = "SELECT * FROM exercise WHERE exercise=%s"
    # sql = "SELECT * FROM 'exercise'"
    return select_one(conn, sql, name)


def select_workout(conn, id):
    sql = "SELECT * FROM workout WHERE workout_id=%s"
    return select_one(conn, sql, id)


# inserts
def insert_one(conn, sql, argTuple):
    id = -1
    with conn.cursor() as cursor:
        cursor.execute(sql, argTuple)
        id = cursor.lastrowid

    return id


def insert_exercise(conn, exerciseName, demoLoc, modelLoc, trainer_id=None, notes =None):
    trainerStr = str(trainer_id) + ","
    notesStr = "," + notes 
    nArgs = 3
    if trainer_id:
        nArgs = nArgs +1
    if notes:
        nArgs = nArgs +1
    
    valsArr = []
    for i in range(nArgs):
        valsArr.append("%s")
    
    valsStr = ",".join(valsArr)
    
    sql = f"INSERT INTO exercise ({trainerStr} exercise, demo_location, model_location {notesStr})"\
          " VALUES ({valsStr})"
        
    return insert_one(conn, sql, (exerciseName, demoLoc, modelLoc))


def insert_workout(conn, userID, score, date, vidPath, exerciseName=None ,exerciseID=None):
    #TODO: if database is modifided, swap below
    # sql = "INSERT INTO workout (user_id, exercise_id, score, date, video_location)"\
    if exerciseID:
        sql = "INSERT INTO workout (user_user_id, exercise_exercise_id, score, date, video_location)"\
        " VALUES (%s, %s, %s, %s, %s)"
            
        return insert_one(conn, sql, (userID, exerciseID, score, date, vidPath))
    if exerciseName:
        exercise = select_exercise(conn, exerciseName)
        exID = exercise["exercise_id"]
        sql = "INSERT INTO workout (user_user_id, exercise_exercise_id, score, date, video_location)"\
        " VALUES (%s, %s, %s, %s, %s)"
            
        return insert_one(conn, sql, (userID, exID, score, date, vidPath))


# TESTING
def test_init(conn):
    user = "INSERT INTO user (username, password, name, email, is_trainer, api_key)"\
        " VALUES (%s, %s, %s, %s, %s, %s)"
    insert_one(conn, user, ("test_db", "testPass", "tester", "test", 1, "NONE"))
    
    insert_exercise(conn, "squat", "NONE", "NONE")
    

def main():
    con = connect_to_db()
    if not select_exercise(con, "squat"):
        test_init(con)
    
    sql = "SELECT MAX(workout_id) FROM workout"
    int(select_one(con, sql, None)["MAX(workout_id)"])
    
    lol = "TEST NOTES"
    
    insert_exercise(con, "squatest1", "demoLoc", "modeLoc")
    insert_exercise(con, "squatest2", "demoLoc", "modeLoc", trainer_id=6)
    insert_exercise(con, "squatest3", "demoLoc", "modeLoc", trainer_id=6, notes=lol)
    
    # id = insert_workout(con, 5, 1, "2023-03-23", "lol",  exerciseID=2)
    # print(select_workout(con, str(id)))
    
main()