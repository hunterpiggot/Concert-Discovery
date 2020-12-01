from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    """
    This will be the inputs to create a user
    """

    states = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DC",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]

    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state = SelectField("State", choices=states, validators=[InputRequired()])
    search_radius = StringField("Search Radius", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """
    This will be to log in the user
    """

    email = StringField("email", validators=[InputRequired()])
    password = StringField("password", validators=[InputRequired()])