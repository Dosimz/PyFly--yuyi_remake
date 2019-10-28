from fly_bbs.extensions import mongo
from bson import ObjectId
import json
import datetime

from flask import Blueprint

# ????????????
user_view = Blueprint('user', __name__)

@user_view.route('/')
def home():
    users = mongo.db.users.find()
    print(type(users))
    l = [i for i in users]
    return json.dumps(l, cls=JSONEncoder)

class JSONEncoder(json.JSONEncoder):
   def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
