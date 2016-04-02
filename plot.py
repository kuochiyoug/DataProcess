#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,re,os
import math
import matplotlib.pyplot as plt
import graph_line_class as Line
import graph_marker_class as Marker

def execute(Input_dir_line,Input_dir_marker):

	#line_plot = Line.Graph_line(Input_dir_line)	
	marker_plot = Marker.Graph_marker(Input_dir_marker)	

	#line_plot.Line_plot()
	marker_plot.Marker_plot()

	plt.xlabel("X [cm]",fontsize=15)
	plt.ylabel("Y [cm]",fontsize=15)
	plt.suptitle("Armtip Position",size="20")
	plt.legend(bbox_to_anchor=(0.3, 1.0))
	plt.savefig(Input_dir_marker + "/test_marker.png")
	plt.clf()#描画のリセット

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) != 3:
		print "make_graph.py [Input_File_line] [Input_File_marker]"
		exit()
		
	execute(argv[1],argv[2])
