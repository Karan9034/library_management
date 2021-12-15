from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class ReturnForm(FlaskForm):
    amount = StringField('Amount Paid', validators=[validators.DataRequired()])
    returnBtn = SubmitField('Return')