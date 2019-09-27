from .user_view import user_view
from .bbs_front import bbs_index

DEFAULT_BLUEPRINT = (
        (bbs_index, '/'),
        (user_view, '/user')
        )

def config_blueprint(app):
    for blue_name, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_name, url_prefix=url_prefix)
