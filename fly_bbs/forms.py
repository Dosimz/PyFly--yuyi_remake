from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

# 登录验证表单
class LoginForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired('邮箱不能为空')])
    vercode = fields.StringField(validators=[InputRequired('验证码错误')])
    password = fields.PasswordField(validators=[DataRequired('密码长度应在6～16位之间')])

# 注册验证表单
class RegisterForm(FlaskForm):
    email = fields.StringField(validators=[DataRequired('邮箱不能为空'),
                                           Email('请输入正确的邮箱格式')])
    username = fields.StringField(validators=[DataRequired('昵称不能为空')])
    vercode = fields.StringField(validators=[InputRequired('验证码错误')])
    password = fields.PasswordField(validators=[Length(min=6, max=16, message='密码长度应该在6～16之间')])
    re_password = fields.PasswordField(validators=[EqualTo('password', '两次输入的密码不一样')])


class PostsForm(FlaskForm):
    id = fields.StringField()
    title = fields.StringField(validators=[DataRequired('帖子标题不能为空')])
    content = fields.StringField(validators=[DataRequired('帖子内容不能为空')])
    catalog_id = fields.StringField(validators=[DataRequired('帖子种类不能为空')])
    reward = fields.IntegerField(validators=[InputRequired('帖子悬赏不能不选')])
    vercode = fields.StringField(validators=[InputRequired('验证码不能为空')])
