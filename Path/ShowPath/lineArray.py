# -*- coding: utf-8 -*-
# @Author: converse
# @Date:   2019-04-02 21:47:14
# @Last Modified by:   dell
# @Last Modified time: 2019-04-03 09:02:09
Array = []
f = open('F1.txt','r')
for line in f.readlines():
	if line != '\n':
		lng, lat = line.strip().split(',')
		Array.append([float(lng),float(lat)])

print Array