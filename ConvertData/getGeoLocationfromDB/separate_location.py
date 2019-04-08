# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-03-26 13:33:06
# @Last Modified by:   dell
# @Last Modified time: 2019-03-26 13:36:36


import pymysql
import re
import csv
import os
import codecs

def get_location():
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='password',
	                             db='survey',
	                             charset='utf8',
	                            )#cursorclass = pymysql.cursors.DictCursor
	
	cursor = connection.cursor()	
	sql = "select HomeLocation from importbycode"
	res = cursor.execute(sql)
	info = cursor.fetchall()
	pattern = re.compile('\[(.*)\]')	
	dict_arrary = []
	for i in info:
		#print i[0]
		result = re.search(pattern, i[0])		
		#print result.groups()
		res = str(result.groups()[0])
		#print type(res)
		item = {'loc':res}
		dict_arrary.append(item)
	return dict_arrary



def writetocsv(items):
	filename = 'location.csv'
	with open(os.path.join(os.path.dirname(__file__), filename) ,'ab+') as f:
		fieldnames = ["loc"]
		f.write(codecs.BOM_UTF8)
		w = csv.DictWriter(f, fieldnames = fieldnames)
		w.writeheader()
		for item in items:
			w.writerow(item)

if __name__ == '__main__':
	res = get_location()
	writetocsv(res)