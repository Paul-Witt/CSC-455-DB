from sqlalchemy import text
#from sqlalchemy.sql.expression import func
from oneList import db
from oneList.models import User, Items

def selectAllUsers():
    value = text("SELECT * FROM Users") # sqlalchemy
    return value

def pairItemAndUser():
    return db.session.query(User, Items).filter(User.uid == Items.addedByUid)

# TODO ADD removed Items to the Removed table
def removeItem(iid):
    myitem = db.session.query(Items).filter(Items.iid == iid).first()
    db.session.delete(myitem)
    db.session.commit()

