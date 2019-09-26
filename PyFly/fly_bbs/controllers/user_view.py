from fly_bbs.extensions import mongo
import json
import datetime
from bson import ObjectId
from flask import Blueprint, render_template

user_view = Blueprint('user', __name__)

# @user_view.route('/')
# def home():
#     users = mongo.db.users.find()
#     print(type(users))
#     l = [i for i in users]
#     print(l)
#     return json.dumps(l, cls=JSONEncoder)

@user_view.route('/')
def index():
    return render_template('base.html')


@user_view.route('/login/')
def login():
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
