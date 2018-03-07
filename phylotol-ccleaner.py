import os, sys
import Utilities

infile = open('pipeline_parameter_file.txt','r').readlines()
for line in infile:
	if line[0] == '#':
		attribute = line.split()[0].strip('#')
		value = line.split()[2].strip()
		if attribute == 'PathtoFiles':
			PathtoFiles = value
		elif attribute == 'testPipelineList':
			testPipelineList = value

restart = 'y'
while restart == 'y':

	treeFolder = '../' + testPipelineList + '_results2keep/'
	if os.path.exists(treeFolder):
		
		