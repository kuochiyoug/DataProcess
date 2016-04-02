#!/usr/bin/python

import re,sys,os
import shutil
import cv2
import numpy as np

argv = sys.argv

if len(argv) != 3:
    print "Usage: test.py [InputDir] [OutputDir]"
    exit()

indir = os.path.realpath(argv[1])
outdir = os.path.realpath(argv[2])

for root,dirs,files in os.walk(indir):
    if root.startswith(outdir):
        continue
    #print root
    
    for d in dirs:
        if outdir == os.path.join(root,d):
            continue
        outd = os.path.join(root.replace(indir,outdir),d)
        if os.path.isdir(outd):
            shutil.rmtree(outd)
        os.makedirs(outd)


    for f in files:
        #realpath = os.path.abspath(f)
        print root
        #print os.path.dirname(realpath)


        if not f.endswith(".png"):
            continue
        tmp_f = f
        if tmp_f == "1.png":
            tmp_f = "01.png"
        if tmp_f == "2.png":
            tmp_f = "02.png"
        if tmp_f == "3.png":
            tmp_f = "03.png"
        if tmp_f == "4.png":
            tmp_f = "04.png"
        if tmp_f == "5.png":
            tmp_f = "05.png"
        if tmp_f == "6.png":
            tmp_f = "06.png"
        if tmp_f == "7.png":
            tmp_f = "07.png"
        if tmp_f == "8.png":
            tmp_f = "08.png"
        if tmp_f == "9.png":
            tmp_f = "09.png"
        inf = os.path.join(root,f)


        
        print "inf: " + str(inf)
        outf = os.path.join(root.replace(indir,outdir),tmp_f)
        print outf
        #print os.path.dirname(outf)
        if not os.path.isdir(os.path.dirname(outf)):
            os.makedirs(os.path.dirname(outf))
            print os.path.dirname(outf)
        outf = outf.replace(".png",".dat")
        #cmd = ["./getPixel",inf,outf]
        #cmd = ["./getPixelColor",inf,outf]
        array = cv2.imread(inf)
        (h, w) = array.shape[:2]
        array = cv2.resize(array,(h/4,w/4))
        np.savetxt(outf,array)
