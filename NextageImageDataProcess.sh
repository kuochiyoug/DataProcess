#!/bin/bash
#!/usr/bin/python
clear

#echo "Please input your Raw Data folder:"
#read RAW_DATA
#echo "Please input your output folder:"
#read OUT
IMAGE_RAW_DATA="/home/assimilation/Koma/Nextage_Experiment/PenPicking/SamePosition/RawData/IdolData/Image/"
OUT="/home/assimilation/Koma/Nextage_Experiment/PenPicking/SamePosition/ProcessData_CV2/"
Resized_H=30
Resized_W=40


#########################################
echo "RAW IMAGE --> PIXEL...."
PIXEL_DATA=$OUT"IMG_Pixel/"
mkdir $PIXEL_DATA
#
#python ./getPixelsAll.py $IMAGE_RAW_DATA $PIXEL_DATA
python ./getPixelsAll_komaCV2format.py $IMAGE_RAW_DATA $PIXEL_DATA $Resized_H $Resized_W


echo "Connecting each Image to Motion...."
CONNECT_DATA=$OUT"IMG_ConnectPixelData/"
mkdir $CONNECT_DATA
python ./Input_image4DNN_without_normalize.py $PIXEL_DATA $CONNECT_DATA


echo "Connecting all file to One File...."
CONNECT_COMMAND_R=$CONNECT_DATA"Right/"
CONNECT_COMMAND_L=$CONNECT_DATA"Left/"
Motion_Count=$(ls $CONNECT_COMMAND_L | grep ".dat$" | wc -l)
Files=$(ls $CONNECT_COMMAND_L | grep ".dat$") 
echo "You have "$Motion_Count "files to Connect"
echo $Files
CONNECT_FILE_L=$CONNECT_DATA"IMG_Left_Motion$Motion_Count""_ConnectedData.dat"
CONNECT_FILE_R=$CONNECT_DATA"IMG_Right_Motion$Motion_Count""_ConnectedData.dat"
LIST_FILE_L=$CONNECT_DATA"IMG_Left_ConnectList.dat"
LIST_FILE_R=$CONNECT_DATA"IMG_Right_ConnectList.dat"

python ./Input_image4DNN_connect_Infolder.py $CONNECT_COMMAND_L $CONNECT_FILE_L $LIST_FILE_L
python ./Input_image4DNN_connect_Infolder.py $CONNECT_COMMAND_R $CONNECT_FILE_R $LIST_FILE_R
echo "Image Teaching Data Generate Complete"
#########################################

