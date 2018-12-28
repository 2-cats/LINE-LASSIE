from .rds import connect

def username_to_line_user_id(username):
    database = connect()
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_username =  %s", args)
    result = cursor.fetchone()
    database.close()
    return result[0]

def line_user_id_to_username(line_user_id):
    database = connect()
    cursor = database.cursor()
    args = (line_user_id,)
    cursor.execute("SELECT aws_username FROM users WHERE line_user_id =  %s", args)
    result = cursor.fetchone()
    database.close()
    return result[0]