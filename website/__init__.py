from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.csrf import CSRFProtect
import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#import requests
import pathlib
from flask import Flask, session, abort, redirect, request
import os
from pip._vendor import cachecontrol
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database():
    db.create_all()
    print('Database Created')


def validateLicenseKey():
     print("a")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "udfhçgkufyıvökçlı.hşp.gub.vkhcjdthxfndgtzhseajmswkmeıötgçloıdfykgctjkxhy"
    csrf = CSRFProtect(app)
    #limiter = Limiter(get_remote_address, app=app)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    GOOGLE_CLIENT_ID = "1087409452458-8asgv2ur8664id8te1uijrh523turdv4.apps.googleusercontent.com"
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order, Settings

    app.register_blueprint(views, url_prefix='/') # localhost:5000/about-us
    app.register_blueprint(auth, url_prefix='/') # localhost:5000/auth/change-password
    app.register_blueprint(admin, url_prefix='/')

    # with app.app_context():
    #     create_database()

    return app

