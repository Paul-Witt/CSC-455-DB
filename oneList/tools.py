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

# this will add the trigger we need
def addTrigger():
    # The Sql that will add a trigger
    # The trigger adds one to the user's post count when they post
    updatePostCountSQL = '''
CREATE TRIGGER updatePostCount 
after INSERT 
on items
BEGIN
    UPDATE user
    SET postCount = user.postCount+1
    WHERE user.uid in
    (
        select addedByUid
        from items
        where iid in 
            (select max(iid)
            from items)
    );
END;'''

    db.session.execute(updatePostCountSQL)
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
    # Add Triggers
    addTrigger()
    # Add views
    addViews()
    # add admin
    makeAdmin()

# Log the user to get a login history
def logUser(request, current_user):
    recordLength = 30
    # Keep the logged sessions to 30
    sessions = db.session.\
        query(Sessions).\
        filter(Sessions.uid==current_user.uid).\
        order_by(Sessions.issueddate)
    # Check if session entries have exceded the recordLength
    if sessions.count()>recordLength-1:
        # Make a list of all the old sessions we want to remove
        removeSessions=sessions[:-(recordLength-1)]
        # removed each logged session
        for log in removeSessions:
            db.session.delete(log)
        db.session.commit()
    # Make a new entry for the current login
    newSession=Sessions(
        uid=current_user.uid, 
        ip=request.remote_addr,
        useragent=str(request.user_agent),
        issueddate=getEpoch()
    )
    # Add it to the database
    db.session.add(newSession)
    db.session.commit()







