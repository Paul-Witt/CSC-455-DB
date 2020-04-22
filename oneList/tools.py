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

# This will add the views we need
def addViews():
    # itemsPage SQL we will run
    addItemsPageViewSql = '''
CREATE VIEW itemsPage
AS
SELECT Items.iid, User.username, Items.item, Items.dateAdded
from Items
inner join User on Items.addedByUid = User.uid;'''
    
    # View for removed items page
    # outputs a table with rid, addedBy, item, dateAdded, dateRemoved, removedBy
    removedItemsPageViewSql = '''
CREATE VIEW removedItemsPage
AS
select * from 
(
    SELECT removed_items.rid, user.username as addedBy ,removed_items.item, removed_items.dateAdded, removed_items.dateRemoved
    from removed_items
    inner join User on removed_items.addedByUid = user.uid
)
NATURAL join
(   
    SELECT removed_items.rid, user.username as removedBy,removed_items.item, removed_items.dateAdded, removed_items.dateRemoved
    from removed_items
    inner join User on removed_items.removedByUid = user.uid
);'''
    # Add view by running SQL
    db.session.execute(addItemsPageViewSql)
    db.session.execute(removedItemsPageViewSql)
    db.session.commit()


# Make the DB and add the admin
def makeDB():
    # make 
    db.create_all()
    # Add views
    addViews()
    # add admin
    makeAdmin()

def logUser(request, current_user):
    thisSession = request.cookies['session']
    # log new session
    loggedSession = db.session.query(Sessions).filter(Sessions.session == thisSession)
    if loggedSession.count() == 0:
        now = getEpoch()
        newSession=Sessions(
            session=thisSession,
            uid=current_user.uid,
            dateIssued=now,
            lastUsed=now,
            ip=request.remote_addr,
            useragent=str(request.user_agent)
        )
        # add it to the database
        db.session.add(newSession)
        db.session.commit()
    # Update session
    else:
        # Get row from table
        loggedSession=loggedSession.first()
        # Update it
        loggedSession.ip=request.remote_addr
        loggedSession.lastUsed=getEpoch()
        loggedSession.useragent=str(request.user_agent)
        # save it
        db.session.commit()






