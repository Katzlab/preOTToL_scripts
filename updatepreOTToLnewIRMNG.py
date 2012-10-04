#updateOTToLnewIRMNG.py
'''
##########################################################################################
1) Download new IRMNG from http://www.cmar.csiro.au/datacentre/downloads/IRMNG_DWC.zip

2) Unzip IRMNG_DWC.zip and leave everything in file IRMNG_DWC

3) run updateOTToLnewIRMNG.py
 
 This script extracts valid species and genera from IRMNG and finds those not already in preOTToL
 It tries to add these if the parent or grandparent is in oTToL.  
 
 Currently writes out taxa if they need to be added to homonyms.  It's a work in progress

##########################################################################################
'''


import datetime
import os, re, sys
numlist = []
IRMDict = {}
PATH = 'IRMNG_DWC/'
##########################################################################################
def cleanIRMNG(IRMNG):
	infile = open(PATH + IRMNG,'r')
	outfile = open(PATH + 'Tabbed_' + IRMNG,'a')
	for line in infile:
		newline = ''
		flag = 0
		for char in line:
			if char == '"' and flag == 0:
				flag = 1
			elif char == '"' and flag == 1:
				flag = 0
			
			if char == ',' and flag == 1:
				newchar = '_'
			elif char == ',' and flag == 0:
				newchar = '\t'
			elif char == '"':
				newchar = ''
			else:
				newchar = char
		
			newline = newline + newchar
		outfile.write(newline)
##########################################################################################
def getValid(IRMNG):
	
	infile = open(PATH + 'Tabbed_' + IRMNG,'r')
	for line in infile:
		try:
			taxon = line.split('\t')[3].strip()
			taxnum = line.split('\t')[0].strip()
			IRMDict[taxon] = line
			IRMDict[str(taxnum)] = line #can query either by name or number
		except:
			print line
		if re.search('species\tvalid',line):
			out = open(PATH + 'IRMNGValidSpecies','a')
			out.write(line)
			out.close()
		elif re.search('genus\tvalid',line):
			out = open(PATH + 'IRMNGValidGenera','a')
			out.write(line)
			out.close()
	print IRMDict.keys()
	return IRMDict
##########################################################################################
def checkID(taxid,parid,taxidlist):
	if taxid in taxidlist:
		return 'taxon'
	elif parid not in taxidlist:
		return 'parent'
	else:
		return True
##########################################################################################

def findlastnum(filename, dbname):

	infile = open(filename,'r').readlines()
	for line in infile:
		numlist.append(line.split('\t')[0])
		
	numlist.sort()
	#print numlist
	return int(numlist.pop()) + 1
##########################################################################################
def mark(IRMDict, OTToL,date, nextnum, file):
	flag = 0
	infile = open(PATH + file,'r').readlines()
	infile2 = open(OTToL,'r').readlines()
	outfile = open('allNotinOTToL','a')
	taxonDict = {}
	parDict = {}
	added = []
	for line in infile2:
		taxid = line.split('\t')[0]
		parid = line.split('\t')[1]
		rank  = line.split('\t')[2]
		taxon = line.split('\t')[3]
		taxonDict[taxon] = line #line by taxon name in OTToL
		taxonDict[str(taxid)] = line #line by taxon number in OTToL
		parDict[taxon] = parid #parent name by taxon name in OTToL
		#IRMDict = line by taxon name in IRMNG (parent name = line.split('\t')[13], parent number = line.split('\t')[14])
		
	for line in infile: #in Valid Genera
		
		genus = line.split('\t')[3].strip()
		family = line.split('\t')[13].split()[0].strip()
		familynum = line.split('\t')[14].split()[0].strip()
		try:
			order = IRMDict[familynum].split('\t')[13].strip()
			print '.'
		except:
			print 'problem with order: ' + familynum + ',' + line
			order = ""
		
		try: #is taxon in OTToL?
			outfile2 = open('already_in','a')
			outfile2.write(taxonDict[genus])
			outfile2.close()			
		except: #if not...
			crap = open('maybeCrap.txt','r').readlines()
			if genus + '\n' in crap:
				out3 = open('tryingtoadd_possibleCrap','a')
				out3.write(genus + ',' + family + ',' + order + '\n')
				out3.close()				
			else:
				
				outfile.write(line)
				try: #is parent in OTToL?
					if re.search('_hom', taxonDict[family].split('\t')[2]): #if parent is a homonym, write out to check
						out3 = open('tryingtoaddtoHomonym','a')
						out3.write(genus + ',' + family + '\n')
						out3.close()					
					else: #if not a homonym, write out to lines 2 add
						out3 = open('lines2add','a')
						out3.write(str(nextnum) + '\t' + taxonDict[family].split('\t')[0] + '\tIRMNG_' + date + '_IRMid' + line.split('\t')[0] + '\t' + genus + '\t\tgenus\t' + date + '\n')
						out3.close()
						nextnum = nextnum + 1
				except: #parent not in Ottol-check grandparent
					try:
						if re.search('_hom', taxonDict[order].split('\t')[2]): #if parent is a homonym, write out to check
							out3 = open('tryingtoaddtoHomonym','a')
							out3.write(genus + ',' + family + ',' + order + '\n')
							out3.close()					
						else: #if not a homonym, write out family and genus to lines 2 add
							out3 = open('lines2add','a')
							if line.split('\t')[14] not in added: #fam already added
								#add family - if not already in lines2add
								out3.write(str(nextnum) + '\t' + taxonDict[order].split('\t')[0] + '\tIRMNG' + date + '_IRMid' + line.split('\t')[14] + '\t' + family + '\t\tfamily\t' + date + '\n')# not going to work--wrong number
								#add genus
								out3.write(str(nextnum + 1) + '\t' + str(nextnum) + '\tIRMNG_' + date + '_IRMid' + line.split('\t')[0] + '\t' + genus + '\t\tgenus\t' + date + '\n')					
								out3.close()
								nextnum = nextnum + 2
								added.append(line.split('\t')[14])
							else:
								flag = 1
								out5= open(PATH + 'addback','a')
								out5.write(line)
								out5.close()
								
					except:
						if sys.exc_info()[0] != "<type 'exceptions.KeyError'>":
							print sys.exc_info()[0]
						out2 = open('genera_ParentsNotInOTToL','a')
						out2.write(line)
						out2.close()
	taxonDict = add2OTToL(OTToL, taxonDict,'family')
	if flag == 1:
		mark(IRMDict, OTToL,date, nextnum, 'addback')
	
	outfile.close()
	return taxonDict
	##########################################################################################
def marksp(IRMDict, OTToL,date, nextnum, file):
	os.system('mv lines2add lines2add1')

	flag = 0
	infile = open(PATH + file,'r').readlines()
	infile2 = open(OTToL,'r').readlines()
	outfile = open('allNotinOTToL','a')
	taxonDict = {}
	parDict = {}
	added = []
	for line in infile2:
		taxid = line.split('\t')[0]
		parid = line.split('\t')[1]
		rank  = line.split('\t')[2]
		taxon = line.split('\t')[3]
		taxonDict[taxon] = line #line by taxon name in OTToL
		taxonDict[str(taxid)] = line #line by taxon number in OTToL
		parDict[taxon] = parid #parent name by taxon name in OTToL
		#IRMDict = line by taxon name in IRMNG (parent name = line.split('\t')[13], parent number = line.split('\t')[14])
		
	for line in infile: #in Valid Species
	
		genus = line.split('\t')[3].strip()
		species = line.split('\t')[4].strip()
		taxon = genus + ' ' + species
		genusnum = line.split('\t')[14].split()[0].strip()
		try:
			family = IRMDict[genusnum].split('\t')[13].strip()
			print '.'
		except:
			print 'problem with family: ' + genusnum + ',' + line
			order = ""
		
		try: #is taxon in OTToL?
			outfile2 = open('already_in','a')
			outfile2.write(taxonDict[taxon])
			outfile2.close()			
		except: #if not...
			crap = open('maybeCrap.txt','r').readlines()
			if genus + '\n' in crap:
				out3 = open('tryingtoadd_possibleCrap','a')
				out3.write(taxon + ',' + genus + ',' + family + '\n')
				out3.close()				
			else:
				
				outfile.write(line)
				try: #is parent in OTToL?
					if re.search('_hom', taxonDict[genus].split('\t')[2]): #if parent is a homonym, write out to check
						out3 = open('tryingtoaddtoHomonym','a')
						out3.write(taxon + ',' + genus + '\n')
						out3.close()					
					else: #if not a homonym, write out to lines 2 add
						out3 = open('lines2add','a')
						out3.write(str(nextnum) + '\t' + taxonDict[genus].split('\t')[0] + '\tIRMNG_' + date + '_IRMid' + line.split('\t')[0] + '\t' + taxon + '\t\tspecies\t' + date + '\n')
						out3.close()
						nextnum = nextnum + 1
				except: #parent not in Ottol-check grandparent
					try:
						if re.search('_hom', taxonDict[family].split('\t')[2]): #if parent is a homonym, write out to check
							out3 = open('tryingtoaddtoHomonym','a')
							out3.write(taxon + ',' + genus + ',' + family + '\n')
							out3.close()					
						else: #if not a homonym, write out genus and species to lines 2 add
							out3 = open('lines2add','a')
							if line.split('\t')[14] not in added: #gen already added

								#add family first check it isn't already in 'to be dded'
								out3.write(str(nextnum) + '\t' + taxonDict[family].split('\t')[0] + '\tIRMNG' + date + '_IRMid' + line.split('\t')[14] + '\t' + genus + '\t\tgenus\t' + date + '\n')# not going to work--wrong number
								#add genus
								out3.write(str(nextnum + 1) + '\t' + str(nextnum) + '\tIRMNG_' + date + '_IRMid' + line.split('\t')[0] + '\t' + taxon + '\t\tspecies\t' + date + '\n')					
								out3.close()
								nextnum = nextnum + 2
								added.append(line.split('\t')[14])
							else:
								flag = 1
								out5= open(PATH + 'addbacksp','a')
								out5.write(line)
								out5.close()
					except:
						if sys.exc_info()[0] != "<type 'exceptions.KeyError'>":
							print sys.exc_info()[0]
						out2 = open('genera_ParentsNotInOTToL','a')
						out2.write(line)
						out2.close()
	taxonDict = add2OTToL(OTToL, taxonDict,'genus')
	if flag == 1:
		marksp(IRMDict, OTToL,date, nextnum, 'addbacksp')	
	outfile.close()
	return taxonDict
##########################################################################################
def add2OTToL(OTToL, taxonDict, ranktoadd):
	print 'add2ottol'
	added = []
	os.system('cp ' + OTToL + ' ' + OTToL +   '_orig')
	outfile = open(OTToL,'a')
	for line in open('lines2add','r'):
		tax = line.split('\t')[3]
		taxid = line.split('\t')[0]
		parid = line.split('\t')[1]
		rank = line.split('\t')[-2]
		#print rank, ranktoadd
		if tax not in added and rank == ranktoadd:
			added.append(tax) #in case line is in file twice
			try:
				taxonDict[taxon] #make sure it isn't already in OTToL again
				errorlog = open('adderrorlog','a')
				errorlog.write('Duplicate taxon: ' + line)
				errorlog.close()
			except:				
				try: 
					taxonDict[str(taxid)] #make sure taxid hasn't been used already
					print 'Taxon id used: ' + line
					errorlog = open('adderrorlog','a')
					errorlog.write('Taxon id used: ' + line)
					errorlog.close() 				
				except:
					#print parid, taxonDict[str(parid)]
					try: 
						taxonDict[str(parid)] #make sure parid exists				
						outfile.write(line)
						taxonDict[str(taxid)] = line
						print 'adding'
					except:
						errorlog = open('adderrorlog','a')
						errorlog.write('No parent ID: ' + line)
						errorlog.close()										
		else:
			print '.'
	return taxonDict
##########################################################################################



def main():
	OTToL = raw_input('What is the latest OTToL? ')
#	date = raw_input('What is the download date for the latest OTToL? ')
	date = 'today'
#	OTToL = 'OTToL080912v2'
	for f in os.listdir(os.curdir + '/' +  PATH):
		if re.match('IRMNG_DWC',f) and not re.search('PROFILE',f):
			IRMNG = f
	nextnum = findlastnum(OTToL, 'IRMNG')

	#cleanIRMNG(IRMNG)
	IRMDict = getValid(IRMNG)
	for file in ['IRMNGValidGenera']:
		taxonDict = mark(IRMDict, OTToL,date, nextnum,file)

		taxonDict = add2OTToL(OTToL, taxonDict,'genus')
		#x = raw_input('add lines to OTToL and hit return to continue...')
		taxonDict = add2OTToL(OTToL, taxonDict,'species')
		#x = raw_input('add lines to OTToL and hit return to continue...')
	nextnum = findlastnum(OTToL, 'IRMNG')
	for file in ['IRMNGValidSpecies']:
		taxonDict = marksp(IRMDict, OTToL,date, nextnum,file)
		taxonDict = add2OTToL(OTToL, taxonDict,'genus')
		#x = raw_input('add lines to OTToL and hit return to continue...')
		taxonDict = add2OTToL(OTToL, taxonDict,'species')
		#x = raw_input('add lines to OTToL and hit return to continue...')
'''


'''
main()

	