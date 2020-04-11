from sqlalchemy import text
from sqlalchemy.sql.expression import oneList
from oneList import db

def selectAllUsers():
    value = text("SELECT * FROM agents") # sqlalchemy
    return value

