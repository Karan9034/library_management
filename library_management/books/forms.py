from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, validators

class ImportForm(FlaskForm):
    number = IntegerField('No. of books', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    quantity = IntegerField('Quantity of each book', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    title = StringField('Title', validators=[validators.Optional()])
    authors = StringField('Authors', validators=[validators.Optional()])
    isbn = StringField('ISBN', validators=[validators.Optional()])
    publisher = StringField('Publisher', validators=[validators.Optional(), validators.Length(min=10, max=10)])
    importBtn = SubmitField('Import')

class IssueForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    book_id = IntegerField('Book ID', validators=[validators.DataRequired()])
    dues_per_week = IntegerField('Charges Per Week', validators=[validators.DataRequired()])
    issueBtn = SubmitField('Issue')