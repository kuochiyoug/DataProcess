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
    if len(argv) != 4:
        print "Usage: Input_image4DNN_connect_Infolder.py [InputFolder] [Outputfile] [ListFile]"
        #exit()



    indir = os.path.realpath(argv[1])
    Output_file = argv[2]
    List_file = argv[3]

    if indir[-1] != "/":
        indir=indir+"/"


    fw = open(Output_file, "w")
    fl = open(List_file,"w")

    for root,dirs,files in os.walk(indir):
        sort_nicely(files)
        for f in files:
            fr = open(indir+f, "r")
            lines = fr.readlines()
            fr.close()
            fl.write(f+" "+str(len(lines))+"\n")
            count = 0
            for j in range(0,len(lines)):
    	        buf = str2flist(lines[j])
    	        #fw.write(str(count))
    	        count = count + 1
    	        for k in range(0, len(buf)):
    		        fw.write(" ")
    		        fw.write(format( buf[k],'.7f'))			
    	        fw.write("\n")
    fw.close()
    fl.close()

