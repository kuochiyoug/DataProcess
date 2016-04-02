#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,re,os
import glob
import random
import shutil

MAX = 0.01
MIN = -0.01
Seed = 10

#データ文字列をfloatのリストに変換	
def str2flist(str):
	str = str.split()
	ret = []
	for x in str:
		ret.append(float(x))#末尾に追加（アクトロイド用）
	return ret

def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 

def execute(Input_dir):
	if not Input_dir.endswith("/"):
		Input_dir = Input_dir + "/"
	Output_dir_tmp = Input_dir + "range_"+str(MAX)+"/"
	if not os.path.isdir(Output_dir_tmp):
		os.mkdir(Output_dir_tmp)
	files = os.listdir(Input_dir)
	sort_nicely(files)
	for seed in range(Seed+1):
		Output_dir = Output_dir_tmp + str(seed)  + "/"
		if not os.path.isdir(Output_dir):
			os.mkdir(Output_dir)
		for file in files:
			if file.endswith(".dat"):
				if seed == 0:
					shutil.copyfile(Input_dir + file, Output_dir + file)
				else:
					fr = open(Input_dir + file, "r")
					lines = fr.readlines()
					fr.close()
					random.seed(seed)
					fw = open(Output_dir + file,"w")
					for i in range(len(lines)):
						buf = str2flist(lines[i])
						for k in range(len(buf)):
							buf[k] = buf[k] + random.uniform(MIN,MAX)
							fw.write(format(buf[k],".7f"))
							if not (k == len(buf)-1):
								fw.write(" ")
						fw.write("\n")
					fw.close()
	
if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 2:
		print "add_seed.py [Input_dir]"
		exit()
		
	execute(argv[1])
