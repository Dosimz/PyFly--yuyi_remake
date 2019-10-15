from fly_bbs.extensions import mongo
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

def init():
    lock_file = os.path.join(os.getcwd(), 'installed.lock')
    if os.path.exists(lock_file):
        return

    options = [
        {
            'name': '网站标题',
            'code': 'title',
            'val': 'PyFly'
        },
        {
            'name': '网站描述',
            'code': 'desciption',
            'val': 'PyFly'
        },
        {
            'name': '网站关键字',
            'code': 'keywords',
            'val': 'PyFly'
        },
        {
            'name': '网站Logo',
            'code': 'logo',
            'val': '/static/images/logo.png'
        },
        {
            'name': '签到奖励(格式：1-100)',
            'code': 'sign_interval',
            'val': '1-100'
        },
        {
            'name': '开启用户注册(0: 开启; 1: 关闭)',
            'code': 'open_user',
            'val': '1'
        },
        {
            'name': '管理员邮箱（申请友链链接用到）',
            'code': 'email',
            'val': '981764793@qq.com'
        },
        {
            'name': '底部消息(支持html代码)',
            'code': 'footer',
            'val': 'Power by PyFly'
        },
    ]

    result = mongo.db.options.insert_many(options)

    mongo.db.users.insert_one({
        'email': 'admin',
        'username': 'admin',
        'password': generate_password_hash('admin'),
        'is_admin': True,
        'renzheng': 'SuperAdminStrongger',
        'vip': 5,
        'coin': 99999,
        'avatar': '/static/images/avatar/1.jpg',
        'is_active': True,
        'create_at': datetime.utcnow(),
        })

    catalogs = [{'name': '游戏'}, {'name': '音乐'}, {'name': '科技'}, {'name': '影视'}]
    mongo.db.catalogs.insert_many(catalogs)

    if len(result.inserted_ids) > 0:
        with open(lock_file, 'w') as file:
            file.write('1')
