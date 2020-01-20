#!/usr/bin/python
#coding=utf-8
import sys,os
import json,urllib2

import ConfigParser
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#参数
config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'db.conf'))

DingURL1 = config.get('DingURL','DingURL1')
DingURL2 = config.get('DingURL','DingURL2')

def SendMs(host,msg):

	if host.find('duofuwu') != -1 or host.find('多服务') != -1:
		url = DingURL1
	else:
		url = DingURL2

	textmod={"msgtype": "text", "text": {"content": '%s'%msg}}
	textmod = json.dumps(textmod)
	print(textmod)
	header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
	req = urllib2.Request(url=url,data=textmod,headers=header_dict)
	res = urllib2.urlopen(req)
	res = res.read()
	print(res)




