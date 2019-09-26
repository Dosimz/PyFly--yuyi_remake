from .user_view import user_view

def config_blueprint(app):
    app.register_blueprint(user_view, url_prefix='/user')
