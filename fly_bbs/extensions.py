from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
# 从 models 文件里引入 User 类
from fly_bbs.models import User
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL

mongo = PyMongo()
# 创建 LoginManager 对象
login_manager = LoginManager()
# 配置作为登录页的视图函数
login_manager.login_view = 'user.login'
# 实例化图片上传对象，extensions 参数代表允许扩展名
upload_photos = UploadSet(extensions=ALL)

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
    # 获取配置信息并存储在 app 上
    configure_uploads(app, upload_photos)

