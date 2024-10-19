import os

from flask import Flask
from flask_sock import Sock

sock = Sock()

from . import battle

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    TOKEN_DB = os.path.join(app.instance_path, 'token.db')
    #)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # socket
    sock.init_app(app)

    # importing configs
    from . import db
    db.init_app(app)

    # health
    from . import health
    app.register_blueprint(health.bp)

    # battle
    from . import battle
    battle.init_app(app)

    return app