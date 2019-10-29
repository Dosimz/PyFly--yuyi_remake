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

class Prod:
    pass

config = {
        "Dev": Dev,
        "Prod": Prod
        }


