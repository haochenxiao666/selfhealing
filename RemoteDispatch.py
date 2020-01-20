#!/usr/bin/python
# ~*~ coding: utf-8 ~*~


import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')

from ansible_api import *
from Log import get_logger
from DingDing import SendMs
from RemoteDispatch import *
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#日志
logger = get_logger("selfhealing.log")

def RemoteDispatch(assets,cmd):

	results = ansible_shell(assets,cmd)
	for (hostname,result) in results['contacted'].items():

		if result['stdout'] != '':
			mes = '%s 的自愈信息是%s'%(hostname,result['stdout'])
			logger.info(mes)
			SendMs(hostname,mes)
			return 0

	for (hostname, result) in results['dark'].items():
		if result['stderr'] != '':
			mes = '%s 的自愈信息是%s'%(hostname,result['stderr'])
			logger.info(mes)
			SendMs(hostname,mes)
			return 1

	for (hostname,result) in results['contacted'].items():
		mes = '%s 的自愈信息是%s'%(hostname,result)
		logger.info(mes)
		SendMs(hostname,mes)
		return 1
