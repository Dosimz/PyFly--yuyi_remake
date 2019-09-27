from flask import Flask
from fly_bbs.config import  config
from fly_bbs.controllers import config_blueprint
from fly_bbs.install_init import init as install_init
from fly_bbs.extensions import init_extensions

def create_app(config_name):
    app = Flask(__name__)
    # 使用 seission 必须配置
    app.config['SECRET_KEY'] = 'PyFly123'
    app.config.from_object(config[config_name])
    config_blueprint(app)
    init_extensions(app)
    with app.app_context():
        install_init()
    return app

