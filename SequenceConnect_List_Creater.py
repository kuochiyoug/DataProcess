#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,re,os
from pylab import *
import glob

def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 

def execute(Target):
	fw = open("SequenceConnect_List.txt","w")
	files = os.listdir(Target)
	#files = glob.glob(os.path.abspath(Target)+"/*.dat")
	sort_nicely(files)
	for file in files:
		#fw.write(file.strip(".dat")+"\n")
		fw.write(file+"\n")
	fw.close()

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 2:
		print "SequenceConnect_List_Creater.py Target_dir"
		exit()
		
	execute(argv[1])
