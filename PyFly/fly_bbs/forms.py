from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo

class RegisterForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired(), Email()])
    username = fields.StringField(validators=[DataRequired(), Email()])
    vercode = fields.StringField(validators=[InputRequired()])
    re_password = fields.PasswordField(validators=[EqualTo('password',)])
    

class LoginForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired()])
    vercode = fields.StringField(validators=[InputRequired()])
    password = fields.PasswordField(validators=[DataRequired()])
