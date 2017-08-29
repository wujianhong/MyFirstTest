#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time    : 2017/8/14 9:30
# @Author  : wujianhong

import os
import pandas as pd
class Bike():
	def __init__(self, source):
		data_list = source.split(',')
		self._bike_id = data_list[0]
		self.biketype = data_list[1]
		self.boundary= data_list[2]
		self.dist_id= data_list[3]
		self.dist_num= data_list[4]
		self.dist_x= data_list[5]
		self.dist_y= data_list[6]
		self.distince= data_list[7]
		self.type= data_list[8]

if __init__ == "__mian__":
	
