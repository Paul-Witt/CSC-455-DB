from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path 

databaseName = "oneList_Database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = '4ca1628ca0b13ce0c6c6dfde280ba14f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(databaseName)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# a place for holding invite keys 
inviteKeyList = []

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# If there is no database we make one
dbPath = path.abspath("oneList/"+databaseName)

# Make the database if there isnt one
if not path.exists(dbPath):
    from oneList import tools
    tools.makeDB()

from oneList import routes








