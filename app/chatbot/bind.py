'''
LINE account with Goodlinker AWS user

Created at 2018/12/26 by Eric
'''

from .rds import connect


# Check user is bind
def check_bind(line_user_id):
    database = connect()
    cursor = database.cursor()
    args = (line_user_id,)
    cursor.execute("SELECT aws_user_name FROM users WHERE line_user_id =  %s", args)
    result = cursor.fetchone()
    database.close()
    if result:
        return True
    return False
