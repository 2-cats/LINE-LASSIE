'''
Handle 5breakfast and local Database
'''
import pymysql

import config
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def connect():
    '''
    Handle Database connect
    '''
    # database information
    database_ip = app.config['DB_HOST']
    database_user = app.config['DB_USERNAME']
    database_pw = app.config['DB_PASSWORD']
    database_name = app.config['DB_NAME']
    database = pymysql.connect(database_ip, database_user, database_pw, database_name, charset='utf8')
    return database
