#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')


#ansible 2.x 引用
from runner import AdHocRunner,PlayBookRunner
from callback import CommandResultCallback


def ansible_playbook(playbook,asset,vname):
	play = PlayBookRunner(assets, playbook_path=playbook, extra_vars = vname,forks=30)
	ret = play.run()
	return ret
	
def ansible_copy(assets,src,dest):
	args = "src=%s dest=%s owner=root group=root"%(src,dest)
	task_tuple = (('copy', args),) 
	hoc = AdHocRunner(hosts=assets,forks=10)
	hoc.results_callback = CommandResultCallback()
	ret = hoc.run(task_tuple)
	return ret

def ansible_shell(assets,args):
	task_tuple = (('shell', args),) 
	hoc = AdHocRunner(hosts=assets,forks=10)
	hoc.results_callback = CommandResultCallback()
	ret = hoc.run(task_tuple)
	return ret
	
def ansible_script(assets,args):
	task_tuple = (('script', args),) 
	hoc = AdHocRunner(hosts=assets,forks=10)
	hoc.results_callback = CommandResultCallback()
	ret = hoc.run(task_tuple)
	return ret

