from fly_bbs.extensions import mongo
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

def init():
    # ???????? 'installed.lock' ?????
    lock_file = os.path.join(os.getcwd(), 'installed.lock')
    # ?????????????????????
    if os.path.exists(lock_file):
        return

    # ???????
    mongo.db.users.insert_one({
        'email': 'admin',
        'username': 'admin',
        'password': generate_password_hash('admin'),
        'is_admin': True,
        'renzheng': '社区超级管理员',
        'vip': 5,
        'coin': 99999,
        'avatar': '/static/images/avatar/1.jpg',
        'is_active': True,
        'create_at': datetime.utcnow(),
    })


    options = [
        {
            'name': '网站标题',
            'code': 'title',
            'val': 'PyFly'
        },
        {
            'name': '网站描述',
            'code': 'description',
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
            'name': '签到奖励区间（格式: 1-100）',
            'code': 'sign_interval',
            'val': '1-100'
        },
        {
            'name': '开启用户注册（0关闭，1开启)',
            'code': 'open_user',
            'val': '1'
        },
        {
            'name': '管理员邮箱',
            'code': 'email',
            'val': '981764793@qq.com'
        },
        {
            'name': '底部信息(支持 html 代码)',
            'code': 'footer',
            'val': 'Power by PyFly'
        },
    ]
    result = mongo.db.options.insert_many(options)

    # ?????????? options ?????? lock_file ??
    if len(result.inserted_ids) > 0:
        with open(lock_file, 'w') as file:
            file.write('1')
