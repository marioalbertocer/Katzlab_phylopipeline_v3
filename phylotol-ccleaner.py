import os, sys
import Utilities

script, rules = sys.argv

infile = open('pipeline_parameter_file.txt','r').readlines()
for line in infile:
	if line[0] == '#':
		attribute = line.split()[0].strip('#')
		value = line.split()[2].strip()
		if attribute == 'PathtoFiles':
			PathtoFiles = value + "/"
		elif attribute == 'testPipelineList':
			testPipelineList = value

os.system('mkdir ../' + 'Temp')
temp = '../Temp'

restart = 'y'
run = 0
if "/" not in rules : rules = PathtoFiles + rules
seqs2remove_all = open(PathtoFiles + seqs2remove_all, 'w')

while restart == 'y':
	
	treeFolder = '../' + testPipelineList + '_results2keep/'
	if os.path.exists(treeFolder):
		run += 1
		os.system("python phyloTOL.py ct")
		Utilities.contaminationRemoval(treeFolder, PathtoFiles, rules)
		runOuts_path = "../Temp/" + testPipelineList + "_ContRun" + str(run) 
		os.system("mkdir " + runOuts_path)
		os.system('mv ' + treeFolder + " " + runOuts_path)
		os.system('mv sisterReport ' +  runOuts_path)
		os.system('mv nonHomologs ' +  runOuts_path)
		os.system('mv seqs2remove_out ' +  runOuts_path)
		os.system('mv seqs2remove_out_treesWcont ' +  runOuts_path)
		seqs2remove = open(runOuts_path + "/seqs2remove_out").readlines()
		treesWcont = open(runOuts_path + "/seqs2remove_out_treesWcont").readlines()
		for seq in seqs2remove : seqs2remove_all.write("%s" % seq)
		newListOGs = open(PathtoFiles + testPipelineList, 'w')
		for tree in treesWcont : newListOGs.write("%s" % treesWcont)
		if treesWcont == [] : restart = 'n'	
		
	else:
		os.system("python phyloTOL.py ct")
		
