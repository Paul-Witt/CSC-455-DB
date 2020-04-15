from oneList import db, bcrypt
from oneList.models import User, Sessions, RemovedItems, Items
from datetime import datetime
import time

'''
Gets the seconds since epoch
'''
def getEpoch():
	return int(time.time())

'''
Converts an epoch time stamp to a readable date
@Pram epoch :: int
'''
def epochToDate(epoch):
	return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M')

# Make the admin
def makeAdmin():
    # Hash password
    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    # Add user, ID will AI
    admin = User(username='admin', password=hashed_password, dateAdded=getEpoch(), isAdmin = 'true')
    # Commit user
    db.session.add(admin)
    db.session.commit()

def addItem(text='Nothing'):
    anItem = Items(addedByUid=1, item=text,dateAdded=getEpoch())
    db.session.add(anItem)
    db.session.commit()

# Make the DB and add the admin
def makeDB():
    # make 
    db.create_all()
    # add admin
    makeAdmin()




