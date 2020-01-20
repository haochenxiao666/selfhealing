#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import redis
from ansible_api import *
from link import DbSearch
import datetime
import time
from RemoteDispatch import *
from SelfHealing import SelfHealing


#alert 队列
alert_list = redis.StrictRedis(host='127.0.0.1',port=6379,decode_responses=True,db=0)
#连接redis
rc = redis.Redis(host='127.0.0.1', port=6379)

content = '如果队列中暂无元素,将休息3秒钟~~~'
logger.info(content)

while True:
	num = alert_list.llen('alert')
	if num == 0:
		time.sleep(3)
	else:
		comment = '队列中元素个数是%s,开始消费~~~'%(str(num))
		logger.info(comment)
		task = alert_list.brpop('alert',1)
		msg = task[1]
		logger.info('消费者端获取到的元素是%s'%str(task))

		msglist = msg.split('\n')
		ip = [ m for m in msglist if 'IP' in m ][0].split(':')[1].strip()
		hostname = [ m for m in msglist if '主机' in m ][0].split(':')[1].strip()

		alertpj = [ m for m in msglist if '告警项目' in m ][0].split(':')[1].strip()
		#logger.info('source is %s'%alertpj)

		status = [ m for m in msglist if '当前状态' in m ][0].split(':')[1].strip()

		#IP
		rc.hsetnx(hostname,'IP', ip)

		if status == 'OK':
			alert = json.dumps({"alertime":0,"fixtime":0})
			rc.hset(hostname,alertpj,alert)
			#告警信息记录
			alertmsg = '本次告警恢复 IP:%s, HOSTNAME: %s,告警项目: %s, 告警状态: %s'%(ip,hostname,alertpj,status)
			logger.info(alertmsg)
		else:

			#通过报警项目报警次数去做处理
			if rc.hexists(hostname,alertpj):
				alert = rc.hget(hostname,alertpj)
				alert = json.loads(alert)
				alertime = alert['alertime']
				fixtime = int(alert['fixtime'])
				alertime = int(alertime) + 1
				alert['alertime']=alertime

				##判断告警次数处理逻辑
				if SelfHealing.has_key(alertpj):
					switchtime = SelfHealing[alertpj]['time']
					switchcmd = SelfHealing[alertpj]['cmd']
					maxfixtime = SelfHealing[alertpj]['fixtime']
				else:
					continue

				if alertime >= switchtime:

					if fixtime <= maxfixtime:
						#获取资产信息
						db = DbSearch()
						asset = [db.GetOneHostMessage(ip,hostname)]
						result = RemoteDispatch(asset,switchcmd)
						if result == 0:
							alert = json.dumps({"alertime":0,"fixtime":0})
							rc.hset(hostname,alertpj,alert)
							continue

						#告警信息记录
						selfhealingmes = 'IP:%s, HOSTNAME: %s,告警项目: %s, 告警状态: %s, 告警次数: %s,自愈次数: %s 小于等于最大设定值 %s 将继续尝试修复'%(ip,hostname,alertpj,status,alertime,fixtime,maxfixtime)
						logger.info(selfhealingmes)

						fixtime += 1
						alert['fixtime']= fixtime
						rc.hset(hostname,alertpj,json.dumps(alert))

					else:
						selfhealingmes = 'IP:%s, HOSTNAME: %s,告警项目: %s, 告警状态: %s, 告警次数: %s,自愈次数: %s 大于设定值 %s 不做处理'%(ip,hostname,alertpj,status,alertime,fixtime,maxfixtime)
						logger.info(selfhealingmes)

						fixtime += 1
						alert['fixtime']= fixtime
						rc.hset(hostname,alertpj,json.dumps(alert))


				else:
					rc.hset(hostname,alertpj,json.dumps(alert))
					#告警信息记录
					alertmsg = '本次告警信息是 IP:%s, HOSTNAME: %s,告警项目: %s, 告警状态: %s, 告警次数: %s'%(ip,hostname,alertpj,status,alertime)
					logger.info(alertmsg)

			else:
				alert = json.dumps({"alertime":1,"fixtime":0})
				rc.hset(hostname,alertpj,alert)
				alertime = 1
				fixtime = 0

				#告警信息记录
				alertmsg = '首次创建告警信息是 IP:%s, HOSTNAME: %s,告警项目: %s, 告警状态: %s, 告警次数: %s'%(ip,hostname,alertpj,status,alertime)
				logger.info(alertmsg)