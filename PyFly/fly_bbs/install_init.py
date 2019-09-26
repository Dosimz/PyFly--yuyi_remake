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
            'name': 'WebTitle',
            'code': 'title',
            'val': 'PyFly'
        },
        {
            'name': 'WebDST',
            'code': 'desciption',
            'val': 'PyFly'
        },
        {
            'name': 'WebKeywords',
            'code': 'keywords',
            'val': 'PyFly'
        },
        {
            'name': 'WebLogo',
            'code': 'logo',
            'val': '/static/images/logo.png'
        },
        {
            'name': 'Attendance(1-100)',
            'code': 'sign_interval',
            'val': '1-100'
        },
        {
            'name': 'BeginRegister(0:close; 1:open)',
            'code': 'open_user',
            'val': '1'
        },
        {
            'name': 'AdministongerEmail',
            'code': 'email',
            'val': '981764793@qq.com'
        },
        {
            'name': 'BottomMessages(support Html)',
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

    if len(result.inserted_ids) > 0:
        with open(lock_file, 'w') as file:
            file.write('1')
