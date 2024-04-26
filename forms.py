from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import URL, NumberRange

class AddCupcakeForm(FlaskForm):
    '''Add a cupcake'''
    
    flavor = StringField("Flavor")
    size = SelectField(
        "Size",
        choices=[("small", "small"), ("medium", "medium"), ("large", "large")])
    rating = FloatField(
        "Rating",
        validators=[NumberRange(
            min=0.1, max=10.0, message="Select a number 1-10")])
    image = StringField(
        "Image URL",
        validators=[URL(
            require_tld=True, message="Please select an image url")])