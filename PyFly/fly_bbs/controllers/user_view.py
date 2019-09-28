from fly_bbs.extensions import mongo
import json
from datetime import datetime
# from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from random import randint
from fly_bbs.models import User
from fly_bbs import utils, forms
from werkzeug.security import generate_password_hash

user_view = Blueprint('user', __name__)


@user_view.route('/login/', methods=['GET','POST'])
def login():
#    SUBMIT_METHODS = set(('POST','))
#    print('登录成功了为什么不返回JSON???')
    # if request.method == 'POST':
    user_form = forms.LoginForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify({'status': 50001, 'msg': str(user_form.errors)})
        utils.verify_num(user_form.vercode.data)
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if not user:
            return jsonify({'status': 50102, 'msg': '用户不存在'})
        if not User.validate_login(user['password'], user_form.password.data):
            return jsonify({'status': 50000, 'msg': '密码错误'})
        session['username'] = user['username']
        return redirect(url_for('index.index'))
    ver_code = utils.gen_verify_num()
    return render_template('user/login.html', ver_code=ver_code['question'], form=user_form)


@user_view.route('/reg', methods=['GET', 'POST'])
def register():
    # 是否开放注册
    # if db_utils.get_option('open_user', {}).get('val') != '1':
    #     abort(404)
    user_form = forms.RegisterForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify({'status': 50001, 'msg': str(user_form.errors)})
        utils.verify_num(user_form.vercode.data)
        user = mongo.db.users.find_one({'email': user_form.email.data})
        if user:
            return jsonify({'status': 50000, 'msg': '用户已注册'})
        user = dict({
            'is_active': False,
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

        # send_active_email(user['username'], user['_id'], user['email'])
        # return jsonify(code_msg.REGISTER_SUCCESS.put('action', url_for('user.login')))
        return redirect(url_for('user.login'))
    ver_code = utils.gen_verify_num()
    # session['ver_code'] = ver_code['answer']
    return render_template('user/reg.html', ver_code=ver_code['question'], form=user_form)