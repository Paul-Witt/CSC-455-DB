from random import randint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from oneList import app, db, bcrypt, tools
from oneList.tools import getEpoch, epochToDate
from oneList.forms import RegistrationForm, LogInForm, ItemForm
from oneList.models import User, Items
from oneList.storedProcedures import pairItemAndUser, removeItem, selectRemovedItems, getUsername


'''
Notes
@login_required :: used to check if user is logged in

db.session.rollback()

'''

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
            # TODO
            login_user(user, remember=form.remember.data)
            # get fwd page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
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


@app.route("/app", methods=['GET','POST'])
@login_required
def listApp():
    return render_template('app.html', title='List', form=ItemForm(),dateConversion=epochToDate, posts=pairItemAndUser())


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
    if current_user.isAdmin == 'true': 
        return render_template('removed.html',removedItemsList=selectRemovedItems(),getUser=getUsername,dateConversion=epochToDate)
    else:
        return 'Admin only'

