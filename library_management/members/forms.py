from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    registerBtn = SubmitField('Register')

class EditForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    editBtn = SubmitField('Save Changes')