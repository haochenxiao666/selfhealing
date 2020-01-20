#!/usr/bin/python
# ~*~ coding: utf-8 ~*~

#故障自愈报警项目字典数据
SelfHealing = {
			'memcached.ping':{'time':3,'fixtime':3,'cmd':'service memcached restart'},
			#'system.cpu.load':{'time':10,'fixtime':3,'cmd':'/opt/lampp/lampp restartapache'},
			'vfs.fs.size[/opt,pfree]':{'time':3,'fixtime':3,'cmd':"find /opt/lampp/logs -mtime +10 -name '*.txt' -exec /bin/rm -f {} \; && find /opt/lampp/logs -mtime +10 -name '*.log' -exec /bin/rm -f {} \;"},
			'proc.num[httpd,,]':{'time':2,'fixtime':3,'cmd':'/opt/lampp/lampp startapache'},
			'proc.num[supervisord]':{'time':2,'fixtime':3,'cmd':'supervisord -c /etc/supervisord.conf'},
			'mysql.ping':{'time':2,'fixtime':3,'cmd':'/opt/lampp/lampp startmysql'}
			  }

