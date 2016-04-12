#!/bin/bash
#!/usr/bin/python
clear

#echo "Please input your Raw Data folder:"
#read RAW_DATA
#echo "Please input your output folder:"
#read OUT
RAW_CONNECT_IMAGE_FILE="/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-GreenSheet_LeftHand_ShimaRagOnly_2arms_Predesigned/ProcessedData_CV2/IMG_ConnectPixelData/IMG_Left_Motion5_ConnectedData.dat"
CONNECT_LIST_FILE="/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-GreenSheet_LeftHand_ShimaRagOnly_2arms_Predesigned/ProcessedData_CV2/IMG_ConnectPixelData/IMG_Left_ConnectList.dat"
TRAINED_MODEL="/home/assimilation/Koma/workspace/HFOptimizeSimple/result/NextageExperiment_CV2/GreenSheetTable/BothArms/mid50_2e-5/result_HFMNIST_12345_200.mat"
MODIFIED_MOTION_DATA="/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-GreenSheet_LeftHand_ShimaRagOnly_2arms_Predesigned/ProcessedData_CV2/Nomarlized_Gripper_Modified_Motion/"
OUT="/home/assimilation/Koma/Nextage_Experiment/FoldingTask/Experiment1-GreenSheet_LeftHand_ShimaRagOnly_2arms_Predesigned/ProcessedData_CV2/"
Resized_H=30
Resized_W=40
DNN_FeatureLayer=6
DNN_OutputLayer=12
TDNN_WINDOW=30




############################################
DNN_OUT_FOLDER=$OUT"DNN_output/"

echo "[SH]Fowarding Data with Models to Image(For Checking)..."
IMG_FEATURES_FOLDER=$DNN_OUT_FOLDER"IMG_Fowarded/"
python ./AutoDNNFeedForwarder_ToCV2Image.py $RAW_CONNECT_IMAGE_FILE $IMG_FEATURES_FOLDER $CONNECT_LIST_FILE $TRAINED_MODEL 0 $DNN_OutputLayer $Resized_H $Resized_W


echo "[SH]Fowarding Data with Models..."
IMG_FEATURES_FOLDER=$DNN_OUT_FOLDER"IMG_Features/"
python ./AutoDNNFeedForwarder_ToValue.py $RAW_CONNECT_IMAGE_FILE $IMG_FEATURES_FOLDER $CONNECT_LIST_FILE $TRAINED_MODEL 0 $DNN_FeatureLayer


TDNN_DATA_FOLDER=$OUT"TDNN_DATA/"
echo "[SH]Combining Feature and Motion..."
COMBINED_FEATURES_AND_MOTION=$TDNN_DATA_FOLDER"CombinedData/"
python ./SequenceConnect_List_Creater.py $MODIFIED_MOTION_DATA
python ./SequenceConnect.py ./"SequenceConnect_List.txt" $MODIFIED_MOTION_DATA $IMG_FEATURES_FOLDER $COMBINED_FEATURES_AND_MOTION
#mkdir $COMBINED_FEATURES_AND_MOTION



COMBINED_FEATURES_AND_MOTION_CONNECT_FILE=$TDNN_DATA_FOLDER"CombinedData_Connect.dat"
LIST=$TDNN_DATA_FOLDER"CombinedData_Connect_List.dat"
python ./Input_image4DNN_connect_Infolder.py $COMBINED_FEATURES_AND_MOTION $COMBINED_FEATURES_AND_MOTION_CONNECT_FILE  $LIST

TDNN_TEACHING_DATA=$TDNN_DATA_FOLDER"TDNN_TeachingData_Window"$TDNN_WINDOW".dat"
echo "[SH]Creating TDNN Data"
python ./Make_TDNN_data.py $COMBINED_FEATURES_AND_MOTION_CONNECT_FILE $TDNN_TEACHING_DATA $TDNN_WINDOW
echo $TDNN_TEACHING_DATA
echo "Done"


