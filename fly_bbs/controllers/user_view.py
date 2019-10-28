
from fly_bbs.extensions import mongo
import json
import datetime
from bson import ObjectId
from fly_bbs import utils
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from fly_bbs import models
from fly_bbs import utils, forms
from flask_login import login_user,logout_user

user_view = Blueprint('user', __name__)


@user_view.route('/login/', methods=['GET','POST'])
def login():
    user_form = forms.LoginForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify({'status': 50001, 'msg': str(user_form.errors)})
        utils.verify_num(user_form.vercode.data)
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if not user:
            return jsonify({'status': 50102, 'msg': '用户不存在'})
        if not models.User.validate_login(user['password'], user_form.password.data):
            return jsonify({'status': 50000, 'msg': '密码错误'})
        if not user.get('is_active', False):
            return jsonify({'status': 403, 'msg': '账号未激活'})
        # session['username'] = user['username']
        # 使用扩展来进行登录
        login_user(models.User(user))
        return redirect(url_for('index.index'))
    # 登出用户
    logout_user()
    ver_code = utils.gen_verify_num()
    return render_template('user/login.html', ver_code=ver_code['question'], form=user_form)


@user_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@user_view.route('/register/', methods=['GET', 'POST'])
def register():
    # 创建注册的表单对象
    user_form = forms.RegisterForm()
    # 用户提交的表单
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify({'status': 50001, 'msg': str(user_form.errors)})
        utils.verify_num(user_form.vercode.data)
        # 查询这个邮箱是否有用户注册
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if user:
            return jsonify({'status': 50000, 'msg': '用户已注册'})
        # 创建注册用户的基本信息
        user = dict({
            'is_active': True,
            'coin': 0,
            'email': user_form.email.data,
            'username': user_form.username.data,
            'vip': 0,
            'reply_count': 0,
            'avatar': url_for('static', filename='images/avatar/' + str(randint(0, 12)) + '.jpg'),
            'password': generate_password_hash(user_form.password.data),
            'create_at': datetime.utcnow()
        })
        mongo.db.users.insert_one(user)
        # 跳转登录页面
        return redirect(url_for('user.login'))
    ver_code = utils.gen_verify_num()
    return render_template('user/reg.html', ver_code=ver_code['question'], form=user_form)

