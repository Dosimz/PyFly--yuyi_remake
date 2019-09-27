from fly_bbs.extensions import mongo
import json
import datetime
from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify

from fly_bbs.models import User

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
    if bool(request) and request.method == 'POST':
        print('登录成功了为什么不返回JSON???000000000000000')
        email_form = request.form.get('email')
        pwd_form = request.form.get('password')
        user = mongo.db.users.find_one({'email': email_form})
        print('登录成功了为什么不返回JSON???111111111111111111')
        if not user:
            return jsonify({'status': 50102, 'msg': '用户不存在'})
        if not User.validate_login(user['password'], pwd_form):
            return jsonify({'status': 'Error', 'msg': '密码错误'})
        print('登录成功了为什么不返回JSON???2222222222222222')
        return jsonify({'status': 200, 'msg': '登录成功了啊'})

    return render_template('user/login.html')

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
