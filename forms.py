from flask_wtf import Form
from wtforms import StringField, SelectField, validators
from utils import get_countries

country_list = get_countries()

class ReusableForm(Form):
    
    #Set up form
    name = StringField('Recipe Name:', validators=[validators.DataRequired("*Required")])
    description = StringField('Description:', validators=[validators.DataRequired("*Required")])
    author = StringField('Author:', validators=[validators.DataRequired("*Required")])
    instruction1 = StringField('Step 1:', validators=[validators.DataRequired("*Required")])
    ingredient1 = StringField( validators=[validators.DataRequired("*Required")])
    country = SelectField('Country of Origin', choices=country_list, validators=[validators.InputRequired(message=('*Required'))]) 

class Username(Form):
    #Set up form
    username = StringField('Username:', validators=[validators.DataRequired("*Required")])

class Search(Form):
    #Set up form
    search = StringField('Search:', validators=[validators.DataRequired("*Required")])