# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-04-03 14:30:51
# @Last Modified by:   dell
# @Last Modified time: 2019-04-04 11:27:05

import pymysql
import pandas as pd
from sqlalchemy import create_engine
import codecs
import re
import json
import requests
import os

def getnum(sql):
	conn = pymysql.connect(host="localhost",
						   user = "root",
						   password = 'password',
						   db = "survey",
						   charset='utf8',
						   )
	cursor = conn.cursor()
	res = cursor.execute(sql)    	#res只等于1 和 0，不能反悔affected rows
	return cursor.fetchone()[0]		#返回的是tuple，所以需要去出，count只返回一个结果，所以fetchone



def readcsv(filename):
	community_arr = []
	with open(filename,'r') as f:
		for line in f.readlines():
			line = line.strip()
			if line !='':
				community_arr.append(line)
	# print community_arr
	return community_arr


def writetocsv(filename,data):
	# data.rename(index=str, columns=rename_col,inplace=True)

	#csv 需要写文件头，否则乱码
	f = open(filename+'.csv','wb+')
	f.write(codecs.BOM_UTF8)
	data.to_csv(f, header=True, index=False, encoding='utf-8')


def analyze(filename,bustime):
	community_arr =  readcsv(filename)
	grade_arr = [str(i) for i in range(1,7)]	#1-6个年级
	dic = {}
	for grade in grade_arr:
		num_array =[]
		for community in community_arr:
			community = "'%"+community+"%'"		#组成like
			sql = 'SELECT count(*) FROM survey_data where Grade = %s and %s = 1 and WillingToTakeBus = 1 and HomeLocation like %s'%(grade,bustime, community)
			res =getnum(sql)
			num_array.append(res)
		dic[grade] = num_array

	data = pd.DataFrame.from_dict(dic)
	rename_col = dict(zip(grade_arr,[u"7年级",u"8年级",u"9年级",u"高一",u"高二",u"高三"]))

	data.rename(index=str, columns=rename_col,inplace=True)

	col_name=data.columns.tolist()       	 	# 将数据框的列名全部提取出来存放在列表里
	col_name.insert(0,u'小区')    	 			# 在列索引为2的位置插入一列,列名为:city，刚插入时不会有值，整列都是NaN
	data = data.reindex(columns=col_name)   	# DataFrame.reindex() 对原行/列索引重新构建索引值

	 
	community_arr_uni = []
	for community in community_arr:
		community_arr_uni.append(community.decode('utf8'))
	data[u'小区'] = community_arr_uni

	writetocsv(bustime+file.encode('utf-8').split('.')[0].decode('utf-8'),   data)


def get_files_in_dir():
	"""返回：当前文件夹下的含有txt格式的文件列表"""
	path =  os.path.dirname(__file__)
	files = []
	for dirpath,dirnames,filenames in os.walk(path):
		for filename in filenames:
			if '.txt' in filename:
				filename = filename.decode('gbk')
				files.append(filename)
	return files


if __name__ == '__main__':
	files = get_files_in_dir()  #线路方向的文件名列表
	times = [u'周内',u'周五']	#时间列表
	for file in files:
		for time in times:
			if time == u'周内':
				bustime = 'NightBus'
			else:
				bustime = 'FridayBus'
			analyze(file,bustime)	
	

	


