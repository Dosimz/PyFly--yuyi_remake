
from fly_bbs.extensions import mongo
import json
import datetime
from bson import ObjectId
from fly_bbs import utils,forms, models, db_utils, code_msg
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from fly_bbs import models
from flask_login import login_user, logout_user, login_required, current_user

user_view = Blueprint('user', __name__)


@user_view.route('/active', methods=['GET', 'POST'])
def user_active():
    if request.method == 'GET':
        code = request.values.get('code')
        if code:
            user_id = mongo.db.active_codes.find_one({'_id': ObjectId(code)})['user_id']
            # 可以激活账户了
            if user_id:
                # 通过激活验证后，删掉 user_id 关联的 active_codes 
                mongo.db.active_codes.delete_many({'user_id': ObjectId(user_id)})
                # 激活账户
                mongo.db.users.update({'_id': user_id}, {"$set": {'is_active': True}})
                # 根据 user_id 在数据库中取到用户对象
                user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
                # 登录
                login_user(models.User(user))
                return render_template('user/activate.html')
        # 如果没有登录,显示错误
        if not current_user.is_authenticated:
            abort(403)
        return render_template('user/activate.html')

    if not current_user.is_authenticated:
        abort(403)
    user = current_user.user
    # 删除
    mongo.db.active_codes.delete_many({'user_id': ObjectId(user['_id'])})
    # 发送邮件
    send_active_email(user['username'], user['_id'], user['email'])
    return jsonify(code_msg.RE_ACTIVATE_MAIL_SEND.put('action', url_for('user.active')))


def send_active_email(username, user_id, email, is_forget=False):
    code = mongo.db.active_codes.insert_one({'user_id': user_id})
    # 激活邮件内容
    body = render_template('email/user_active.html', username=username,
                           url=url_for('user.user_active', code=code.inserted_id, _external=True))
    # 发送邮件
    utils.send_email(email, '账号激活', body=body)


@user_view.route('/repass', methods=['POST'])
def user_repass():
    # 未登录用户跳转到登录页面
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    pwd_form = forms.ChangePassWordForm()
    if not pwd_form.validate():
        return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(pwd_form.errors)))
    nowpassword = pwd_form.nowpassword.data
    password = pwd_form.password.data
    user = current_user.user
    # 验证输入密码是否正确
    if not models.User.validate_login(user['password'], nowpassword):
        raise models.GlobalApiException(code_msg.PASSWORD_ERROR)
    # 更新密码
    mongo.db.users.update({'_id': user['_id']}, {'$set': {'password': generate_password_hash(password)}})
    return jsonify(models.R.ok())


@user_view.route('/set', methods=['GET', 'POST'])
@login_required
def user_set():
    if request.method == 'POST':
        include_keys = ['username', 'avatar', 'desc', 'city', 'sex']
        data = request.values
        update_data = {}
        for key in data.keys():
            if key in include_keys:
                update_data[key] = data.get(key)
        mongo.db.users.update({'_id': current_user.user['_id']}, {'$set': update_data})
        return jsonify('修改成功')
    return render_template('user/set.html', user_page='set', page_name='user', title='基本设置')


@user_view.route('/message')
@user_view.route('/message/page/<int:pn>')
@login_required
def user_message(pn=1):
    user = current_user.user
    if user.get('unread', 0) > 0:
        # 更新未读消息重新为零
        mongo.db.users.update({'_id': user['_id']}, {'$set': {'unread': 0}})
    message_page = db_utils.get_page('messages', pn, filter1={'user_id': user['_id']}, sort_by=('_id', -1))
    return render_template('user/message.html', user_page='message', page_name='user', page=message_page)



@user_view.route('/message/remove', methods=['POST'])
@login_required
def remove_message():
    user = current_user.user
    if request.values.get('all') == 'true':
        mongo.db.messages.delete_many({'user_id': user['_id']})
    elif request.values.get('id'):
        msg_id = ObjectId(request.values.get('id'))
        mongo.db.messages.delete_one({'_id': msg_id})
    return jsonify(models.BaseResult())



# 用户 home 界面
@user_view.route('/<ObjectId:user_id>')
@login_required
def user_home(user_id):
    # 在数据库 user 集合中查找主键为 user_id 的数据
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    return render_template('user/home.html', user=user)


@user_view.route('/login/', methods=['GET','POST'])
def login():
    user_form = forms.LoginForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(user_form.errors)))
        utils.verify_num(user_form.vercode.data)
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if not user:
            return jsonify(code_msg.USER_NOT_EXIST)
        if not models.User.validate_login(user['password'], user_form.password.data):
            raise models.GlobalApiException(code_msg.PASSWORD_ERROR)
        if not user.get('is_active', False):
            return jsonify(code_msg.USER_UN_ACTIVE)
        if user.get('is_disabled', False):
            return jsonify(code_msg.USER_DISABLED)
        login_user(models.User(user))
        action = request.values.get('next')
        if not action:
            action = url_for('index.index')
        return jsonify(code_msg.LOGIN_SUCCESS.put('action', action))
    logout_user()
    ver_code = utils.gen_verify_num()
    # session['ver_code'] = ver_code['answer']
    return render_template('user/login.html', ver_code=ver_code['question'], form=user_form, title='登录')


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
            return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(user_form.errors)))
        utils.verify_num(user_form.vercode.data)
        # 查询这个邮箱是否有用户注册
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if user:
            return jsonify(code_msg.EMAIL_EXIST)
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
        # 每次在数据库添加完注册账户信息后，我们就发一封邮件高兴一下
        # utils.send_email(user_form.email.data, '你激活了', body='你已经成功注册了账号，同时完成了发送邮件功能！')
        # 跳转登录页面
        return jsonify(code_msg.REGISTER_SUCCESS.put('action', url_for('user.login')))
    ver_code = utils.gen_verify_num()
    return render_template('user/reg.html', ver_code=ver_code['question'], form=user_form)


