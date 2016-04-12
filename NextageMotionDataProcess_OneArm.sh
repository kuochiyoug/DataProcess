#!/bin/bash
#!/usr/bin/python
clear

#echo "Please input your Raw Data folder:"
#read RAW_DATA
#echo "Please input your output folder:"
#read OUT
MOTION_DATA="/home/assimilation/Koma/Nextage_Experiment/PenPicking/SamePosition/RawData/IdolData/Motion/"
NEEDMOTIONDATA="[0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1]"
OUT="/home/assimilation/Koma/Nextage_Experiment/PenPicking/SamePosition/ProcessData_CV2/IDOL_Only/"



echo "MotionData --> Teaching Data...."
MODIFIED_MOTION_DATA=$OUT"MotionFile_Without_GripperModify/"
python ./getMotionData_From_Logfile.py $MOTION_DATA $MODIFIED_MOTION_DATA $NEEDMOTIONDATA

echo "Modifying Gripper..."
GRIPPER_MODIFIED_MOTION_DATA=$OUT"MotionFile_GripperModified/"
python ./GripperStep_SameStep.py $MODIFIED_MOTION_DATA $GRIPPER_MODIFIED_MOTION_DATA 1

echo "Nomalizing Motion..."
NORMALIZED_GRIPPER_MODIFIED_MOTION_DATA=$OUT"MotionFile_Nomarlized_Gripper_Modified/"
python ./MotionNormalizer.py $GRIPPER_MODIFIED_MOTION_DATA $NORMALIZED_GRIPPER_MODIFIED_MOTION_DATA 2 1

echo "MotionData Processing Done"
