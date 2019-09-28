from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo

class RegisterForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired('邮箱不能为空'), Email('格式不正确')])
    username = fields.StringField(validators=[DataRequired('昵称不能为空')])
    vercode = fields.StringField(validators=[InputRequired('验证码错误')])
    password = fields.PasswordField(validators=[Length(min=6, max=16, message='密码要在6-16位')])
    re_password = fields.PasswordField(validators=[EqualTo('password', '两次输入的密码不一致')])
    

class LoginForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired('邮箱不能为空')])
    vercode = fields.StringField(validators=[InputRequired('验证码错误')])
    password = fields.PasswordField(validators=[DataRequired('密码格式不对')])


class PostsForm(FlaskForm):
    id = fields.StringField()
    title = fields.StringField(validators=[DataRequired('code_msg.POST_TITLE_EMPTY.get_msg()')])
    content = fields.StringField(validators=[DataRequired('code_msg.POST_CONTENT_EMPTY.get_msg()')])
    catalog_id = fields.StringField(validators=[DataRequired('code_msg.POST_CATALOG_EMPTY.get_msg()')])
    reward = fields.IntegerField(validators=[InputRequired('code_msg.POST_COIN_EMPTY.get_msg()')])
    vercode = fields.StringField(validators=[InputRequired('code_msg.VERIFY_CODE_ERROR.get_msg()')])
