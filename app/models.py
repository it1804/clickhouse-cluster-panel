from ldap3 import Server, ALL, Connection, NTLM, SUBTREE
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired
from flask_login import UserMixin
from .database import db
from os import environ

AUTH_SERVER = environ.get('LDAP_AD_SERVER')
AUTH_DOMAIN = environ.get('LDAP_AD_DOMAIN')
AUTH_PORT = environ.get('LDAP_AD_PORT')

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	login = db.Column(db.String(100), unique=True)
	name = db.Column(db.String(1000))

	@staticmethod
	def try_login(login, password):
		if not password or not login:
			return False
		usr = '{0}\\{1}'.format(AUTH_DOMAIN, login)
		srv = Server(AUTH_SERVER, get_info=ALL, port=int(AUTH_PORT))
		conn = Connection(srv, user=usr, password=password, authentication=NTLM)
		return conn.bind()

class LoginForm(FlaskForm):
	class Meta:
		csrf = False
	login = TextField('Логин', [InputRequired()])
	password = PasswordField('Пароль', [InputRequired()])
	submit = SubmitField('Вход')
