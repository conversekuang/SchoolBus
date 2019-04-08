# -*- coding: utf-8 -*-
# @Author: converse
# @Date:   2019-03-11 15:29:52
# @Last Modified by:   dell
# @Last Modified time: 2019-04-02 13:58:19


import pymysql
import pandas as pd
from sqlalchemy import create_engine
import codecs
import re
import json
import requests

conn = pymysql.connect(host="localhost",
					   user = "root",
					   password = 'password',
					   db = "survey",
					   charset='utf8',
					   )
cursor = conn.cursor()

	
def fileWriteToDB(filename,renames):
	df = pd.read_csv(filename)
	df.rename(columns = renames,inplace=True)
	engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('root', 'password', '127.0.0.1:3306', 'survey','utf8'))
	con = engine.connect()#创建连接
	df.to_sql(name='survey_data', con=con, if_exists='replace', index=False)


def fileWriteToCSV(filename,renames):
	df = pd.read_excel(filename)
	df.rename(columns = renames,inplace=True)
	
	#csv 需要写文件头，否则乱码
	f = open('renames.csv','wb+')
	f.write(codecs.BOM_UTF8)
	df.to_csv(f, header=True, index=False, encoding='utf-8')



def columnsRenames():
	old= ["序号","提交答卷时间","所用时间","来源","来源详情","来自IP","1、您的孩子所在学校","2、您孩子所在年级",
	"3、您平时接送孩子上下学的交通工具","4、家庭常住地址(定位到小区即可):","经纬度","5、(乘车不安全)","5、(换乘次数多)",
	"5、(乘坐时间长)","5、(其他)","6、您孩子是否住校？","7、(早上上学)","7、(晚自习放学)","7、(周五放学)","7、(周日返校)",
	"8、根据常住地址，辅助公交优先考虑在小区门口停靠，此外，能否接受您的孩子在小区附近的公交站点进行上下车 ？",
	"9、当您孩子选择乘坐辅助公交上下学，能否接受无座的情况","10、在辅助公交方式上下学过程中，您孩子可接受的最长乘坐时间是多久？",
	"11、您最大可接受孩子从家到辅助公交乘车点的步行时间是","12、当选择辅助公交上下学，您能否接受辅助公交票价略高于常规公交票价？",
	"13、您能接受的最高票价是多少元？（请综合时间成本、乘坐舒适度等因素）","14、您接受辅助公交车票的购买周期？","15、(运行时间)",
	"15、(乘坐安全)","15、(车辆票价)","15、(乘坐舒适度)","15、(步行距离)",
	"16、您对辅助公交还有哪些宝贵意见或建议？（可从乘车安全、乘车舒适度、车票定价等多方面进行考虑）",
	"17、若开通辅助公交线路能够满足您孩子的上学需求，您是否愿意让孩子乘坐？（此项意见情况将对辅助公交开通有重要影响，请认真填写）"]

	new = ['id','SubmitTime','TimeConsumption', 'Source', 'DetailSource','IP', 'School','Grade','Transportation',
	'HomeLocation',"Location",'UnsafetyByBus', 'MultiChangeByBus','LongRideByBus','OtherReasons','BoardingSchool', 
	'DayBus','NightBus', 'FridayBus','WeekendBus', 'ParkNearStation','AccpetableNoSeat', 'AcceptableRidingTime',
	'AcceptableWalkingTime', 'AcceptableHigherTicket',  'HighestTicket','BuyTicketPeriod', 'RidingTimeConsideration', 
	'SafetyConsideration','TicketPriceConsideration', 'ComfortConsideration','WakingDisConsideration','Suggestions','WillingToTakeBus']

	array = []
	for i in old:
		array.append(i.decode('utf-8'))
	renames = dict(zip(array, new))

	return renames




def addColumn(file):
	pattern = re.compile('\[(.*)\]')
	array = []


	df = pd.read_csv(file)
	print df.shape

	col_name=df.columns.tolist()         # 将数据框的列名全部提取出来存放在列表里
	print(col_name)

	col_name.insert(10,'Location')    	 # 在列索引为2的位置插入一列,列名为:city，刚插入时不会有值，整列都是NaN
	df=df.reindex(columns=col_name)      # DataFrame.reindex() 对原行/列索引重新构建索引值
	print df.shape



	for geo in df['HomeLocation']:
		res = re.search(pattern, geo)
		if res != None:									   #正则匹配提取结果
			loc = str(res.groups(1)[0])					   #提取str
			# print geo, res, loc
		else:
			loc = getMissingLocation(geo.decode('utf-8'))  #有遗漏的情况下，根据地址请求坐标
		array.append(loc)
	df['Location'] = array
	print df.shape

	#讲修改后的df重新写到新文件
	f = open('finally.csv','wb+')
	f.write(codecs.BOM_UTF8)
	df.to_csv(f, header=True, index=False, encoding='utf-8')





def getMissingLocation(geo):
	baseurl = "http://restapi.amap.com/v3/geocode/geo?"
	key = "226b378736e355d63444903944631390"
	url = baseurl +"key="+key+"&address=" + geo +"&city="+u"嘉兴市"

	try:
		res = requests.get(url)
		if res.status_code == 200:
			res_dict = json.loads(res.text)
			res_geo = res_dict["geocodes"][0]
			location = res_geo['location']
			return location
		else:
			print "DownLoad Problem url is %s" % url
	except requests.HTTPError as e:
		if hasattr(e,reason):
			print e.reson
		else:
			print "UnKown Problem"

if __name__ == '__main__':

	# 1 修改中文到英文
	filename ='data.xls'  
	renames = columnsRenames()
	fileWriteToCSV(filename,renames)

	#2 添加location列并且写回文件
	file = "renames.csv"
	addColumn(file)
	

	#3可以导出到 Mysql当中
	filename = "finally.csv"
	# renames = columnsRenames()
	fileWriteToDB(filename, renames)
	# fileWriteToCSV(filename,renames)

	