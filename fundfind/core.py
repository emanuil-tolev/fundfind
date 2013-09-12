import os
from flask import Flask
from flask.ext.login import LoginManager, current_user

from fundfind import default_settings

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    configure_app(app)
    add_jinja_globals(app)
    setup_error_email(app)
    login_manager.setup_app(app)
    return app

def configure_app(app):
    app.config.from_object(default_settings)
    # parent directory
    here = os.path.dirname(os.path.abspath( __file__ ))
    config_path = os.path.join(os.path.dirname(here), 'app.cfg')
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)

def setup_error_email(app):
    ADMINS = app.config.get('ADMINS', '')
    if not app.debug and ADMINS:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@no-reply.com',
                                   ADMINS, 'FundFind error')
        mail_handler.setLevel(logging.error)
        app.logger.addHandler(mail_handler)

def add_jinja_globals(app):
    add_to_globals = {
        'isinstance': isinstance,
        'list': list,
        'dict': dict
    }
    app.jinja_env.globals.update(**add_to_globals)

app = create_app()
