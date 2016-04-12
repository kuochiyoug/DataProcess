import sys
import os,re,glob
import numpy as np
import cv2


def str2flist(str):
    str = str.split()
    ret = []
    for x in str:
        ret.append(float(x))
    return ret


def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) <= 6:
        print "Usage: Input_image4DNN_connect_Infolder.py [InputFile] [Outputfolder] [ListFile] [Resized_H] [Resized_W]"
        exit()
    infile = os.path.realpath(argv[1])
    outdir = os.path.realpath(argv[2])
    ListFile = argv[3]
    Resized_H = int(argv[4])
    Resized_W = int(argv[5])

    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)


    print "Loading ListFile..."
    fl = open(ListFile,"r")
    list_lines = fl.readlines()
    fl.close()
    SequenceLength = []
    SequenceName = []
    for line in list_lines:
        SequenceLength.append(int(line.split(" ")[1].strip("/n").strip("\n")))
        SequenceName.append(line.split(" ")[0].strip("/n").strip("\n"))
    print SequenceLength
    print SequenceName
    
    


    print "Loading DataFile..."
    fr = open(infile,"r")
    lines = fr.readlines()
    fr.close()
    lines_dim = len(lines)
    line_dim = len(str2flist(lines[0]))


    print "Seperate & Creating Pixel Files..."
    count = 1
    count_group = 0
    for i in range(lines_dim):
        if count == 1: 
            fw = open(outdir + "/" + SequenceName[count_group], "w")
            #print count_group
            count_group = count_group + 1
        count = count + 1;
        if SequenceLength[count_group-1] < count:
            count = 1
        buf = str2flist(lines[i])
        for j in range(0, line_dim):
            fw.write(format(buf[j],'.7f'))
            #fw.write(format((buf[j]*0.80+0.10),'.6f'))
            fw.write(" ")
        fw.write("\n")
    fw.close()
    
    

    print "Generating Images..."
    files = glob.glob(outdir + "/" + "*.dat")
    sort_nicely(files)
    for file in files:
        fr_out = open(file, "r")
        lines = fr_out.readlines()
        fr_out.close()
        base = os.path.basename(file)
        file_name = os.path.splitext(base)[0]
        file_name_dir = outdir + "_image" + "/" + file_name
        if os.path.isdir(outdir + "_image") == False:
            os.mkdir(outdir + "_image")
        if os.path.isdir(file_name_dir) == False:
            os.mkdir(file_name_dir)
        count = 0
        for line in lines:
            line_float = str2flist(line)
            pixels = np.asarray(line_float)
            pixels = (pixels.reshape((Resized_H,Resized_W,3))*255).astype('uint8')
            cv2.imshow("window",pixels)
            cv2.imwrite(file_name_dir+"/"+str(count)+".png",pixels)
            cv2.waitKey(1)
            count = count+1

