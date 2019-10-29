import os
from flask_uploads import ALL


class Dev:
    MONGO_URI = "mongodb://127.0.0.1:27017/pyfly"

    WTF_CSRF_ENABLED = False
    # 配置允许的扩展名
    UPLOADED_PHOTOS_ALLOW = ALL
    # 配置上传照片的目录
    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'uploads')
    # 配置上传文件的目录
    UPLOADED_FILES_DEST = os.path.join(os.getcwd(), 'uploads')

    # 邮箱配置信息
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'yuyi_201910@163.com'
    MAIL_PASSWORD = ''
    MAIL_DEBUG = True
    MAIL_SUBJECT_PREFIX = '[PyFly]-'

        WHOOSH_PATH = os.path.join(os.getcwd(), 'whoosh_indexes')


class Prod:
    pass

config = {
        "Dev": Dev,
        "Prod": Prod
        }


