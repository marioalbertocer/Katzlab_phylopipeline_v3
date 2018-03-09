import os, sys
import Utilities

script, rules = sys.argv

print "\n\n ** runing PhyloTOL-cCleaner **\n\n"

# read parameters file and take the path to fasta files and the name of the OG list. 
infile = open('pipeline_parameter_file.txt','r').readlines()
for line in infile:
	if line[0] == '#':
		attribute = line.split()[0].strip('#')
		value = line.split()[2].strip()
		if attribute == 'PathtoFiles':
			PathtoFiles = value + "/"
		elif attribute == 'testPipelineList':
			testPipelineList = value


# Start variables for looping contamination removal, including creating the folder for temporal files and creating the file that will contain ALL sequences of contamination
os.system('mkdir ../' + 'Temp')
temp = '../Temp'
restart = 'y'
run = 0
if "/" not in rules : rules = PathtoFiles + rules
seqs2remove_all = open(PathtoFiles + seqs2remove_all, 'w')


# Start looping ... The loop will only stop when restart changes to 'n'

while restart == 'y': 
	treeFolder = '../' + testPipelineList + '_results2keep/'
	if os.path.exists(treeFolder):	

		# See if there are results from PhyloTOL. If so, do contamination removal. If there are not results, check 'else'.
		run += 1
		print "run " + str(run) + " PhyloTOL-cCleaner: runing PhyloTOL with contamination removal \n\n"
		os.system("python phyloTOL.py ct")  # run the pipeline with mode 'ct'
		print "run " + str(run) + " PhyloTOL-cCleaner: PhyloTOL done"
		
		# Run contamination removal. Check contaminationRemoval() in Utilities for details.  
		print "run " + str(run) + " PhyloTOL-cCleaner: removing contamination and non-homologs ..."
		Utilities.contaminationRemoval(treeFolder, PathtoFiles, rules)
		print "run " + str(run) + " PhyloTOL-cCleaner: contamination and non-homologs removal done ..."

		# Inside the Temp folder create an exclusive folder for temporal files in current run and move temporary files
		runOuts_path = "../Temp/" + testPipelineList + "_ContRun" + str(run) 
		os.system("mkdir " + runOuts_path)		
		os.system('mv ' + treeFolder + " " + runOuts_path)
		os.system('mv sisterReport ' +  runOuts_path)
		os.system('mv nonHomologs ' +  runOuts_path)
		os.system('mv seqs2remove_out ' +  runOuts_path)
		os.system('mv seqs2remove_out_treesWcont ' +  runOuts_path)
		
		# From outputs of contaminationRemoval() take contaminant sequences of the current run and attach them for the the list of ALL contaminant sequences.
		seqs2remove = open(runOuts_path + "/seqs2remove_out").readlines()
		for seq in seqs2remove : seqs2remove_all.write("%s" % seq)
		print "run " + str(run) + " PhyloTOL-cCleaner: contamination sequeces appended to final list"
		
		# From outputs of contaminationRemoval() take list of trees with contamination, and use it for running next iteration of contamination removal.
		treesWcont = open(runOuts_path + "/seqs2remove_out_treesWcont").readlines()
		newListOGs = open(PathtoFiles + testPipelineList, 'w')
		for tree in treesWcont : newListOGs.write("%s" % treesWcont)
		print "run " + str(run) + " PhyloTOL-cCleaner: new list of OGs to run generated"
		
		# If there  were mo trees with contamination stop loop of contamination removal (change restart to "n")
		if treesWcont == []: 
			print "run " + str(run) + " PhyloTOL-cCleaner: no more contamination, this was the final run"
			restart = 'n'
		
	else:
	
		# There are not results from PhyloTOL, then runs it for first time.
		print "run 0 PhyloTOL-cCleaner: runing PhyloTOL - pre-contamination removal \n\n"
		os.system("python phyloTOL.py ct")
		print "run 0 PhyloTOL-cCleaner: PhyloTOL done"