--Login
--USERNAME is username from page form
--BCRYPT is hashed password from page form 
SELECT uid FROM User WHERE username = 'USERNAME' and pass = 'BCRYPT';

--Insert Session
--Python Inputs:'SESSION', 'UID', 'DATEISSUED', 'LASEUSED', 'IP', 'USERAGENT'
INSERT into Sessions (session, uid, dateIssued, laseUsed, ip, useragent)
	VALUES ('SESSION', 'UID', 'DATEISSUED', 'LASEUSED', 'IP', 'USERAGENT');

--CheckAdmin
--INPUTSESSION is session cookie
SELECT isAdmin FROM User WHERE uid in (
	SELECT uid from Sessions WHERE 'INPUTSESSION' = session);

--CheckSession
--INPUTSESSION is session cookie
SELECT uid FROM Sessions WHERE "INPUTSESSION" = session;

--AddItem
--Python Inputs: 'ADDEDBYUID', 'ITEM', 'DATEADDED'
INSERT INTO Items (addedByUid, item, dateAdded) 
	VALUES ('ADDEDBYUID', 'ITEM', 'DATEADDED');

--RemoveItem
-- 1)Delete
--Python Inputs: 'IID'
DELETE FROM Items WHERE iid = 'IID';
-- 2)Insert into removed table
--Python Inputs: 'REMOVEDBYUID', 'ADDEDBYUID', 'ITEM', 'DATEADDED', 'DATEREMOVED'
INSERT INTO RemoveItems (removedByUid, addedByUid, item, dateAdded, dateRemoved)
	VALUES ('REMOVEDBYUID', 'ADDEDBYUID', 'ITEM', 'DATEADDED', 'DATEREMOVED');

--LogOut
--Python Inputs: INPUTSESSION
DELETE FROM Sessions WHERE 'INPUTSESSION' = session;

-- AddUsers
--Python Inputs:'USERNAME', 'BCRYPT', 'UNIXDATE', 'ISADMIN'
INSERT INTO User (username, pass, dateAdded, isAdmin) 
	VALUES ('USERNAME', 'BCRYPT', 'UNIXDATE', 'ISADMIN');
