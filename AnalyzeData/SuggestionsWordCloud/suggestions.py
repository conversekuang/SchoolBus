# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-03-26 14:21:42
# @Last Modified by:   dell
# @Last Modified time: 2019-03-27 10:10:56


import pymysql
from wordcloud import WordCloud 
import matplotlib as plt
import jieba 
def get_res():
	connection = pymysql.connect(host='localhost',
	                             user='root',
	                             password='password',
	                             db='survey',
	                             charset='utf8',
	                            )
	cursor = connection.cursor()

	f = open("Suggestions.txt","w+")

	sql = "SELECT Suggestions from survey_data WHERE Suggestions not like '%无' and Suggestions not like '%(空)'and Suggestions not like '%没有'"
	affected_rows = cursor.execute(sql)
	print "总共有%d表达了自己的意见" % affected_rows
	
	# print type(cursor.fetchone())
	# print cursor.fetchone()[0]
	for each in cursor.fetchall():
		f.write(each[0].encode('utf-8'))
		f.write('\n')



def analyze_suggestions_1():
	fontpath='SourceHanSansCN-Regular.otf'

	content = open('Suggestions.txt','r').read()


	# 分词
	words = jieba.lcut(content)
	
	cuted_words = ' '.join(words)
	#print cuted_words

	wc = WordCloud(font_path=fontpath,  # 设置字体
	               background_color="white",  # 背景颜色
	               max_words=1000,  # 词云显示的最大词数
	               max_font_size=500,  # 字体最大值
	               min_font_size=20, #字体最小值
	               random_state=42, #随机数
	               collocations=True, #避免重复单词
	               width=1600,height=1200,margin=10, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
	              )
	wc.generate(cuted_words)  
	# print f
	# wc = WordCloud()
	# wc.generate(cuted_words)
	wc.to_file('./0.jpg')


	# for line in f.readlines():
	# 	print line 
	



def analyze_suggestions_2():
	fontpath='SourceHanSansCN-Regular.otf'

	content = open('Suggestions.txt','r').read()


	#移除
	removes = ['最好','考虑','可以','孩子','不能','不要','希望','主要','离家近','学生']
	for rm in removes:
		jieba.del_word(rm)

	#添加
	adds = ['安全第一','确保安全','运行时间太长','减少时间','减少换乘','缩短时间','等车时间'
	'固定线路','固定班次','准时','时间不要太长','步行距离短','准点','票价合理','公交车站','公交站台','站点','小区门口','附近']
	for add in adds:
		jieba.add_word(add)

	words = jieba.cut(content, cut_all=False)
	#print("Default Mode: " + "/ ".join(words))  # 精确模式
	
	cuted_words = ' '.join(words)
	print cuted_words

	wc = WordCloud(font_path=fontpath,  # 设置字体
	               background_color="white",  # 背景颜色
	               max_words=120,  # 词云显示的最大词数
	               max_font_size=500,  # 字体最大值
	               min_font_size=20, #字体最小值
	               random_state=42, #随机数
	               collocations=True, #避免重复单词
	               width=1600,height=1200,margin=10, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
	              )
	wc.generate(cuted_words)  
	# print f
	# wc = WordCloud()
	# wc.generate(cuted_words)
	wc.to_file('./2.jpg')


	# for line in f.readlines():
	# 	print line 




if __name__ == '__main__':
	#get_res()
	analyze_suggestions_2()

