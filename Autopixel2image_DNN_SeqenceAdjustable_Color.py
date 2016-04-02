#!/usr/bin/python
# -*- coding: utf-8 -*-

from matplotlib import pylab
import sys,re,os
from pylab import *
import glob
import numpy as np
import re
import subprocess

def sp_call(cmd):
	if subprocess.call(cmd) != 0:
		print cmd[0] + " " + cmd[1] + " Error!"
		exit()

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

#SequenceLength = [185,214,269,204,229,196,196,306,211,191,284,270,229,239,249,282,448,437,510,440]
#SequenceName = ['Smooth01','Smooth02','Smooth03','Smooth04','Smooth05','Smooth06','Smooth07','Smooth08','Smooth09','Smooth10','Smooth11',
#		'Smooth12','Smooth13','Smooth14','NotSmooth01','NotSmooth02','NotSmooth03','NotSmooth04','NotSmooth05','NotSmooth06']
#Nextage PenPicking Experiment1
#SequenceLength = [157,451,218,700,414,384,673,170,183,818,498,621,1045]
#SequenceName = ['Train01','Train02','Train03','Train04','Train05','Train06','Train07','Train08','Train09','Train10','Train11','Train12','Train13']
#Nextage PenPicking Experiment1 Test
SequenceLength = [603,647]
SequenceName = ['Test01','Test02']

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) < 3:
		print "Usage: Autopixel2image.py [InputFile] [OutputDir]"
		exit()

	#Check SequenceLength and SequenceName Length
	if len(SequenceLength) != len(SequenceName):
		print "[ERROR] Your length of [SequenceLength] is "+str(len(SequenceLength))+"and [SequenceName] is "+str(len(SequenceName))
		print "[ERROR] They must be same!"
		exit()


	Input_file  = argv[1]
	Output_dir_tmp = argv[2]
	if Output_dir_tmp[len(Output_dir_tmp)-1] == "/":
		Output_dir = Output_dir_tmp[:-1]
	else:
		Output_dir = Output_dir_tmp

	fr = open(Input_file, "r")
	lines = fr.readlines()
	fr.close()
	lines_dim = len(lines)#ファイル内の行数の長さ
	line_dim = len(str2flist(lines[0]))#1行辺りの次元

	if os.path.isdir(Output_dir) == False:#フォルダがなければ作成
		os.mkdir(Output_dir)



	#Seperate Pixel File
	count = 1
	count_group = 0
	for i in range(lines_dim):
		if count == 1: 
			fw = open(Output_dir + "/" + SequenceName[count_group] + ".dat", "w")
			print count_group
			count_group = count_group + 1

		count = count + 1;
		if SequenceLength[count_group-1] < count:
			count = 1


		buf = str2flist(lines[i])
		for j in range(0, line_dim):
			fw.write(format(buf[j],'.6f'))
			#fw.write(format((buf[j]*0.80+0.10),'.6f'))
			fw.write(" ")
		fw.write("\n")
	fw.close()
	
	#pixelデータから画像を作成
	files = glob.glob(Output_dir + "/" + "*.dat")
	sort_nicely(files)
	for file in files:
		fr_out = open(file, "r")
		lines = fr_out.readlines()
		fr_out.close()
		lines_DNN = len(lines)#ファイル内の行数の長さ
		line_DNN = len(str2flist(lines[0]))#1行辺りの次元
		base = os.path.basename(file)
		file_name = os.path.splitext(base)[0]
		file_name_dir = Output_dir + "_image" + "/" + file_name
		if os.path.isdir(Output_dir + "_image") == False:#フォルダがなければ作成
			os.mkdir(Output_dir + "_image")
		if os.path.isdir(file_name_dir) == False:#フォルダがなければ作成
			os.mkdir(file_name_dir)
		cmd = ["./pixel2image_DNN_Color", str(file), str(file_name_dir), str(lines_DNN)]
		sp_call(cmd)

	#画像の拡大
	file_name_tmp = Output_dir + "_image"
	files2 = os.listdir(file_name_tmp)
	sort_nicely(files2)
	for file2 in files2:
		files3 = glob.glob(file_name_tmp + "/" + file2 + "/" + "*.bmp")
		sort_nicely(files3)
		for file3 in files3:
			cmd = ["convert", "-geometry", "400%", file3, file3]
			sp_call(cmd)


