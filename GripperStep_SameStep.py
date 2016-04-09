#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,re,os
from pylab import *
import glob
import numpy as np
import math

Stepsize = 3


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
        print "Usage: Gripper_Step.py [InputDir] [OutputDir] [Gripper_Amount]"
        exit()
    Input_dir = argv[1]
    outdir = argv[2]
    Gripper_Amount = argv[3]
    if Input_dir[-1] != "/":
        Input_dir = Input_dir+"/"

    if Gripper_Amount == "1":
        ModifyList =[-1]
    elif Gripper_Amount == "2":
        ModifyList =[-1,-2]
    else:
        print "[ERROR] Gripper Amount Max to 2"
        exit()

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


            newlist = []
            for line in lines:
                newlist.append(str2flist(line))


            
            for sequence in ModifyList:
                start_index = []
                start_dvalue = []
                start_ini_value = []
                end_index = []
                end_dvalue = []
                end_ini_value = []
                i = 0 
                for line in lines:
                    buf = str2flist(line)
                    if i == 0:
                        pass
                    else:
                        buf_tmp = str2flist(lines[i-1])
                        if buf[sequence] != buf_tmp[sequence]:
                            if buf[sequence] < buf_tmp[sequence]:
                                end_index.append(lines.index(line))
                                end_dvalue.append(buf[sequence] - buf_tmp[sequence])
                                end_ini_value.append(buf_tmp[sequence])
                            elif buf[sequence] > buf_tmp[sequence]:
                                start_index.append(lines.index(line))
                                start_dvalue.append(buf[sequence] - buf_tmp[sequence])
                                start_ini_value.append(buf_tmp[sequence])
                    i = i + 1 

                print start_index
                print start_ini_value
                print start_dvalue

                count = 0
                for start_point in start_index:
                    step_num = 1
                    for step in range(Stepsize):
                        #print start_ini_value[start_point]
                        newlist[start_point+step][sequence] = start_ini_value[count] + (start_dvalue[count]*step_num)/Stepsize
                        step_num = step_num + 1
                    count = count +1

                count = 0
                for end_point in end_index:
                    step_num = 1
                    for step in range(Stepsize):
                        newlist[end_point+step][sequence] = end_ini_value[count] + (end_dvalue[count]*step_num)/Stepsize
                        step_num = step_num + 1
                    count = count +1


            for line in newlist:
                for i in range(len(line)):
                    value = line[i]
                    if i != len(line)-1:
                        fw.write(format(value,'.7f')+"\t")
                    else:
                        fw.write(format(value,'.7f'))
                fw.write("\n")
            fw.close()
