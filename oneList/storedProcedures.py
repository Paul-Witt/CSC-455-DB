from sqlalchemy import text
#from sqlalchemy.sql.expression import func
from oneList import db
from oneList.models import User, Items, RemovedItems
from oneList.tools import getEpoch

def selectAllUsers():
    value = text("SELECT * FROM Users") # sqlalchemy
    return value

def pairItemAndUser():
    return db.session.query(User, Items).filter(User.uid == Items.addedByUid)

# Moves items to removed items tabel 
def removeItem(itemID,removedByUid):
    myitem = db.session.query(Items).filter(Items.iid == itemID).first()
    if myitem:
        removedItem = RemovedItems(
            removedByUid=removedByUid ,
            addedByUid=myitem.addedByUid ,
            item=myitem.item ,
            dateAdded=myitem.dateAdded ,
            dateRemoved=getEpoch()
        )
        db.session.add(removedItem)
        db.session.delete(myitem)
        db.session.commit()

# 
def selectRemovedItems():
    return db.session.query(RemovedItems).all()

