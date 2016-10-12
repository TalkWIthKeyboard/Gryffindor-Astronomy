from app.models.config import Config
import app.core.tools as variable
from flask_mongoengine import MongoEngine
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, static_url_path='')
app.config.from_object(Config())
app.secret_key = 'taskProject'
db = MongoEngine(app)
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view='admin_login'

from app.models.adminModel import User
from app.routes import taskManageRoute
from app.routes import logRoute
from app.routes import adminRoute


@loginManager.user_loader
def load_user(id):
    if str(id) == 'None':
        return None
    return User.objects(myid=int(id)).first()