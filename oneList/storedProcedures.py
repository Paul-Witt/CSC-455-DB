from sqlalchemy import text
#from sqlalchemy.sql.expression import func
from oneList import db
from oneList.models import User, Items, RemovedItems
from oneList.tools import getEpoch

# Moves items to removedItems tabel 
## This is our transaction 
def removeItem(itemID,removedByUid):
    myitem = db.session.query(Items).filter(Items.iid == itemID).first()
    try:
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
    except:
        db.session.rollback()

def deleteUser(uid):
    



