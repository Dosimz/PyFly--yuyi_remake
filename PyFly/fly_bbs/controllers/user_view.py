from fly_bbs.extensions import mongo
import json
# import datetime
# from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect

from fly_bbs.models import User
from fly_bbs import utils, forms

user_view = Blueprint('user', __name__)

# @user_view.route('/')
# def home():
#     users = mongo.db.users.find()
#     print(type(users))
#     l = [i for i in users]
#     print(l)
#     return json.dumps(l, cls=JSONEncoder)


@user_view.route('/login/', methods=['GET','POST'])
def login():
    #l = request.values
    #one_email = request.form.get('email')
    #form = request.form
    #res = request.get_json()
    #files = request.files

    #print(l)
    #print(form)
    #print(res)
    #print(request.files)
    #print(type(one_email), end='')
    #print(one_email)
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
    return render_template('user/login.html', ver_code=ver_code['question'])

@user_view.route('/register/')
def register():
    return render_template('user/reg.html')


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         elif isinstance(o, datetime.datetime):

#             return o.isoformat()
#         return json.JSONEncoder.default(self, o)
