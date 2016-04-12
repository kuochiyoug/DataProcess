#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        DNNReprodiceClass.py
# Purpose:     A fast way for applying Online Feed Foward Calculation in python Code.
# Version:     1.0.0 (2016.01.04)
# Author:      KomaYang
# OS:          Ubuntu 14.04
# Created:     2016.01.04
# Copyright:   (c) YANG PIN CHU(Koma) at SuganoLab in Waseda University 2016
#-------------------------------------------------------------------------------
# Note: 
# (1) By loading trained model file that trained by HFDNN matlab program made by Dr.Noda.
# (2) When you want to input your data, you will need to translate your data type to 'numpy.ndarray'. It usually need to be transpose. 
# (3) For only 1 image pixel input data, you need to reshape your data to (1,PIXEL_SIZE_OF_IMAGE) in order to acquire correct data. 

import sys
import os
import cv2
import numpy as np
import numpy.matlib
import scipy.io as sio

class DNNReproduceClass:
    def __init__(self,DNN_MODEL,ShowDetails=False):
        self.DNN_MODEL = DNN_MODEL
        self.ShowDetails = ShowDetails
        print "[INFO] Start Loading Model..."
        self.__load_Model()
        print "[INFO] Loading Compeleted! Class Standing by..."
        
    def __load_Model(self):
        ModelFile = sio.loadmat(self.DNN_MODEL)
        self.cnf = CNF_for_FeedForward(ModelFile)
        paramsp = ModelFile['info']['paramsp'][0][0].T
        if self.ShowDetails:
            print "Parameter Amount:" + str(paramsp.size)
            print "Layersize:"+str(self.cnf.layersizes.T) 
        [self.Wu,self.bu] = self.__unpack_param(paramsp,self.cnf)
        ModelFile = None

    def __unpack_param(self,M,cnf):
        W = [] 
        b = []
        cur = 0
        for i in range(cnf.numlayers):
            Min = M[0,cur:(cur+int(cnf.layersizes[i,0])*int(cnf.layersizes[i+1,0]))]
            W.append(Min)
            W[i] = np.reshape(W[i],(int(cnf.layersizes[i+1,0]),int(cnf.layersizes[i,0])),order="F")
            if self.ShowDetails:
                print "W=" + str(W[i][0:3,0])
                print "W.shape=" + str(W[i].shape)
            cur = cur + int(cnf.layersizes[i,0])*int(cnf.layersizes[i+1,0])

            b_in = np.reshape(M[0,cur:(cur+int(cnf.layersizes[i+1,0]))],(int(cnf.layersizes[i+1,0]),1),order="F")
            b.append(b_in)
            if self.ShowDetails:
                print "b=" + str(b[i][0:3,0])
                print "b.shape=" + str(b[i].shape)
            cur = cur + int(cnf.layersizes[i+1,0])
        return [W,b]
    
    def __forward(self,layertypes,using_layer,data):
        if self.ShowDetails:
            print "[INFO] Start Fowarding..."
        yip = data
        for i in using_layer:
            yi = yip
            xi = np.dot(self.Wu[i],yi) + numpy.matlib.repmat(self.bu[i],1,data[0].size)
            if self.ShowDetails:
                print "Input in layer "+str(i)+" : "+str(xi)
                print "Input Shape : " + str(xi.shape)
            if layertypes[i,0][0] == "logistic":
                yip = 1.0/(1 + np.exp(-xi))
            elif layertypes[i,0][0] == "tanh":
                yip = np.tanh(xi)
            elif layertypes[i,0][0] == "linear":
                yip = xi
            else:
                print "[ERROR] Unknown/Unsupport Layer Type!"
                exit()
            """
            elif layertypes[i,0][0] == "softmax":
                tmp = exp(xi);
                yip = tmp./repmat( sum(tmp), [self.cnf.layersizes(i+1) 1] );
                tmp = None;
            """
        return yip


    def Fw_prop_partial(self,st_layer,data,ed_layer):
        using_layer = range(st_layer,ed_layer)
        yip = self.__forward(self.cnf.layertypes,using_layer,data)
        return yip


        
class CNF_for_FeedForward:
    def __init__(self,ModelFile):
        self.numlayers = ModelFile['cnf']['numlayers'][0][0].transpose()
        self.layersizes = ModelFile['cnf']['layersizes'][0][0].transpose()
        self.layertypes = ModelFile['cnf']['layertypes'][0][0].transpose()


if __name__ == '__main__':
    RModel = "/home/assimilation/Koma/workspace/HFOptimizeSimple/result/NextageExperiment/FoldingTask/TableOnly/DNN/mid25/ALL_R_Color_2e-7_seed12345_Train5404_TestSmooth01/result_HFMNIST_12345_80.mat"

    InputDataFile = "/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-LeftHand_ShimaRagOnly/Data4DNN/40x30_Color/ALL_R.dat"
    data = np.loadtxt(InputDataFile)
    
    ORC_R = DNNReproduceClass(RModel,ShowDetails=False)
    #ORC_L = OnlineDNNReproduceClass(LModel)
    #ORC_TDNN = OnlineDNNReproduceClass(TDNN_Model)
    Value = ORC_R.Fw_prop_partial(0,data.T,6).transpose()
    print Value.shape
    print Value[0]
    print type(Value)
