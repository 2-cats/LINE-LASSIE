import pymysql
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# Convert username to line_user_id
def username_to_line_user_id(username):
    database = pymysql.connect(
        app.config['DB_HOST'],
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME'],
        charset="utf8"
    )
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name=%s and deleted_at IS NULL", args)
    result = cursor.fetchone()
    database.close()
    return result[0]

def get_push_id(username):
    database = pymysql.connect(
        app.config['DB_HOST'],
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME'],
        charset="utf8"
    )
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT source_id FROM users JOIN members ON users.id = members.user_id WHERE users.aws_user_name = %s ORDER BY members.id DESC", args)
    member_result = cursor.fetchone()
    if member_result is None:
        cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name = %s", args)
        user_result = cursor.fetchone()
        psuh_id = user_result[0]
    else:
        psuh_id = member_result[0]
    database.close()
    return psuh_id
