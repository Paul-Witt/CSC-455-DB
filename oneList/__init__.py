from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path, getcwd 

databaseName = "oneList_Database.db"

pwd = getcwd()


app = Flask(__name__)
app.config['SECRET_KEY'] = '4ca1628ca0b13ce0c6c6dfde280ba14f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(databaseName)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


print(pwd+"\\oneList\\"+databaseName)

# If there is no database we make one
if not path.exists(pwd+"\\oneList\\"+databaseName):
    from oneList import tools
    tools.makeDB()

from oneList import routes








