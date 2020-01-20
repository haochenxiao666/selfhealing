#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import MySQLdb
import re
import os 
import ConfigParser
#
#BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#参数
config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'db.conf'))

db = config.get('dbconfig','db')
host = config.get('dbconfig','host')
user = config.get('dbconfig','user')
passwd = config.get('dbconfig','passwd')
charset = config.get('dbconfig','charset')
timeout = int(config.get('dbconfig','timeout'))


class DbSearch():
	def __init__(self,db=db,host=host,user=user,passwd=passwd,charset=charset,timeout=timeout):
		self.db = db
		self.host = host
		self.user = user
		self.passwd = passwd
		self.charset = charset
		self.timeout = timeout
		
		self.con = MySQLdb.connect(db=self.db,host=self.host,user=self.user,
									passwd=self.passwd,charset=self.charset,
									connect_timeout=self.timeout)
		self.cursor = self.con.cursor()

		
	def GetOneHostMessage(self,ip,hostname):

		sql = 'select a.ip,a.port,a.hostname from jasset_asset a where \
				a.ip = "{0}" and a.hostname = "{1}"'.format(ip,hostname)
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			try:

				ip = row[0].strip()
				port = int(row[1])
				hostname = row[2]
				pp = ip + ':' + str(port)
				asset = {
					"hostname": hostname,
					"ip": ip,
					"port": port,
					"username": "root",
					#"private_key": BASE_DIR + "/autoops/keys/id_rsa",
					"private_key": BASE_DIR + "/keys/id_rsa",
					}
				return asset
			except:
				asset = {}
				return asset
	
	def close(self):
		self.cursor.close()
		self.con.close()
