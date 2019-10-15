from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
from fly_bbs.models import User
# import pymongo

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return User(u)

def init_extensions(app):
    mongo.init_app(app)
    login_manager.init_app(app)
