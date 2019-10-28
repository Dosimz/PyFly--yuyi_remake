from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
# 从 models 文件里引入 User 类
from fly_bbs.models import User

mongo = PyMongo()
# 创建 LoginManager 对象
login_manager = LoginManager()
# 配置作为登录页的视图函数
login_manager.login_view = 'user.login'

# 创建 load_user 函数
@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return User(u)

def init_extensions(app):
    mongo.init_app(app)
    # 在 Flask 应用里初始化
    login_manager.init_app(app)
