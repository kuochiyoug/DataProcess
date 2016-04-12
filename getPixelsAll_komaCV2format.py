#!/usr/bin/python

import re,sys,os
import shutil
import cv2
import numpy as np

argv = sys.argv

if len(argv) != 5:
    print "Usage: test.py [InputDir] [OutputDir] [Resize_H] [Resized_W]"
    exit()

indir = os.path.realpath(argv[1])
outdir = os.path.realpath(argv[2])
resized_height = int(argv[3])
resized_width = int(argv[4])


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


    for f in sorted(files):
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
        
        #print outf
        #print os.path.dirname(outf)
        if not os.path.isdir(os.path.dirname(outf)):
            os.makedirs(os.path.dirname(outf))
            #print os.path.dirname(outf)
        outf = outf.replace(".png",".dat")
        print outf
        
        #cmd = ["./getPixel",inf,outf]
        #cmd = ["./getPixelColor",inf,outf]
        array = cv2.imread(inf)
        (h, w) = array.shape[:2]
        
        print resized_height
        print resized_width

        array = cv2.resize(array,(resized_width,resized_height))
        
        #array=array.astype(float)/255
        fw = open(outf, "w")
        array.tofile(outf," ")
        #print array.shape
        #print array.size
        
        count = 0 
        for h in range(resized_height):
            for w in range(resized_width):
                for ch in range(3):
                    #print "h:"+str(h)+" w:"+str(w)+" ch:"+str(ch)
                    #print array[h][w]
                    buff = float(array[h][w][ch])/255
                    #buff = array[h][w][ch]
                    #fw.write(str(buff))
                    fw.write(format(buff,'0.7f'))
                    count += 1
                    if int(w) != int(resized_width):
                        fw.write(" ")
            #fw.write("\n")
        #print count
        fw.close()
        
        
        img = np.fromfile(outf,sep=' ')
        #print img.shape
        #print img.reshape(resized_width,resized_height,3)
        cv2.imshow("window",array)
        cv2.waitKey(1)
