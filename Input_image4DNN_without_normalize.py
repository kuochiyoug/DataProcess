#!/usr/bin/python
# -*- coding: utf-8 -*-

from matplotlib import pylab
import sys,re,os
from pylab import *
import glob
import numpy as np
import re
import subprocess

def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 

#データ文字列をfloatのリストに変換	
def str2flist(str):
	str = str.split()
	ret = []
	for x in str:
		ret.append(float(x))#末尾に追加
	return ret	
	
if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 3:
		print "Usage: Input_image2DNN.py [InputDir] [OutputDir]"
		exit()
	Input_dir   = argv[1]
	Output_dir = argv[2]
	count = 1
	#fw = open(Output_file, "w")
	files = os.listdir(Input_dir)
	sort_nicely(files)#ファイルソート([R_11,R_2,R_1]をソートすると，[R_1,R_2,R_11]となる)
	print files
	for file in files:#教師データディレクトリ下の各ファイルについて生成データと比較
		#print Input_dir + file
		#files2 = glob.glob(Input_dir + "/" +file + "/" + "*" +".dat")
		files2 = os.listdir(os.path.join(Input_dir,file))
		sort_nicely(files2)
		if not os.path.isdir(os.path.join(Output_dir,file)):
				os.makedirs(os.path.join(Output_dir,file))
		print files2	
		for file2 in files2:
			print file2
			fw = open(os.path.join(os.path.join(Output_dir,file),file2)+".dat","w")
			files3 = glob.glob(Input_dir + "/" + file + "/" + file2 + "/" + "*" + ".dat")
			sort_nicely(files3)
			for file3 in files3:
				print file3
				fr = open(file3, "r")
				lines = fr.readlines()
				fr.close()
				for i in range(0,len(lines)):
					buf = str2flist(lines[i])
					#fw.write(str(count))
					count = count + 1
					for j in range(0, len(buf)):
						#fw.write(format( buf[j]*(0.9-0.1)/(1.0-0.0)+0.1,'.7f'))#Normalize
						fw.write(format( buf[j],'.7f'))#Copy Only
						fw.write(" ")
					fw.write("\n")	
			fw.close()


