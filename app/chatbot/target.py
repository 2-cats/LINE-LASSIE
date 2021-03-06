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
    cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name = %s and deleted_at=None", args)
    user_result = cursor.fetchone()
    database.close()
    return user_result[0]
