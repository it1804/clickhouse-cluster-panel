from clickhouse_driver import Client
from . import logger
import json


class Click:
	def __init__(self,nodes,user,password):
		self.nodes = nodes
		self.user = user
		self.password = password

	def get_databases(self):
		database = {}
		nodes = sorted(self.nodes)
		for node in nodes:
			client = Client(host=node,port=9000,user=self.user,password=self.password)
			ret = client.execute('SHOW databases')
			ret = [x for xs in ret for x in xs if x != 'system'] # Фильтруем системную
			for row in ret:
				if not database.get(row):
					database[row] = {"nodes": [node]}
				else:
					database[row]["nodes"].append(node)
		return {"nodes": nodes,"databases":database};


	def get_tables(self,database):
		tables = {}
		nodes = sorted(self.nodes)
		for node in nodes:
			t = {}
			client = Client(host=node,port=9000,user=self.user,password=self.password)
			ret = client.execute('select name,engine,create_table_query from system.tables where database = %(database)s', {'database':database})
			for row in ret:
				t = {"engine":row[1],"create_table_query":row[2]}
				if not tables.get(row[0]):
					tables[row[0]]={"nodes": {node: t }}
				else:
					tables[row[0]]["nodes"][node]=t
		return {"nodes": nodes,"tables":tables,"database":database}


	def get_table_info(self,node,database,table):
		nodes = sorted(self.nodes)
		if node not in nodes:
			return {"error":"invalid node name"}
		client = Client(host=node,port=9000,user=self.user,password=self.password)
		ret = client.execute('select name,engine,engine_full,create_table_query from system.tables where database = %(database)s and name=%(table)s', {'database':database, 'table': table})
		if not len(ret):
			return {"error":"invalid data"}
		row=ret[0]
		return {"table":row[0],"engine":row[1],"engine_full":row[2],"create_table_query":row[3],"table":table,"database":database,"node":node}
