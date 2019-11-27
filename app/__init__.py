import logging
import datetime
import sys
from os import environ
from flask import Flask, session, render_template
from flask_login import LoginManager 
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def create_app():
	app = Flask(__name__)
	CORS(app)
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
	app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	migrate = Migrate(app, db)
	from .models import User
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.session_protection = "strong"
	login_manager.login_message = u"Требуется авторизация"
	login_manager.login_message_category = "info"
	login_manager.init_app(app)

	with app.app_context():
		@app.errorhandler(404)
		def error_404(e):
			data = render_template('error.html', message = 'Страница не найдена')
			return (data, 404)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

