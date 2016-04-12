#-------------------------------------------------------------------------------
# Name:        TDNN_DataProcessing_Class.py
# Purpose:     Calibration Class
# OS:          Ubuntu 14.04
#-------------------------------------------------------------------------------

import sys,re,os
import Image
import cv2
import numpy as np

def normalize(value,Maxvalue,Minvalue,NewMaxvalue=0.9,NewMinvalue=0.1): #Normalize the value to the range between NewMax and NewMin
    answer = NewMaxvalue-((Maxvalue-value)*(NewMaxvalue-NewMinvalue)/(Maxvalue-Minvalue))
    return answer

def denormalize(value,Maxvalue,Minvalue,NewMaxvalue=0.9,NewMinvalue=0.1): #denormalize the value to the range between NewMax and NewMin
    answer = (value - NewMaxvalue) * (Maxvalue-Minvalue) / (NewMaxvalue-NewMinvalue) + Maxvalue
    return answer

def str2flist(str):
    str = str.split()
    ret = []
    for x in str:
        ret.append(float(x))
    return ret


class Data_Processing_Class:
    def __init__(self, NormalizeRange=[], NormalizeMax=0.9,NormalizeMin=0.1):
        print "=" * 10 + "Data Processing Initialize" + "=" * 10
        #===========Homography parameter===========
        self.NormalizeRangeList = NormalizeRange
        self.NormalizeMax = NormalizeMax
        self.NormalizeMin = NormalizeMin
        print "=" * 10 + "Data Processing Done" + "=" * 10

    def normalizer(self,old_data,Mode="",):
        self.new_data = []
        #print old_data
        if Mode == "normalize":
            for i in range(len(old_data)):
                self.new_data.append(normalize(old_data[i],
                     self.NormalizeRangeList[i][1],
                     self.NormalizeRangeList[i][0],
                     self.NormalizeMax, self.NormalizeMin))
        elif Mode == "denormalize":
            for i in range(len(old_data)):
                self.new_data.append(denormalize(old_data[i],
                     self.NormalizeRangeList[i][1],
                     self.NormalizeRangeList[i][0],
                     self.NormalizeMax, self.NormalizeMin))
        return self.new_data


    def deconnect_Sequence_with_denormalize(self,Sequence,Dimension_Per_Sequence,STEP):
        """
        Split Data to each sequence.
        Ex. You want your data (90 dims) transfer to 30x3 dims data
            >> deconnect_Sequence_with_denormalize(Sequence,Dimension_Per_Sequence=30,STEP=3)
        """
        output_list=[]
        for j in range(STEP):
            data = []
            for k in range(Dimension_Per_Sequence):
                data.append(Sequence[j*(Dimension_Per_Sequence)+k])
            data = self.normalizer(data, Mode="denormalize")
            output_list.append(data)
        return output_list

    def deconnect_Sequence(self,Sequence,Dimension_Per_Sequence,STEP):
        """
        Split Data to each sequence.
        Ex. You want your data (90 dims) transfer to 30x3 dims data
            >> deconnect_Sequence_with_denormalize(Sequence,Dimension_Per_Sequence=30,STEP=3)
        """
        output_list=[]
        for j in range(STEP):
            data = []
            for k in range(Dimension_Per_Sequence):
                data.append(Sequence[j*(Dimension_Per_Sequence)+k])
            output_list.append(data)
        return output_list

    def deconnect_DataFromOneSequence(self, Sequence, Start, Size):
        output = []
        #print Sequence
        for i in range(Start, Start + Size):
            output.append(Sequence[i])
        return output


    def deconnect_InitialMotion_fromFile_2file(self, OldMotionPath="",NewMotionPath="",STEP_start=50,STEP=30,Dimension=14):
        fr = open(OldMotionPath,"r")
        lines = fr.readlines()
        fr.close()
        buf = str2flist(lines[0])
        fw = open(NewMotionPath,"w")
        for j in range(STEP):
            self.output_tmp = []
            self.output_angle = []
            for k in range(STEP_start+((STEP_start+Dimension)*j),(STEP_start+Dimension)+((STEP_start+Dimension)*j)):
                self.output_tmp.append(buf[k])
            self.output_angle = self.normalizer(self.output_tmp, Mode="denormalize")
            for k in range(len(self.output_angle)):
                fw.write(str(self.output_angle[k])+" ")
            fw.write("\n")
        fw.close()


    def deconnect_InitialMotion_fromFile(self, Path="",SequenceStart=25,Dimension=7,STEP=30):
        fr = open(Path,"r")
        lines = fr.readlines()
        fr.close()
        buf = str2flist(lines[0])
        #print buf
        output_angle_list = []
        for j in range(STEP):
            output_angle = []
            for k in range(SequenceStart+((SequenceStart+Dimension)*j),(SequenceStart+Dimension)+((SequenceStart+Dimension)*j)):
                output_angle.append(buf[k])
            output_angle = self.normalizer(output_angle, Mode="denormalize")
            output_angle_list.append(output_angle)
        return output_angle_list

    def deconnect_InitialImgFeature_fromFile(self, Path="",SequenceStart=0,Dimension=25,STEP=30):
        fr = open(Path,"r")
        lines = fr.readlines()
        fr.close()
        buf = str2flist(lines[0])
        #print buf
        output_feature_list = []
        for j in range(STEP):
            output_feature = []
            for k in range(SequenceStart+((SequenceStart+Dimension)*j),(SequenceStart+Dimension)+((SequenceStart+Dimension)*j)):
                output_feature.append(buf[k])
            output_feature_list.append(output_feature)
        return output_feature_list

    def deconnect_InitialImgFeature_fromFile2(self, Path="",SequenceStart=0,Dimension=25,STEP=30):
        fr = open(Path,"r")
        lines = fr.readlines()
        fr.close()
        buf = str2flist(lines[0])
        buf.reverse()
        print "Features In File: " + str(len(buf))
        Dimension_per_sequence = len(buf)/STEP
        count = 0
        output_feature_list = []
        for i in range(STEP):
            output_feature = []
            for j in range(Dimension_per_sequence):
                data = buf.pop()
                if (count < SequenceStart+Dimension) and (count >= SequenceStart):
                    output_feature.append(data)
                else:
                    pass
                count = count + 1
                if count % Dimension_per_sequence == 0:
                    count = 0
            output_feature_list.append(output_feature)
        return output_feature_list


    def deconnect_ImageFromTDNN(self, Sequence, SequenceStart=0, Dimension=25, STEP=30):
        output_list=[]
        for j in range(STEP):
            output = []
            for k in range(SequenceStart+((SequenceStart+Dimension)*j),(SequenceStart+Dimension)+((SequenceStart+Dimension)*j)):
                output.append(buf[k])
            output_list.append(output)                
        return output_list

    
            


    #def get_lastSequence(self,SequenceStart)

    #def replace_for_SMTRNN(self,TDNN_data):


if __name__ == '__main__':
    NormalizeRangeList = [[-88,88],[-140,60],[0,-158],[-165,105],[-100,100],
            [-163,163],[-88,88],[-140,60],[0,-158],[-165,105],
            [-100,100],[-163,163],[-1,800],[-1,800]]
    Pro = Data_Processing_Class(NormalizeRangeList)
    #Path = '/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-LeftHand_ShimaRagOnly/TDNN_Generation/BothEyeImageFeatures_Motion_First30Step_from_Smooth02.dat'
    #listw = Pro.deconnect_InitialMotion(Path)
    Sequence = range(90)
    print len(Sequence)
    SpiltS = Pro.deconnect_Sequence(Sequence,Dimension_Per_Sequence=30,STEP=3)
    print SpiltS
    print len(SpiltS)
    print "YW"
    #print len(listw[0])
    print "YEnd"

