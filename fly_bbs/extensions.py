from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
# 从 models 文件里引入 User 类
from fly_bbs.models import User
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from flask_admin import Admin
from fly_bbs.admin import admin_view
from flask_mail import Mail

from fly_bbs.plugins import WhooshSearcher
from whoosh.fields import Schema, TEXT, ID, DATETIME

whoosh_searcher = WhooshSearcher()
from jieba.analyse import ChineseAnalyzer

admin = Admin(name='PyFly 后台管理系统')

mail = Mail()
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
    mail.init_app(app)
    mongo.init_app(app)
    # 在 Flask 应用里初始化
    login_manager.init_app(app)
    # 获取配置信息并存储在 app 上
    configure_uploads(app, upload_photos)
    # 将 admin 对象注册到 app 上
    admin.init_app(app)

    whoosh_searcher.init_app(app)

    with app.app_context():
        # 添加flask-admin视图
        admin.add_view(admin_view.UsersModelView(mongo.db['users'], '用户管理'))
        admin.add_view(admin_view.CatalogsModelView(mongo.db['catalogs'], '栏目管理', category='内容管理'))
        admin.add_view(admin_view.PostsModelView(mongo.db['posts'], '帖子管理', category='内容管理'))
        admin.add_view(admin_view.PassagewaysModelView(mongo.db['passageways'], '温馨通道', category='推广管理'))
        admin.add_view(admin_view.FriendLinksModelView(mongo.db['friend_links'], '友链管理', category='推广管理'))
        admin.add_view(admin_view.PagesModelView(mongo.db['pages'], '页面管理', category='推广管理'))
        admin.add_view(admin_view.FooterLinksModelView(mongo.db['footer_links'], '底部链接', category='推广管理'))
        admin.add_view(admin_view.AdsModelView(mongo.db['ads'], '广告管理', category='推广管理'))
        admin.add_view(admin_view.OptionsModelView(mongo.db['options'], '系统设置'))

        # 使用 jieba 中文分词
        chinese_analyzer = ChineseAnalyzer()
        # 建立索引模式对象
        post_schema = Schema(obj_id=ID(unique=True, stored=True), title=TEXT(stored=True, analyzer=chinese_analyzer)
                                , content=TEXT(stored=True, analyzer=chinese_analyzer), create_at=DATETIME(stored=True)
                                , catalog_id=ID(stored=True), user_id=ID(stored=True))
        whoosh_searcher.add_index('posts', post_schema)