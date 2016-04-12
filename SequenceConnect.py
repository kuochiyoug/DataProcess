#!/usr/bin/python

import sys,os,re
import collections
import numpy as np

def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 

def connecting(data1,data2):
    newdata = []
    steps = len(data1)
    data1_length = len(data1[0])
    data2_length = len(data2[0])
    for step in range(steps):
        newdata.append([])
        for i in range(data1_length):
            newdata[step].append(data1[step][i])
        for i in range(data2_length):
            newdata[step].append(data2[step][i])
    return newdata
    

argv = sys.argv

if len(argv) <= 3:
	print "Before you do this! Please check your Normalize Range in this code."
	print "Usage: SequenceConnect.py.py [ListFile] [InputDir1] [InputDir2] [OutputDir]"
	exit()


listfile = os.path.realpath(argv[1])
indir1 = os.path.realpath(argv[2])
indir2 = os.path.realpath(argv[3])
outdir = os.path.realpath(argv[4])


if indir1[-1] != '/':
    indir1 = indir1 + "/"
if indir2[-1] != '/':
    indir2 = indir2 + "/"
if outdir[-1] != '/':
    outdir = outdir + "/"

#GetConnectList
listfr = open(listfile,'r')
lines = listfr.readlines()
listfr.close()
DataNamelist=[]
for line in lines:
     DataNamelist.append(line.strip("\n"))
print DataNamelist 


for f in DataNamelist:
   #print f
   inf1 = os.path.join(indir1,f)
   inf2 = os.path.join(indir2,f)
   #print inf
   fr = open(inf1,"r")
   InputDatalines1 = fr.readlines()
   fr.close()
   ##Read Data from file in Indir1
   Data1 = []
   for i in range(len(InputDatalines1)):
        buf = np.fromstring(InputDatalines1[i],dtype=float,sep=" ")
        buf = buf.tolist()
        #print buf
        Data1.append(buf)


   fr = open(inf2,"r")
   InputDatalines2 = fr.readlines()
   fr.close()
   ##Read Data from file in Indir2
   Data2 = []
   for i in range(len(InputDatalines2)):
       buf = np.fromstring(InputDatalines2[i],dtype=float,sep=" ")
       buf = buf.tolist()
       #print buf
       Data2.append(buf)



   #print Data2
   #Check Data Length
   if len(Data1) != len(Data2):
       print "ERROR occurs in " + f
       print "Length Data1:" + str(len(Data1))
       print "Length Data2:" + str(len(Data2))
       print "DATA Length Different! Please Check!"
       exit()
   #print Data
   connected_data = connecting(Data1,Data2)
   if os.path.isdir(outdir) == False:
      os.makedirs(outdir)
      #print "Create Folder"

   compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
   outfr = open(outdir + f,"w")
   #print outdir + f
   for data in connected_data:
      for i in range(len(data)):
         #print data[i]
         outfr.write(format(data[i],".7f"))
         if not (i == len(data)-1):
            outfr.write(' ')
      outfr.write("\n")
   outfr.close()

