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

os.system('mkdir ../' + 'Temp')
temp = '../Temp'

restart = 'y'
run = 0
while restart == 'y':
	
	treeFolder = '../' + testPipelineList + '_results2keep/'
	if os.path.exists(treeFolder):
		run += 1
		os.system("python phyloTOL.py ct")
		ogs2reprocess = contaminationRemoval(treeFolder, PathtoFiles, rules)
		os.system('mkdir ../' + testPipelineList + '_ContRun' + str(run))
		os.system('rm ' + PathtoFiles + testPipelineList)
		newListOGs = open(PathtoFiles + testPipelineList, 'w')
		for og in ogs2reprocess = newListOGs.write("%s\n", og)