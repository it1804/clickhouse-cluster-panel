from flask import Blueprint, render_template, session,request,jsonify
from flask_login import login_required, current_user
from . import logger
import json
from .click import Click

from os import environ


CLICKHOUSE_NODES = json.loads(environ.get('CLICKHOUSE_NODES'))
CLICKHOUSE_USER = environ.get('CLICKHOUSE_USER')
CLICKHOUSE_PASS = environ.get('CLICKHOUSE_PASSWORD')

main = Blueprint('main', __name__)

@main.route('/static/<path:path>', methods=['GET'])
def get_static(path):
	return send_from_directory('static', path)

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.login)


@main.route('/', methods=['GET'])
@login_required
def index():
	click = Click(CLICKHOUSE_NODES,CLICKHOUSE_USER,CLICKHOUSE_PASS)
	databases = click.get_databases()
	return render_template('index.html',databases=databases)


@main.route('/api/<database>/tables',methods=['GET'])
@login_required
def get_databases(database):
	click = Click(CLICKHOUSE_NODES,CLICKHOUSE_USER,CLICKHOUSE_PASS)
	tables = click.get_tables(database)
	return jsonify(tables)

@main.route('/api/<database>/<table>/detail', methods=['GET'])
@login_required
def get_table_info(database,table):
	node = request.args.get('node')
	click = Click(CLICKHOUSE_NODES,CLICKHOUSE_USER,CLICKHOUSE_PASS)
	info = click.get_table_info(node,database,table)
	return jsonify(info)

