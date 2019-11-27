import datetime
from ldap3.core.exceptions import LDAPException
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, LoginForm
from . import logger
from .database import db


auth = Blueprint('auth', __name__)

def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/login', methods=['GET','POST'])
def login():
	next = request.args.get('next')
	form = LoginForm()
	if current_user.is_authenticated:	
		return redirect(url_for('main.profile'))
	if form.validate_on_submit():
		login = form.login.data
		password = form.password.data
		try:
			is_auth = User.try_login(login, password)
		except LDAPException:
			is_auth = False
		if not is_auth: 
			flash('Во время авторизации произошла ошибка','danger')
			return redirect(url_for('auth.login'))

		user = User.query.filter_by(login=login).first()
		if not user:
			user = User(login=login, name="Test User")
			db.session.add(user)
			db.session.commit()
		if login_user(user, remember=False):
			logger.debug("User %s successfully authorized" % (login))

		if next is not None:
			if not is_safe_url(next):
				return abort(400)
			return redirect(next)
		return redirect(url_for('main.index'))

	if form.errors:
		flash(form.errors, 'danger')
	return render_template('login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
