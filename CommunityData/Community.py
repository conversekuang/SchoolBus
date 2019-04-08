# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-04-01 16:38:18
# @Last Modified by:   dell
# @Last Modified time: 2019-04-03 13:57:56


import requests
from lxml import etree
import codecs
import csv
import os
from time import sleep
headers = {
	"User-agent":"User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"
}

def download_page():
	search_dict = {"nanhu":8,"xiuzhou":4}
	for loc, page_num in search_dict.items():
		for num in range(1,page_num):
			url = "https://www.anjuke.com/jx/cm/%s/p%d"%(loc, num)
			print url
			try:
				response = requests.get(url, headers =headers)
				if response.status_code == 200:
					yield (loc, response.text)
					sleep(0.5)
				else:
					print "Download Failed"
			except requests.HTTPError as e:
				if hasattr(e, reason):
					print e.reason
			

def writetocsv(filename, col ,res):
	if os.path.exists(filename) == False:
		with open(filename,'wb+') as f:
			f.write(codecs.BOM_UTF8)
			# f.writeheader()
			fieldnames = [col]
			print fieldnames
			w = csv.DictWriter(f,fieldnames = fieldnames)#,
			w.writeheader()
			for item in res:
				item_res = {col:item.encode('utf8')}
				print item_res
				w.writerow(item_res)
	else:
		with open(filename,'ab+') as f:
			f.write(codecs.BOM_UTF8)
			# f.writeheader()
			fieldnames = [col]
			print fieldnames
			w = csv.DictWriter(f,fieldnames = fieldnames)#,
			for item in res:
				item_res = {col:item}
				print item_res
				w.writerow(item_res)

def writetotext(content):
	with open('community','w') as f:
		f.write(content)

	

def parse_page(content):
	parse_content = etree.HTML(content)
	arrays = parse_content.xpath('//ul[@class="P3"][1]/li/em/a/text()')
	# print arrays
	return arrays


if __name__ == '__main__':
	for loc, content in download_page():
	# content = open('src.html','r').read()
		res = parse_page(content)
		writetotext(res)

		#print loc+'.csv', loc
		# print type(loc),type(res)
		# writetocsv(loc+'.csv', loc ,res)
