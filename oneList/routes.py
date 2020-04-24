from random import randint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from oneList import app, db, bcrypt, tools
from oneList.tools import getEpoch, epochToDate, logUser
from oneList.forms import RegistrationForm, LogInForm, ItemForm, SortDropDown, MakeAdminFrom,\
     ChangeUsername, ChangePassword, DeleteAccount
from oneList.models import User, Items
from oneList.storedProcedures import removeItem

# user can make an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Check session
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # get form
    form = RegistrationForm()

    # Check if form is 
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Get user info from form
        user = User(username=form.username.data, password=hashed_password, dateAdded=getEpoch(), isAdmin='false')

        try:
            # Add user
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            # Send them to the login
            return redirect(url_for('login'))
        except:
            # Undo if it broke
            db.session.rollback()
            flash('Your account has not been created.', 'fail') 
    return render_template('register.html', title='Register', form=form)

# Log in page
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Check if logged in
    if current_user.is_authenticated:
        return redirect(url_for('listApp'))
    # login get Login Form
    form = LogInForm()

    if form.validate_on_submit():
        # Get User using username
        user = User.query.filter_by(username=form.username.data).first()

        # Check password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # User login
            login_user(user, remember=form.remember.data)
            # Log the user
            logUser(request, current_user)
            return redirect(url_for('listApp'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Log out the user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# index page redirects the user to the right place
@app.route("/index")
@app.route("/", methods=['GET'])
def index():
    # Check user is logged in, move them to the app
    if current_user.is_authenticated:
        return redirect(url_for('listApp'))
    # If they are not logged in, make them log in
    else:
         return redirect(url_for('login'))

# list app page
@app.route("/app", methods=['GET','POST'])
@login_required
def listApp():
    # Froms
    sortForm = SortDropDown()
    itemForm = ItemForm()
    # Check how the user wants to sort
    if sortForm.sortOptions.data == "oldDate":
        itemsWithUsernames = db.session.execute('select * from itemsPage order by dateAdded DESC')
    elif sortForm.sortOptions.data == "userName":
        itemsWithUsernames = db.session.execute('select * from itemsPage order by username')
    else:
        itemsWithUsernames = db.session.execute('select * from itemsPage order by dateAdded ASC')
    return render_template(
        'app.html',
        title='List',
        sortForm=sortForm,
        itemForm=itemForm,
        dateConversion=epochToDate,
        posts=itemsWithUsernames
    )

# Used for added an Item
@app.route("/itemAction", methods=['POST'])
@login_required
def itemAction():
    # Get form
    addItemForm = ItemForm()
    # Check which button is pressed
    # Add an item button
    if 'submitAdd' in request.form:
        print("Add pressed")
        if addItemForm.validate_on_submit():
            anItem = Items(addedByUid=current_user.uid, item=addItemForm.text.data, dateAdded=getEpoch())
            db.session.add(anItem)
            db.session.commit()
        else:
            flash('Posted item needs to be 3-200 characters', 'warning')

    # Remove an item button
    elif 'submitDel' in request.form: 
        # remove all items checked
        for formiid in request.form.getlist('box'):
            try:
                formiid = int(formiid)
                removeItem(formiid, current_user.uid)
            except ValueError as err:
                print("[!!] Cause:", formiid, "Error:", err)
            
    return redirect(url_for('listApp'))

# Page that will show all the past items
@app.route("/removedItems", methods=['POST','GET'])
@login_required
def removedItems():
    # Get all removed items
    removedItemsWithUsernames = db.session.execute('select * from removedItemsPage')
    # Show then to the user
    return render_template('removed.html',
        removedItemsList=removedItemsWithUsernames,
        dateConversion=epochToDate)


# Get account settings and log
@app.route("/loginLog", methods=['POST','GET'])
@login_required
def loginLog():
    # Get from
    sortForm = SortDropDown()
    if current_user.isAdmin == 'true': 
        # Check if we need to sort
        if sortForm.sortOptions.data == "oldDate":
            sessions = db.session.execute('select * from sessionLog order by issueddate DESC')
        elif sortForm.sortOptions.data == "userName":
            sessions = db.session.execute('select * from sessionLog order by uid')
        else:
            sessions = db.session.execute('select * from sessionLog order by issueddate ASC')
    else:
        sessions = db.session.execute('select * from sessionLog where uid = :uid order by issueddate ASC',
            {'uid':current_user.uid}
        )
    return render_template(
        'loginLog.html',
        sessions=sessions,
        sortForm=sortForm,
        epochToDate=epochToDate
    )

# Menu for settings
@app.route("/settings", methods=['POST','GET'])
@login_required
def settings():
    # Show page to the user
    return render_template('settings.html')

# Page for username update
@app.route("/usernameChange", methods=['POST','GET'])
@login_required
def changeUserName():
    form = ChangeUsername()
    if form.validate_on_submit() and form.username.data != current_user.username:
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            if current_user.username=='admin':
                flash('Admin account change username.', 'warning')
            else:
                # Update username
                if form.username.data != "":
                    current_user.username = form.username.data
                    db.session.commit()
                    # Tell user
                    flash('Username Updated.', 'success')
                    return redirect(url_for('settings'))
                else:
                    flash('Username cannot be empty.', 'warning')
        else:
            flash('Password does not match.', 'danger')
    # Show page to the user
    return render_template('changeUsername.html',form=form)

# Page for password update
@app.route("/passwordChange", methods=['POST','GET'])
@login_required
def changePassword():
    form = ChangePassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            if form.newPassword.data == form.confirmNewPassword.data:
                current_user.password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
                db.session.commit()
                flash('Password Updated.', 'success')
                return redirect(url_for('settings'))
            else:
               flash('"New Password" and "Confirm New Password" fields do not match.', 'warning') 
        else:
            flash('Password does not match.', 'danger')
    # Show page to the user
    return render_template('changePassword.html',form=form)

# Page for Removing account
@app.route("/deleteAccount", methods=['POST','GET'])
@login_required
def deleteAccount():
    form = DeleteAccount()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            if current_user.username=='admin':
                flash('Admin account cannot be deleted.', 'warning')
            else:
                # Delete the user 
                db.session.execute('Delete from user where uid=:uid',{'uid':current_user.uid})
                db.session.commit()
                # Tell user
                flash('Account Deleted.', 'success')
                # Log out user
                logout_user()
                return redirect(url_for('login'))
        else:
            flash('Password does not match.', 'danger')
    # Show page to the user
    return render_template('deleteAccount.html',form=form)


