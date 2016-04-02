#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys,re,os
from pylab import *
import glob
import numpy as np
import math

Gripper_stepsize = 5

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
	if len(argv) < 2:
		print "Usage: Gripper_Step.py [InputDir]"
	Input_dir = argv[1]
	outdir = Input_dir + "/Modified_Motion"
	if not os.path.isdir(outdir):
		os.makedirs(outdir)
	Gripper_flag = False
	tmp_size = []

	files = os.listdir(Input_dir)
	print files
	sort_nicely(files)
	for file in files:
		if file.endswith(".dat"):
			print file
			fr = open(Input_dir + file, "r")
			lines = fr.readlines()
			fr.close()

			Output_file = outdir + "/" + file
			fw = open(Output_file, "w")

			for i in range(len(lines)):
				buf = str2flist(lines[i])
				if i == 0:
					pass
				else:
					buf_tmp = str2flist(lines[i-1])
					if buf[-1] != buf_tmp[-1] or buf[-2] != buf_tmp[-2]:
						print "Gripper_lines:" + str(i+1)
						for k in range(len(buf)):
							tmp_size.append((buf[k] - buf_tmp[k]) / Gripper_stepsize)
						Gripper_flag = True

				if Gripper_flag == True:
					for l in range(Gripper_stepsize+1):
						for k in range(len(buf)):
							buf[k] = buf_tmp[k] + (tmp_size[k] * l)
						for j in range(len(buf)):
							if j != len(buf)-1:
								fw.write(format(buf[j],'.7f')+"\t")
							else:
								fw.write(format(buf[j],'.7f'))
						fw.write("\n")
					Gripper_flag = False
					tmp_size = []
				else:
					for j in range(len(buf)):
						if j != len(buf)-1:
							fw.write(format(buf[j],'.7f')+"\t")
						else:
							fw.write(format(buf[j],'.7f'))
					fw.write("\n")
			fw.close()
