#!/usr/bin/python
# -*- coding: utf-8 -*-
#Links adjustable version remodified by Koma


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
	if len(argv) <= 3:
		print "Usage: Input_image4DNN_connect_kai2.py [InputFile1] [InputFile2]....[InputFileN] [Outputfile]"
		exit()

	input_files_number = len(argv)-2
	print "You have input " + str(input_files_number) + " files."

	Input_file = []
	for i in range(input_files_number):
		Input_file.append(argv[i+1])
	Output_file = argv[input_files_number+1]
	#print Input_file

	count = 1
	fw = open(Output_file, "w")
	for i in range(input_files_number):
		
		fr = open(Input_file[i], "r")
		lines = fr.readlines()
		fr.close()
		for j in range(0,len(lines)):
			buf = str2flist(lines[j])
			#fw.write(str(count))
			count = count + 1
			for k in range(0, len(buf)):
				fw.write(" ")
				fw.write(format( buf[k],'.7f'))			
			fw.write("\n")	
	fw.close()

