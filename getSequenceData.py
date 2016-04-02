#!/usr/bin/python

import sys,os,re


def sort_nicely(list):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)',key)]
    list.sort(key = alphanum_key)

argv = sys.argv

if len(argv) != 4:
	print "Usage: getSequenceData.py [InputDir] [OutputDir] [DATA_SEQUENCE_YOU_NEED]"
	print "Option for [DATA_SEQUENCE_YOU_NEED]:"
	print "(1) all : All Sequence will be saved."
	print "(2) [1,0,1,1]: Sequence 0,2,3 will be saved."
	exit()



indir = os.path.realpath(argv[1])
outdir = os.path.realpath(argv[2])



if argv[3]=="all":
	Trigger_for_need_data_list = False
else:
	needed_data_list = map(int,argv[3].strip("[").strip("]").split(","))
	Trigger_for_need_data_list = True

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
		tmp_f = f
		if tmp_f == "1.dat":
			tmp_f = "01.dat"
		if tmp_f == "2.dat":
			tmp_f = "02.dat"
		if tmp_f == "3.dat":
			tmp_f = "03.dat"
		if tmp_f == "4.dat":
			tmp_f = "04.dat"
		if tmp_f == "5.dat":
			tmp_f = "05.dat"
		if tmp_f == "6.dat":
			tmp_f = "06.dat"
		if tmp_f == "7.dat":
			tmp_f = "07.dat"
		if tmp_f == "8.dat":
			tmp_f = "08.dat"
		if tmp_f == "9.dat":
			tmp_f = "09.dat"

		inf = os.path.join(root,f)
		fr = open(inf,"r")
	        InputDatalines = fr.readlines()
	        fr.close()


		InputDatalines_float = map(float,InputDatalines[0].split(" "))
		

		##Check for length
		if Trigger_for_need_data_list == True:
			if not len(InputDatalines_float) == len(needed_data_list):
				print "[ERROR] Please input the same length of your choosen sequence list "			
				print "[INFO] Sequence Length: " + str(len(InputDatalines_float))
				print "[INFO] Your Input Length: " + str(len(needed_data_list))
				exit()
		else:
			needed_data_list = []
			for i in range(len(InputDatalines_float)):
				needed_data_list.append(1)

		print "DataTaken:" + str(needed_data_list)

		##Read Data from files
		index = 0
		Data = []
		for i in range(len(InputDatalines)):
			Data.append(InputDatalines[index].strip("\n").split('\t'))
			index = index + 1 

		
		inf = os.path.join(root,f)
		outf = os.path.join(root.replace(indir,outdir),tmp_f)
		print outf		
		if not os.path.isdir(os.path.dirname(outf)):
			os.makedirs(os.path.dirname(outf))
			print os.path.dirname(outf)

		file_out = open(outf,"w")
		for i in range(len(Data)):
			for j in range(len(Data[i])):
				if needed_data_list[j] == 1:
					file_out.write(str(format(Data[i][j],'.7f')))
					if not j == len(Data[i])-1:
						file_out.write(" ")
				elif needed_data_list[j] == 0:
					pass
				else:
					print "[ERROR] needed_data_list only accept for 0 or 1"
					exit()
			file_out.write("\n")
		file_out.close()

		

