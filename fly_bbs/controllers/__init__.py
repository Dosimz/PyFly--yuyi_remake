from .bbs_front import bbs_index
from .user_view import user_view
from .post_collection import post_collection
from .api_view import api_view

# 蓝本默认配置
DEFAULT_BLUEPRINT = (
    (bbs_index, ''),
    (user_view, '/user'),
    (post_collection, '/collection'),
    (api_view, '/api'),
)

def config_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
