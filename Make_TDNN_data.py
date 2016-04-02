#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,re,os
from pylab import *
import glob
import subprocess
import os.path
import pipes

STEP = 30
#ReadDirs = ["angle","angular_velocity","arm_tip","torque"]
#ReadDirs = ["angle","angular_velocity","arm_tip"]
#ReadDirs = ["angle","arm_tip"]
#ReadDirs = ["l_angle","l_armtip","r_angle","r_armtip"]
#ReadDirs = ["r_angle","l_angle"]
#ReadDirs = ["r_1","r_2","r_3","r_4","r_test"]
#ReadDirs = ["r_5","r_6","r_7","r_8"]
#ReadDirs = ["r_2"]
#Filename = "/r1234test_test_2e10_0.01_30step"
#ReadDirs2 = ["r_5","r_6","r_7","r_8"]
#データ文字列をfloatのリストに変換	
def str2flist(str):
	str = str.split()
	ret = []
	for x in str:
		ret.append(float(x))#末尾に追加（アクトロイド用）
	return ret

def execute(Teach_File, Output_File):
	fw1 = open(Output_File,"w")
	#for ReadDir in ReadDirs:
	fr = open(Teach_File,"r")
	lines = fr.readlines()
	fr.close()
	dim = len(str2flist(lines[0]))
	for k in range(0, len(lines)-29):
		for j in range(STEP):
			buf = str2flist(lines[k+j])
			for i in range(0,dim):
				fw1.write(str(buf[i]) + " ")
		fw1.write("\n")
	fw1.close()

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 3:
		print "Make_TDNN_data.py [Teach_File] [Output_File]"
		exit()
		
	execute(argv[1],argv[2])
