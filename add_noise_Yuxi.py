import glob
import numpy as np
import sys,os


argv = sys.argv
if len(argv) != 4:
    print "Usage: AutoSeperatebySequence.py [InputDir] [OutputDir] [seed]"
    exit()

Input_dir  = argv[1]
Output_dir = argv[2]
SeedNum = int(argv[3])


if Input_dir[-1] != "/" :
    Input_dir = Input_dir + "/"
if Output_dir[-1] != "/" :
    Output_dir = Output_dir + "/"
if os.path.isdir(Output_dir) == False:
    os.makedirs(Output_dir)

np.random.seed(SeedNum)

#sigma = 0.03
sigma = np.sqrt(0.0001)

filenames = glob.glob(Input_dir + "*.dat")    #get files's names and store in "filenames"
filenames.sort()

#print filenames

for filename in filenames:
    print filename
    new_filename = filename.replace(".dat", "_noisy_seed"+str(SeedNum)+".dat")  #get new name for new data
    data = np.loadtxt(filename)              #read and write file's content in data
    gaussian_noise = np.random.normal(0, sigma, size = (data.shape[0], data.shape[1]))
    data[:, :] += gaussian_noise[:, :]
    new_filename = os.path.basename(new_filename)
    print new_filename
    
    np.savetxt(Output_dir+new_filename, data, fmt = "%.6f",delimiter = " ")
        

