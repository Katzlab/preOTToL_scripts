#This script checks OToL for several problems that can occur and outputs several files:

#<OTToLName>_duplicates: Lines not marked as homonym with duplicate names in field 3 
#QuickListofParentlessTaxa_<OTToLName>: Lines from taxa that do not have parents (can return all descendents of parentless taxa, at user request.)
#<OTToLName>_problems: several small problems:
#	non-unique taxon id number
#	life and cellular life not just Euk, Bact, Arch
#	Taxid = Parid
#	Taxid, Parid not numeric
#	More or fewer than 6 tabs
#<OTToLName>_spproblems: speceis problems:
#	Binomial names not labeled as species
#	Species that have parents that are not labeled genus
##########################################################################################

import re
removeList = []
iddict = {}
linedict = {}
childdict = {}


def makeDicts(x):
	iddict = {}
	linedict = {}
	infile = open(x,'r').readlines()
	
	for line in infile:
		try:
			rank =  line.split('\t')[-2]
			taxid =  line.split('\t')[0]
			parid = line.split('\t')[1]
			db =  line.split('\t')[2]
			taxon =  line.split('\t')[3]
			
				
			try:
				childdict[parid].append(taxid)
			except:
				childdict[parid] = []
				childdict[parid].append(taxid)
			try:
				iddict[taxon].append(taxid)
			except:
				iddict[taxon] = []
				iddict[taxon].append(taxid)	
			linedict[taxid] = line


		
		except:
			print line

	return iddict,linedict,childdict
	
def getparentlessquick(x,linedict):
	outfile = open('QuickListofParentlessTaxa_' + x,'w')
	parentlessList = []
	for line in open(x,'r'):
		parid =  line.split('\t')[1]
		taxid =  line.split('\t')[0]
		taxon =  line.split('\t')[3]
		try:
			parent = linedict[parid]
		except:
			if taxid != '2822864':
				parentlessList.append(taxid)
				outfile = open('QuickListofParentlessTaxa_' + x,'a')
				outfile.write(line)
				outfile.close()
	try:
		return parentlessList
	except:
		print 'no parentless taxa in this file'
		
			
def findAllChildren(x,iddict,childdict,linedict):
	parentlessList = getparentlessquick(x,linedict) #list of taxon ids without parents
	i = 0
	
	#print parentlessList
	for parentlessid in parentlessList:
		if parentlessid != '2822864':
			#print parentlessid, childdict[parentlessid]
			removelist = makeRemoveList(parentlessid,childdict)
			
	outfile= open('ParentlessTaxa_' + x,'w')	
	for item in removelist:		
		outfile.write(linedict[item])
	outfile.close()

	
	
def makeRemoveList(parentlessid,childdict): #find children of parentless taxon and add them to list to be removed
	removeList.append(parentlessid)
	if parentlessid in childdict.keys():
		for child in childdict[parentlessid]:
			#removeList.append(child)
			makeRemoveList(child,childdict)

	return removeList

	

			
def findDups(x,iddict,linedict):
	outfile2 = open(x + '_duplicates','w')
	for taxon in iddict.keys():
		if len(iddict[taxon]) > 1:
			for id in iddict[taxon]:
				if not re.search('_hom',linedict[id].split('\t')[2]):
					outfile2 = open(x + '_duplicates','a')
					outfile2.write(linedict[id])
					outfile2.close()
	
	

def checktabs(x,childdict):
	infile = open(x,'r').readlines()
	outfile3 = open(x + '_problems','w')
	taxidlist = []
	for line in infile:
		taxid =  line.split('\t')[0]
		parid = line.split('\t')[1]
		if taxid in taxidlist:
			outfile3.write(str(taxid) + 'is not unique')
		else:
			taxidlist.append(taxid)
		if parid == 2822864 and taxid != 2823207:
			outfile3.write('life has too many children!')
		if parid == 2823207 and taxid not in [2828118,2823208,2823470]:
			outfile3.write('life has too many children!')
		if taxid == parid:
			outfile3.write('bad ids!: ' + line)
		try:
			x = line.split('\t')[7] # line doesn't have > 6 tabs
			outfile3.write('line too long: ' + line)
		except:
			try: 
				x = line.split('\t')[6] # line doesn't have < 6 tabs
			except:
				outfile3.write('line too short: ' + line)
			try:
				a = int(line.split('\t')[0])
				b = int(line.split('\t')[1]) #id and parid are numbers
			except:
				if line.split('\t')[0] != '2822864':
					outfile3.write('check id numbers: ' + line)
				
	
def checkSp(x,linedict):
	infile = open(x,'r').readlines()
	outfile4 = open(x + '_spproblems','w')	
	parlist = []	
	nameList = ['Unassigned','Other','Unnamed','Peripheral','Fossil','group','i','ii','Residual','Core','Uncertain','complex','Clade','clade','cluster','lineage','incertae']
	for line in infile:
		#print linedict.keys()#[line.split('\t')[1]]
		name = line.split('\t')[3]
		rank = line.split('\t')[-2]
		#try:
		if len(name.split()) == 2:
			g = name.split()[0]	
			s = name.split()[1]	
			if len(name.split()) == 2 and re.match('[A-Z]',g[0]) and re.match('[a-z]',s[0]):
				if rank != 'species' and g not in nameList and s not in nameList:
					if rank != s:
						outfile4.write('1:' + line)
				elif rank == 'species' and g not in nameList and s not in nameList:
					#print linedict[line.split('\t')[1]].split('\t')[-2]
					if linedict[line.split('\t')[1]].split('\t')[-2] != 'genus': #if the rank of the parent isn't genus
						#print linedict[line.split('\t')[1]].split('\t')[-2]
						outfile4.write(linedict[line.split('\t')[1]].split('\t')[-2] + ': ' + line.strip() + ':' + linedict[line.split('\t')[1]])
					else:
						a = 'a'
		#except:
		#	a = 'a'

	
def main():
	
	
	x = raw_input('What file do you want to check? ')
	try:
		o = open(x,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()
	
	y = raw_input('Do you want to check for duplicate genera and species? y/n ')
	try:
		assert y[0] == 'y' or y[0] == 'n'
	except:
		print 'you must enter y or n.  Please try again.'
		main()
	
	z = raw_input('Do you want to check for parentless taxa? y/n ')
	try:
		assert z[0] == 'y' or z[0] == 'n'
	except:
		print 'you must enter y or n.  Please try again.'
		main()
	if z[0] == 'y':
		a = raw_input('Do you want a quick list of parentless taxa or a slow list (this can take up to 24 hours) of parentless taxa and all their decendents? q/s ')
		try:
			assert  a[0] == 's' or a[0] == 'q'	
		except:
			print 'you must enter s or q.  Please try again.'
			main()	
	
	iddict,linedict,childdict = makeDicts(x)
	if y[0] == 'y':
		findDups(x,iddict,linedict)
	try:
		if a[0] == 's':
			findAllChildren(x,iddict,childdict,linedict)
		elif a[0] == 'q':
			getparentlessquick(x,linedict)
	except:
		pass
	checktabs(x,childdict) 
	checkSp(x,linedict)

main()