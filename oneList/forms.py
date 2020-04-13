from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from oneList.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember My Login")
    submit = SubmitField("Login")

class ItemForm(FlaskForm):
    #text = StringField("Text", validators=[DataRequired(), Length(min=2, max=200)])
    text = StringField("Text", validators=[Length(min=3, max=200)])
    submitAdd = SubmitField("Add item")
    submitDel = SubmitField("Remove Checked Items")
    box = BooleanField("Remove")


# class RemoveItem(FlaskForm):
#     box = BooleanField("Remove")
#     submit = SubmitField("XXXXRemove Checked Items")