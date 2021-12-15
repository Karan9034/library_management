from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators

class ReturnForm(FlaskForm):
    amount = IntegerField('Amount Paid', validators=[validators.DataRequired()])
    returnBtn = SubmitField('Return')