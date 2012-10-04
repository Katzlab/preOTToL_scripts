##########################################################################################
# Goal: to make a file from the CoL database that includes just the taxonomy
# reforming the taxonomy list to mirror our ideas of the tree (i.e. changing 'Animalia' 
#to 'Eukaryots, Opisthokonta, Metazoa' and renaming all the 'Chromista' and 'Protozoa'
# taxa.
# Second method, extract the species not already in OTToL 
# 
#
##########################################################################################
import datetime
import os, re
numlist = []
##########################################################################################

def findlastnum(filename, dbname):

	infile = open(filename,'r').readlines()
	for line in infile:
		db = line.split('\t')[2]
		if re.search(dbname,db):
			numlist.append(line.split('\t')[0])
		
	numlist.sort()
	#print numlist
	return int(numlist.pop()) + 1
##########################################################################################
	
def parsetextfromCoL():
	infile = open('col/taxa.txt','r') #taxa.txt is file downloaded from CoL with all taxa
	outfile1 = open('acceptedNames','a')
	outfile2 = open('provisionallyAcceptedNames','a')
	count = 0
	pcount = 0
	for line in infile:
		if not re.search('infraspecies',line):
			if re.search('accepted',line) and re.search('species',line):
				if not re.search('provisionally',line):
					outfile1.write(line)
					count = count + 1
				else:
					outfile2.write(line)
					pcount = pcount + 1
	#print 'accepted names: '+ str(count)
	#print 'provisionally accepted names: '+ str(pcount)
##########################################################################################

def renameCoL(f):
	outfile = open('taxa_' + f,'w')
	errorout = open('viruses_and_other_prblems','a')
	infile = open(f,'r').readlines()
	newtaxlist = []
	for line in infile:
		taxalist = line.split('\t\t')[2]
		#print taxalist
		sp = taxalist.split()[1].strip(',') 
		
		if taxalist.split('\t')[1] == 'Archaea':
			newline = taxalist.split('\t')[1:]
		elif taxalist.split('\t')[1] == 'Bacteria':
			newline = taxalist.split('\t')[1:]
		elif taxalist.split('\t')[1] == 'Animalia':
			newline = re.sub('Animalia','Eukaryota\tOpisthokonta\tMetazoa',taxalist).split('\t')[1:] 
		elif taxalist.split('\t')[1] == 'Fungi':
			newline = re.sub('Fungi','Eukaryota\tOpisthokonta\tFungi',taxalist).split('\t')[1:] 
		elif taxalist.split('\t')[1] == 'Plantae':
			newline = re.sub('Plantae','Eukaryota\tPlantae',taxalist).split('\t')[1:] 
		elif taxalist.split('\t')[1] == 'Protozoa':
			newline = renameProt(taxalist) #.split('\t')[1:] 
		elif taxalist.split('\t')[1] == 'Chromista':
			newline = renameProt(taxalist) #.split('\t')[1:] 
		else:
			if taxalist.split('\t')[1] == 'Viruses' or re.search('viruses',taxalist):
				newline = 'Virus'
			else:
				errorout = open('viruses_and_other_prblems','a')
				errorout.write('problem with 1 ' + line)
				errorout.close()
				newline = ''
		if newline != '' or newline != 'Virus':
			try:
				check(newline)
			except:
				print line, newline

				print 'problem with check(newline) ' + str(printlist)
				errorout = open('viruses_and_other_prblems','a')
				errorout.write('problem with check(newline) ' + str(printlist) + '\n')
				errorout.close()
			try:
				printlist = newline  + [sp]
				try:
					assert re.search('[A-Z]',printlist[-2][0]) and re.search('[a-z]',printlist[-1][0])
					for item in printlist:	
						if re.search(',',item):
							print str(printlist)
							errorout = open('viruses_and_other_prblems','a')
							errorout.write('problem with str(printlist) ' + str(printlist) + '\n')
							errorout.close()					
						else:
							outfile.write(item + '\t')
			
					outfile.write('\n')
				except:
					errorout = open('viruses_and_other_prblems','a')
					errorout.write('problem with genera and species ' + str(line))
					errorout.close()					
			except:
				errorout = open('viruses_and_other_prblems','a')
				errorout.write('problem with printlist ' + str(line))
				errorout.close()
				
				
##########################################################################################
				
def renameProt(taxlist): #hash table built from our understanding of the tree
	myhash = {}
	taxalist = taxlist.split('\t')[1:] #get rid of preceding genus species

	myhash['Protozoa','Acritarcha','Not assigned'] = ['Eukaryota','EE','Acritarcha','Not assigned']
	myhash['Protozoa','Apicomplexa','Conoidasida'] = ['Eukaryota','SAR','Alveolata','Apicomplexa','Conoidasida']
	myhash['Protozoa','Apicomplexa','Not assigned'] = ['Eukaryota','SAR','Alveolata','Apicomplexa','Not assigned']
	myhash['Protozoa','Cercozoa','Chlorarachniophyceae'] = ['Eukaryota','SAR','Rhizaria','Cercozoa','Chlorarachniophyceae']
	myhash['Protozoa','Cercozoa','Phytomyxea'] = ['Eukaryota','SAR','Rhizaria','Cercozoa','Phytomyxea']
	myhash['Protozoa','Choanozoa','Mesomycetozoea'] = ['Eukaryota','Opisthokonta','Choanozoa','Mesomycetozoea']
	myhash['Protozoa','Choanozoa','Not assigned'] = ['Eukaryota','Opisthokonta','Choanozoa','Not assigned']
	myhash['Protozoa','Ciliophora','Ciliatea'] = ['Eukaryota','SAR','Alveolata','Ciliophora','Ciliatea']
	myhash['Protozoa','Dinophyta','Dinophyceae'] = ['Eukaryota','SAR','Alveolata','Dinophyta','Dinophyceae']
	myhash['Protozoa','Dinophyta','Ebriophyceae'] = ['Eukaryota','SAR','Alveolata','Dinophyta','Not assigned']
	myhash['Protozoa','Dinophyta','Not assigned'] = ['Eukaryota','Excavata','Euglenozoa','Euglenida']
	myhash['Protozoa','Euglenozoa','Euglenida'] = ['Eukaryota','Excavata','Euglenozoa','Euglenida']
	myhash['Protozoa','Euglenozoa','Trypanosomatidae'] = ['Eukaryota','Excavata','Euglenozoa','Trypanosomatidae']
	myhash['Protozoa','Flagellata','Not assigned'] = ['Eukaryota','Excavata','Flagellata','Not assigned']
	myhash['Protozoa','Mycetozoa','Acrasiomycetes'] = ['Eukaryota','Amoebozoa','Mycetozoa','Acrasiomycetes']
	myhash['Protozoa','Mycetozoa','Dictyosteliomycetes'] = ['Eukaryota','Amoebozoa','Mycetozoa','Dictyosteliomycetes']
	myhash['Protozoa','Mycetozoa','Myxomycetes'] = ['Eukaryota','Amoebozoa','Mycetozoa','Myxomycetes']
	myhash['Protozoa','Mycetozoa','Protosteliomycetes'] = ['Eukaryota','Amoebozoa','Mycetozoa','Protosteliomycetes']
	myhash['Protozoa','Mycetozoa','Not assigned'] = ['Eukaryota','Amoebozoa','Mycetozoa']
	myhash['Protozoa','Not assigned','Acantharia'] = ['Eukaryota','SAR','Rhizaria','Acantharia']
	myhash['Protozoa','Not assigned','Filosia'] = ['Eukaryota','SAR','Rhizaria','Filosia']
	myhash['Protozoa','Not assigned','Granuloreticulosea'] = ['Eukaryota','SAR','Rhizaria','Granuloreticulosea']
	myhash['Protozoa','Not assigned','Haplosporea'] = ['Eukaryota','SAR','Rhizaria','Haplosporea']
	myhash['Protozoa','Not assigned','Heliozoa','Actinophryida'] = ['Eukaryota','SAR','Stramenopile','Actinophryidae']
	myhash['Protozoa','Not assigned','Heliozoa','Centrohelida'] = ['Eukaryota','EE','Centrohelida']
	myhash['Protozoa','Not assigned','Heliozoa','Desmothothoracida'] = ['Eukaryota','SAR','Rhizaria','Desmothoracida']
	myhash['Protozoa','Not assigned','Heliozoa','Desmothoracida'] = ['Eukaryota','SAR','Rhizaria','Desmothoracida']
	myhash['Protozoa','Not assigned','Lobosa'] = ['Eukaryota','Amoebozoa','Lobosa']
	myhash['Protozoa','Not assigned','Not assigned','Jakobaceae'] = ['Eukaryota','Excavata','Jakobid']
	myhash['Protozoa','Not assigned','Sporozoa'] = ['Eukaryota','SAR','Alveolata','Apicomplexa']
	myhash['Protozoa','Parabasalia','Not assigned'] = ['Eukaryota','Excavata','Parabasalia']
	myhash['Protozoa','Percolozoa','Heterolobosea'] = ['Eukaryota','Excavata','Heterolobosea']
	myhash['Protozoa','Sarcomastigophora','Phytomastigophora'] = ['Eukaryota','SAR','Alveolata','Dinoflagellate']
	myhash['Protozoa','Sarcomastigophora','Zoomastigophora','Diplomonadida'] = ['Eukaryota','Excavata','Fornicata']
	myhash['Protozoa','Sarcomastigophora','Zoomastigophora','Trichomonadida'] = ['Eukaryota','Excavata','Parabasalia']
	myhash['Protozoa','Xenophyophora','Psamminida'] = ['Eukaryota','SAR','Rhizaria','Xenophyophora','Psamminida']
	myhash['Protozoa','Xenophyophora','Stannomida'] = ['Eukaryota','SAR','Rhizaria','Xenophyophora','Stannomida']
	myhash['Protozoa','Sarcomastigophora','Polycystina'] = ['Eukaryota','SAR','Rhizaria','Radiolaria']
	myhash['Protozoa','Myzozoa','Perkinsea'] = ['Eukaryota','EE','Perkinsus']
	myhash['Chromista','Cryptophyta','Cryptophyceae'] = ['Eukaryota','EE','Cryptophyta','Cryptophyceae']
	myhash['Chromista','Haptophyta','Not assigned'] = ['Eukaryota','EE','Haptophyta','Not assigned']
	myhash['Chromista','Haptophyta','Prymnesiophyceae'] = ['Eukaryota','EE','Haptophyta','Prymnesiophyceae']
	myhash['Chromista','Hyphochytriomycota','Hyphochytriomycetes'] = ['Eukaryota','SAR','Stramenopile','Hyphochytriomycetes']
	myhash['Chromista','Labyrinthista','Labyrinthulea'] = ['Eukaryota','SAR','Stramenopile','Labyrinthulea']
	myhash['Protozoa','Labyrinthista','Labyrinthulea'] = ['Eukaryota','SAR','Stramenopile','Labyrinthulea']
	myhash['Chromista','Ochrophyta','Bodonophyceae'] = ['Eukaryota','SAR','Stramenopile','Bodonophyceae']
	myhash['Chromista','Ochrophyta','Chrysophyceae'] = ['Eukaryota','SAR','Stramenopile','Chrysophyceae']
	myhash['Chromista','Ochrophyta','Coscinodiscophyceae'] = ['Eukaryota','SAR','Stramenopile','Coscinodiscophyceae']
	myhash['Chromista','Ochrophyta','Craspedophyceae'] = ['Eukaryota','SAR','Stramenopile','Craspedophyceae']
	myhash['Chromista','Ochrophyta','Dictyochophyceae'] = ['Eukaryota','SAR','Stramenopile','Dictyochophyceae']
	myhash['Chromista','Ochrophyta','Eustigmatophyceae'] = ['Eukaryota','SAR','Stramenopile','Eustigmatophyceae']
	myhash['Chromista','Ochrophyta','Fragilariophyceae'] = ['Eukaryota','SAR','Stramenopile','Fragilariophyceae']
	myhash['Chromista','Ochrophyta','Hexamitophyceae'] = ['Eukaryota','SAR','Stramenopile','Hexamitophyceae']
	myhash['Chromista','Ochrophyta','Phaeophyceae'] = ['Eukaryota','SAR','Stramenopile','Phaeophyceae']
	myhash['Chromista','Ochrophyta','Raphidophyceae'] = ['Eukaryota','SAR','Stramenopile','Raphidophyceae']
	myhash['Chromista','Ochrophyta','Synurophyceae'] = ['Eukaryota','SAR','Stramenopile','Synurophyceae']
	myhash['Chromista','Ochrophyta','Xanthophyceae'] = ['Eukaryota','SAR','Stramenopile','Xanthophyceae']
	myhash['Chromista','Oomycota','Not assigned'] = ['Eukaryota','SAR','Stramenopile','Not assigned']
	myhash['Chromista','Oomycota','Oomycetes'] = ['Eukaryota','SAR','Stramenopile','Oomycetes']
	myhash['Chromista','Sagenista','Bicosoecophyceae'] = ['Eukaryota','SAR','Stramenopile','Bicosoecophyceae']
	myhash['Chromista','Ochrophyta','Pelagophyceae'] = ['Eukaryota','SAR','Stramenopile','Pelagophyceae']
	myhash['Chromista','Ochrophyta','Bolidophyceae'] = ['Eukaryota','SAR','Stramenopile','Bolidophyceae']
	myhash['Chromista','Ochrophyta','Pinguiophyceae'] = ['Eukaryota','SAR','Stramenopile','Pinguiophyceae']
	myhash['Chromista','Not assigned','Schizocladiophyceae'] = ['Eukaryota','SAR','Stramenopile','Schizocladiophyceae']
	myhash['Chromista','Ochrophyta','Pinguiophyceae'] = ['Eukaryota','SAR','Stramenopile','Pinguiophyceae']
	myhash['Chromista','Not assigned','Developayella'] = ['Eukaryota','SAR','Stramenopile','Developayella']

	for key in myhash.keys():
		newtaxlist = myhash[key]
		keylist = key
		if all(x in taxalist for x in keylist):
			for y in keylist:
				taxalist.remove(y) #remove old list
			for item in taxalist:
				newtaxlist.append(item)
			#print newtaxlist
			return newtaxlist
			
##########################################################################################
def mark_notinOTToL(OTToL):
	i = 0
	infile = open('allCoLrenamed_taxa','r').readlines()
	infile2 = open(OTToL,'r').readlines()
	outfile = open('new_sp_2add2OTToL','a')
	taxonDict = {}
	for line in infile2:
		taxid = line.split('\t')[0]
		parid = line.split('\t')[1]
		taxon = line.split('\t')[3]
		taxonDict[taxon] = line 
	
	
	
	for line in infile:
		try:
			assert re.search('[A-Z]',line.split()[-2][0]) and re.search('[a-z]',line.split()[-1][0])
			gensp = line.split()[-2] + ' ' + line.split()[-1]
		except:
			outfile2 = open('error_entering','a')
			outfile2.write(line)
			outfile2.close()
			gensp = ''
		try:
			outfile2 = open('already_in','a')
			outfile2.write(taxonDict[gensp])
			outfile2.close()			
		except:
			if gensp != '':
				outfile.write(line)
	
	outfile.close()
##########################################################################################

def check(line):
	
	#error = open('errorlog','a')
	#infile = open('taxa_' + f,'r')
	#for line in infile:
	if line == 'Virus':
		return
	if line[0] not in ['Eukaryota','Bacteria','Archaea']:
		error = open('errorlog','a')
		error.write(line)
		error.close()
	if line[0] == 'Eukaryota':
		if line[1] not in ['Opisthokonta','Plantae','SAR','Amoebozoa','Excavata','EE']:
			error = open('errorlog','a')
			error.write(line)
			error.close()

	if line[0] == 'Bacteria':
		if line[1] not in ['Actinobacteria','Cyanobacteria','Acidobacteria','Aquificae','Bacteroidetes','Chlamydiae','Chlorobi','Chloroflexi','Chrysiogenetes','Deferribacteres','Deinococcus-thermus','Dictyoglomi','Fibrobacteres','Firmicutes','Fusobacteria','Gemmatimonadetes','Lentisphaerae','Nitrospira','Planctomycetes','Proteobacteria','Spirochaetes','Thermodesulfobacteria','Thermomicrobia','Thermotogae','Verrucomicrobia','Flavobacteria','Sphingobacteria','Ochrophyta','Deinococci','Bacilli','Clostridia','Mollicutes','Bacteria','Alphaproteobacteria','Betaproteobacteria','Deltaproteobacteria','Epsilonproteobacteria','Gammaproteobacteria','Verrucomicrobiae']:
			error = open('errorlog','a')
			error.write(line)
			error.close()

	if line[0] == 'Archaea':
		if line[1] not in ['Crenarchaeota','Euryarchaeota']:
			error = open('errorlog','a')
			error.write(line)
			error.close()
##########################################################################################

def cleanup(toKEEP):
	for f in os.listdir(os.curdir):
		if f not in toKEEP:
			os.system('mv ' + f + ' col_extra_files...check_and_discard')
			
##########################################################################################
def mergesp(date, OTToL,file,newtxid):
	infile1 = open(OTToL,'r').readlines()
	infile2 = open(file,'r').readlines()
	outfile = open('to_merge','w')
	outfile2 = open('genera_2add2OTToL','a')
	genusDict = {}
	
	for line in infile1:
		#try:
		if line.split('\t')[-2] == 'genus' or line.split('\t')[-2] == 'gen.':
			genus = line.split('\t')[3].split()[0]
			txid = line.split('\t')[0]
			genusDict[genus] = txid
		#except:
		#	print line
	for line in infile2:
		if re.search('Not assigned',line):
			unassignedout = open('Not_assigned','a')
			unassignedout.write(line)
			unassignedout.close()
		else:
			genus2add = line.split()[-2]
			species2add = line.split()[-1]
	
			if genus2add in genusDict.keys():
				newparid = genusDict[genus2add]
				newtxid = newtxid + 1
				today = datetime.datetime.now().strftime('%m_%d_%y')

				newline = str(newtxid) + '\t' + str(newparid) + '\tCoL_' + date + '\t' + genus2add + ' ' + species2add + '\t\tspecies\t' + today + '\n'
			
				outfile.write(newline)
			else:
				outfile2.write(line)	
	outfile.close()
	outfile2.close()
	return newtxid
##########################################################################################
def mergegen(date, OTToL,file,newtxid):
	infile1 = open(OTToL,'r').readlines()
	infile2 = open(file,'r').readlines()
	outfile = open('to_merge','a')
	outfile2 = open('stillNotinOTToL','a')
	familyDict = {}
	addedList= []	
	for line in infile1:
		#try:
		if line.split('\t')[-2] != 'species' and line.split('\t')[-2] != 'subspecies' and line.split('\t')[-2] != 'genus':
			try:
				family = line.split('\t')[3].split()[0]
			except:
				family = line.split('\t')[3]
			txid = line.split('\t')[0]
			familyDict[family] = txid
		#except:
		#	print line
	for line in infile2:
			
		genus2add = line.split()[-2]
		fam2add = line.split()[-3]
		
		if genus2add.strip() not in addedList:
			addedList.append(genus2add.strip())
			if fam2add in familyDict.keys():
				newparid = familyDict[fam2add]
				newtxid = newtxid + 1
				today = datetime.datetime.now().strftime('%m_%d_%y')

				newline = str(newtxid) + '\t' + str(newparid) + '\tCoL_' + date + '\t' + genus2add +  '\t\tgenus\t' + today + '\n'
			
				outfile.write(newline)
			else:
				outfile2.write(line)	
	outfile.close()
	outfile2.close()
	add(OTToL,'to_merge')
	os.system('cat ' +  OTToL + ' toAdd_' + OTToL + '+to_merge > ' + OTToL + 'genadded')  #FIXED THIS TO LOOK FOR DUPLICATES/HOMONYMS
	os.system('cp to_merge to_merge_1')
	os.system('mv ' + file  + ' ' + file + '_1')
	mergesp(date, OTToL + 'genadded',file + '_1',newtxid+1 )

##########################################################################################
def add(file,file2):
	infile1 = open(file,'r').readlines()
	infile2 = open(file2,'r').readlines()
	outfile = open('toAdd_' + file + '+' + file2,'w')
	outfile2 = open('dups_2check_before_adding2_' + file + '+' + file2,'w')
	outfile3 = open('homonyms_2check_before_adding2_' + file + '+' + file2,'w')
	taxlist = []
	homlist = []
	taxidlist = []
	taxlist2 = []
	for line in infile1:
		tax = line.split('\t')[3]
		taxid = line.split('\t')[0]
		db = line.split('\t')[2]
		taxlist.append(tax)
		taxidlist.append(taxid)
		if re.search('_hom',db):
			homlist.append(tax)
	#print 'taxlist made'
	
	for line in infile2:
		tax = line.split('\t')[3]
		taxid = line.split('\t')[0]
		parid = line.split('\t')[1]
		if tax not in taxlist2:
			taxlist2.append(tax)
			if tax not in taxlist:
				if checkID(taxid,parid,taxidlist) == True:
					outfile.write(line)
				elif checkID(taxid,parid,taxidlist) == 'parent':
					errorlog = open('adderrorlog','a')
					errorlog.write('No Parent: ' + line)
					errorlog.close()
				elif checkID(taxid,parid,taxidlist) == 'taxon':
					errorlog = open('adderrorlog','a')
					errorlog.write('TaxID exists: ' + line)
					errorlog.close()
			else:
				if tax in homlist:
					outfile3.write(line)
				else:
					outfile2.write(line)
		else:
			errorlog = open('adderrorlog','a')
			errorlog.write('Trying to add twice: ' + line)
			errorlog.close()			

def checkID(taxid,parid,taxidlist):
	if taxid in taxidlist:
		return 'taxon'
	elif parid not in taxidlist:
		return 'parent'
	else:
		return True
##########################################################################################


def main():
#	OTToL = raw_input('What is the latest OTToL? ')
#	date = raw_input('What is the download date for the latest OTToL? ')
	date = 'today'
	OTToL = 'OTToL080912v2'
	parsetextfromCoL()
	for f in ['acceptedNames','provisionallyAcceptedNames']:
		renameCoL(f)
		check(f)
	os.system('cat taxa_provisionallyAcceptedNames taxa_acceptedNames > allCoLrenamed_taxa')
	mark_notinOTToL(OTToL)
	os.system('mkdir col_extra_files...check_and_discard')
	toKEEP = [OTToL,'new_sp_2add2OTToL','col','col_extra_files...check_and_discard','updateOTToLnewCoL.py']
	cleanup(toKEEP)

	##############################
	nextnum = findlastnum(OTToL, 'CoL')
	nextnum = mergesp(date, OTToL,'new_sp_2add2OTToL',nextnum)
	
	mergegen(date, OTToL,'genera_2add2OTToL',nextnum)
	
	add(OTToL + 'genadded','to_merge')
	os.system('cat ' + OTToL + 'genadded toAdd_' + OTToL + 'genadded+to_merge   > ' + OTToL + 'final') 
	toKEEP = [OTToL + 'final','col','col_extra_files...check_and_discard','updateOTToLnewCoL.py','updateOTToLnewCoL_README']
	cleanup(toKEEP)
main()

	
