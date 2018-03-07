# This script removes sequences according to specified rules in local databades (in each instance of the pipeline). 
# It also produces the list of removed sequences so that they can be used for removing in the ready to go folder. 

# input: 
# - Report of sister taxa
# - rules
# - folder of ncbiFiles
# - empty folder for new ncbiFiles

# Running:
# - Put all the imput files and folders in the same folder and run scrip with ruby: "ruby seqs2remove.rb"

# ruby seqs2remove.rb path2Files sisterReport rules seqs2remove_out nonHomologs 

path = ARGV[0]
report_summary = File.open(ARGV[1], 'r').readlines()
rules = File.open(ARGV[2], 'r').readlines()
sequences_contamination = File.open(ARGV[3], 'w')
ncbiFiles = path + '/ncbiFiles/'
system "mkdir " + path + "/newncbi/"
newncbi = path + '/newncbi/'
seqs2remove = Array.new
nonhomologs = File.open(ARGV[4], 'r').readlines()
total2remove = nonhomologs


count = 0
report_summary.each do |line|
	count += 1
	line = line.chomp
	line = line.split("\t")
	taxon = line[1]
	sequence = line[2]
	sister = line[3]

	rules.each do |rule|
		rule = rule.chomp
		rule = rule.split("\t")
		taxon_rule = rule[0]
		
		if taxon == taxon_rule
			contamination = rule[1..-1]	
			contamination.each do |taxon_contamination|

				if sister.include? taxon_contamination
					puts "contamination:\t" + sequence
					seqs2remove << sequence
					sequences_contamination.write(sequence + "\n")
				end
			end	
		end
	end
end

(total2remove << seqs2remove).flatten!

(Dir.open(ncbiFiles)).each do |ncbiFile|
	if ncbiFile.include? ".fasta"
		taxon = ncbiFile[0..9]
		to_remove = Array.new
		ncbisequences = File.open(ncbiFiles + ncbiFile, "r").readlines()
		newncbiTags = Array.new
		newncbiFile = File.open(newncbi + ncbiFile, "w")

		puts ncbiFile
	
#		seqs2remove.each do |seq2remove|
		total2remove.each do |seq2remove|
			seq2remove = seq2remove.gsub(/\n/, "")
			if seq2remove.include? taxon
				to_remove << seq2remove
			end
		end
		
		index = 0
		ncbisequences.each do |ncbisequence|
			if ncbisequence =~ /^>/
				tag = ncbisequence.gsub(/>|\n/, "")
				unless to_remove.include? tag
					newncbiFile.write(ncbisequence + ncbisequences[index + 1])
				else
					puts "removed: " + ncbisequence
					puts "removed: " + ncbisequences[index + 1]
				end
			end
			index += 1
		end
	end
end

system "rm -r " + ncbiFiles
system "mv " + newncbi + "\t" + ncbiFiles
