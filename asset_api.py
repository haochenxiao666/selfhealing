# coding: utf-8
from __future__ import division
import xlrd
import xlsxwriter
import datetime
import traceback
import logging
import os

#日志记录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = BASE_DIR + '/logs/top50purchase.log'
if 1 == 1:
	fh = logging.FileHandler(log_dir,encoding='utf-8') #创建一个文件流并设置编码utf8
	logger = logging.getLogger() #获得一个logger对象，默认是root
	logger.setLevel(logging.DEBUG)  #设置最低等级debug
	fm = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')  #设置日志格式
	logger.addHandler(fh) #把文件流添加进来，流向写入到文件
	fh.setFormatter(fm) #把文件流添加写入格式



def write_excel_detailstoremessage(asset_find,user,strtime):
	try:
		data = asset_find
		#print len(data)
		logger.info(len(data))
		#now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
		file_name = 'scm_%s_%s'%(user,strtime) + '.xlsx'
		workbook = xlsxwriter.Workbook('static/files/excels/SubFileWay/%s' %file_name)
		worksheet = workbook.add_worksheet(u'客户需求查询')
		worksheet.set_first_sheet()
		worksheet.set_column('A:P', 15)

		#title = [u'客户名称', u'新增门店名称','门店ID','门店创建时间','开始使用日期','开店日期','续费日期','状态','类型','品牌','所在城市']
		title = ['客户查询信息报表']
		format = workbook.add_format()
		format.set_border(1)
		format.set_align('center')
		format.set_align('vcenter')
		format.set_text_wrap()

		format_title = workbook.add_format()
		format_title.set_border(1)
		format_title.set_bg_color('#cccccc')
		format_title.set_align('center')
		format_title.set_bold()

		format_ave = workbook.add_format()
		format_ave.set_border(1)
		format_ave.set_num_format('0.00')

		worksheet.write_row('A1', title, format_title)
		i = 2
		for m in data:
			logger.info(m)
			location = 'A' + str(i)
			worksheet.write_row(location, m, format)
			i += 1

		workbook.close()
		ret = (True, file_name)
		return ret
	except Exception as e:
		logger.info(e)