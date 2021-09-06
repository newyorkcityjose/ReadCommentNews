import os
from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from newsapi import NewsApiClient
from init_app.models import User, db, connect_db
from init_app.local_settings import DATABASE, API
app = Flask(__name__)

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
newsapi = NewsApiClient(api_key=API)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE', DATABASE))

# import urllib.parse as up
# import psycopg2

# up.uses_netloc.append("postgres")
# url = up.urlparse(os.environ["DATABASE_URL"])
# conn = psycopg2.connect(database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

toolbar = DebugToolbarExtension(app)
connect_db(app)

from init_app.users.views import users
from init_app.bookmark.views import bookmark
from init_app.mailbox.views import mailbox 

app.register_blueprint(users)
app.register_blueprint(bookmark)
app.register_blueprint(mailbox)