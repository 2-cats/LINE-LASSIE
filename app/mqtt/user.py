import pymysql
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def username_to_line_user_id(username):
    # Convert username to line_user_id
    database = pymysql.connect(
        app.config['DB_HOST'],
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME'],
        charset="utf8"
    )
    cursor = database.cursor()
    args = (username,)
    cursor.execute("SELECT line_user_id FROM users WHERE aws_user_name =  %s", args)
    result = cursor.fetchone()
    database.close()
    return result[0]
