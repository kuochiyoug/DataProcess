#!/usr/bin/python

import sys,os,re

def normalize(value,Maxvalue,Minvalue,NewMaxvalue=0.9,NewMinvalue=0.1): #Normalize the value to the range between NewMax and NewMin
	anwser = NewMaxvalue-((Maxvalue-value)*(NewMaxvalue-NewMinvalue)/(Maxvalue-Minvalue))
	return anwser

def sort_nicely(list):
	convert = lambda text: int(text) if text.isdigit() else text 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	list.sort( key=alphanum_key ) 

argv = sys.argv


NormalizeRangeList = [[-88,88],[-140,60],[0,-158],[-165,105],[-100,100],[-163,163],
		[-88,88],[-140,60],[0,-158],[-165,105],[-100,100],[-163,163],
		[-1,800],[-1,800]]

NormalizeMax = 0.9
NormalizeMin = 0.1



if len(argv) != 3:
	print "Before you do this! Please check your Normalize Range in this code."
	print "Usage: getMotionData.py [InputDir] [OutputDir]"
	exit()

indir = os.path.realpath(argv[1])
outdir = os.path.realpath(argv[2])

for root,dirs,files in os.walk(indir):
	if root.startswith(outdir):
		continue
	#print root
	
	"""
	for d in dirs:
		if outdir == os.path.join(root,d):
			continue
		outd = os.path.join(root.replace(indir,outdir),d)
		if os.path.isdir(outd):
			shutil.rmtree(outd)
		os.makedirs(outd)
	"""

	sort_nicely(files)
	for f in files:
		#realpath = os.path.abspath(f)
		#print root
		#print os.path.dirname(realpath)

		if not f.endswith(".dat"):
			continue
		inf = os.path.join(root,f)
		fr = open(inf,"r")
	        InputDatalines = fr.readlines()
	        fr.close()


		##Read Data from files
		Motion = []
		for i in range(len(InputDatalines)):
			Motion.append(map(float,InputDatalines[i].strip("\n").split('\t')))
			

		
		inf = os.path.join(root,f)
		outf = os.path.join(root.replace(indir,outdir),f)
		print outf
		if not os.path.isdir(os.path.dirname(outf)):
			os.makedirs(os.path.dirname(outf))
			print os.path.dirname(outf)

		file_out = open(outf,"w")
		for i in range(len(Motion)):
			for j in range(len(Motion[i])):
				NormalizedValue = normalize(Motion[i][j],NormalizeRangeList[j][1],NormalizeRangeList[j][0],NormalizeMax,NormalizeMin)
				if NormalizedValue > NormalizeMax :
					print "WARNING!!!! Check Your Normalized Range! Some Value over "+str(NormalizeMax)+"!"
				if NormalizedValue < NormalizeMin :
					print "WARNING!!!!!!! Check Your Normalized Range! Some Value less than "+str(NormalizeMin)+"!"
				file_out.write(str(format(NormalizedValue,'.7f')))
				if not j == len(Motion[i])-1:
					file_out.write(" ")
			file_out.write("\n")
		file_out.close()
