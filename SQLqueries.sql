--Login
--USERNAME is username from page form
--BCRYPT is hashed password from page form 
SELECT uid FROM User WHERE username = 'USERNAME' and pass = 'BCRYPT';

--CheckAdmin
--INPUTSESSION is session cookie
SELECT isAdmin FROM User WHERE uid in (
	SELECT uid from Sessions WHERE 'INPUTSESSION' = session);



--CheckSession
--INPUTSESSION is session cookie
SELECT uid from Sessions WHERE "INPUTSESSION" =session;

--AddItem
--TODO
--RemoveItem
-- TODO
--  * insert
--  * delete

--LogOut
--INPUTSESSION is session cookie
delete from Sessions WHERE 'INPUTSESSION' = session;

-- AddUsers
-- 'USERNAME', 'BCRYPT', 'UNIXDATE', 'ISADMIN' will be input by python
insert into User values(1, 'USERNAME', 'BCRYPT', 'UNIXDATE', 'ISADMIN');
