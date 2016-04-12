import sys
import os,re,glob
import numpy as np
import cv2

#from Nextage_Online_Logger_Class import ImageLoggerThread
#from Nextage_Data_Processing_Class import Data_Processing_Class
from DNNReproduceClass import DNNReproduceClass

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
    if len(argv) != 7:
        print "Usage: Input_image4DNN_connect_Infolder.py [InputFile] [Outputfolder] [ListFile] [ModelFile] [InputLayer] [OutputLayer]"
        print len(argv)
        exit()
    infile = os.path.realpath(argv[1])
    outdir = os.path.realpath(argv[2])
    ListFile = argv[3]
    ModelFile = argv[4]
    InLayer = int(argv[5])
    OutLayer = int(argv[6])

    if os.path.isdir(outdir) == False:
        os.makedirs(outdir)


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
    
   
    """
    print "Loading DataFile..."
    fr = open(infile,"r")
    lines = fr.readlines()
    fr.close()
    lines_dim = len(lines)
    line_dim = len(str2flist(lines[0]))
    """

    print "Loading Model & Fowarding Data..."
    ORC = DNNReproduceClass(ModelFile,ShowDetails=False)
    data = np.loadtxt(infile)
    Value = ORC.Fw_prop_partial(InLayer,data.T,OutLayer).transpose()
    print Value.shape
    #print Value[0]
    #print type(Value)
    List_Fowarded_Value = Value.tolist()
    lines_dim = len(List_Fowarded_Value)
    line_dim = len(List_Fowarded_Value[0])


    print "Seperate & Fowarding Data & Creating Result Files..."
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
        #print List_Fowarded_Value[i]
        buf = List_Fowarded_Value[i]
        for j in range(0, line_dim):
            fw.write(format(buf[j],'.7f'))
            #fw.write(format((buf[j]*0.80+0.10),'.6f'))
            fw.write(" ")
        fw.write("\n")
    fw.close()

    print "Done"

