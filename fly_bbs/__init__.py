from flask import Flask
from fly_bbs.config import config
from fly_bbs.controllers import config_blueprint
from fly_bbs.extensions import init_extensions
from fly_bbs.install_init import init as install_init
from fly_bbs.custom_functions import init_func
from fly_bbs import flask_objectid_converter

def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PyFLy123'
    app.url_map.converters['ObjectId'] = flask_objectid_converter.ObjectIDConverter
    app.config.from_object(config[config_name])
    config_blueprint(app)
    init_extensions(app)
    init_func(app)
    with app.app_context():
        install_init()


    # app.url_map.conv    app.url_map.converters['objectid'] = flask_objectid_converter.ObjectIDConvertererters['objectid'] = flask_objectid_converter.Base64ObjectIDConverter
    return app
