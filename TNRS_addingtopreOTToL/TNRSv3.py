###################################################
#a preliminary script using ncbi eutils to deal with
#taxon name reconciliation when adding trees
#to open tree
#v3 asks for an input table and makes a file of OTToL-formatted lines
# preOTToL and the taxonomy table must be in the same directory
###################################################

from Bio import Entrez 
Entrez.email = ""  #Change
import re
import datetime
outfile = open('Taxa_In_OTToL.txt','a')

def makeDicts(x):
	print 'Processing preOTToL....'
	parDict = {}
	lineDict = {}
	taxDict = {}
	for line in open(x,'r').readlines():
		taxid =  line.split('\t')[0]
		parid = line.split('\t')[1]
		taxon = line.split('\t')[3]
		
		parDict[taxid] = parid
		lineDict[taxid] = line
		try:
			taxDict[taxon].append(line)
		except:
			taxDict[taxon] = []
			taxDict[taxon].append(line)
		
	print 'Dictionaries made.'
	return parDict, lineDict, taxDict 
		
		
		
		
def getNCBIName(x,query,parDict, par, lineDict,taxDict): 
###################################################
#uses ncbi espell to find mis-spellings and then summary to get scientific name
#from common name (i.e. Eutheria not placental)
#If not found, taxon will need to be added to OTToL
###################################################
	record = Entrez.read(Entrez.espell(term = query, db = 'taxonomy'))
	try:
		try: 
			record2 = Entrez.read(Entrez.esearch(term = record['CorrectedQuery'], db = 'taxonomy'))
		except:
			record2 = Entrez.read(Entrez.esearch(term = query, db = 'taxonomy'))

		flag = 0
		for taxid in record2['IdList']:
	
			record3 = Entrez.read(Entrez.esummary(id = taxid, db = 'taxonomy'))
			if query != record3[0]['ScientificName']:
			
				ans = raw_input('Your list contains ' + query + '. Do you mean ' + record3[0]['ScientificName'] + '? ' )

				if ans[0] == 'y':
					flag = 1
					searchOTToL(x, par,record3[0]['ScientificName'],parDict, lineDict, taxDict)
	except:
		print 'problem accessing ncbi. '
	if flag == 0:
		print 'The taxon: ' + query + ' is not in OTToL'
		out2 = open('Taxa_not_in_OTToL.txt','a')
		out2.write(query + '\n')
		out2.close()
		
def searchOTToL(x,query, par,parDict, lineDict, taxDict):
###################################################
#Searches OTToL for the names on the given list
#calls getHom() if not found if the taxon name is marked homonym in OTToL
#calls getNCBIName() if not found.
#queries user if parent in input table is different from parent in OTToL
###################################################
	print '.'
	flag = 0
	homList = []
	for line in open(x,'r').readlines():
		taxid = line.split('\t')[0]
		taxon = line.split('\t')[3]
		if line.split('\t')[3] == query:
			flag = 1
			#print line
			if re.search('_hom',line.split('\t')[2]):
				homtax = getHom(x,taxon,parDict, lineDict, taxDict)
				outfile.write(homtax + ',' + lineDict[homtax].split('\t')[3] + ',' + lineDict[parDict[homtax]].split('\t')[3] + '\n')
				return
			else:
				try:
					if par != lineDict[parDict[taxid]].split('\t')[3]:
						ans = raw_input( 'You have ' + line.split('\t')[3] + ' with the parent ' + par + '. Do you mean the taxon ' + line.split('\t')[3] + ' whose parent in pre-OTToL is: ' + lineDict[parDict[taxid]].split('\t')[3] + ' (y/n)? ')
						if ans[0] == 'y':
							outfile.write(taxid + ',' + line.split('\t')[3] + ',' + lineDict[parDict[taxid]].split('\t')[3] + '\n')
							return
						else:
							getNCBIName(x,query,parDict, par,lineDict,taxDict)
					else:

						outfile.write(taxid + ',' + line.split('\t')[3] + ',' + lineDict[parDict[taxid]].split('\t')[3] + '\n')
						return
						
				except:
					outfile.write(taxid + ',' + line.split('\t')[3] + ',no parent\n')
					return
	if flag == 0:
		getNCBIName(x,query,parDict, par ,lineDict,taxDict)

def getHom(x, taxon, parDict, lineDict, taxDict):
###################################################
#Searches OTToL for the parent names of the homonym
#asks user to choose between taxon with one parent or the other
###################################################
	homList = []
	i = 0		
	print taxon + ' is a homonym. These are the parents of the different homonymic taxa: '
	
	for line in taxDict[taxon]: #open(x,'r').readlines():
		
		if line.split('\t')[3] == taxon:
			i = i + 1
			print str(i) + ')' + lineDict[parDict[line.split('\t')[0]]].split('\t')[3]
			homList.append((lineDict[parDict[line.split('\t')[0]]].split('\t')[3], line.split('\t')[0]))
	q = input('Do you want the one that has one of these as a parent? (type in number next to your selection) ')
	r = raw_input('you selected ' + homList[q - 1][0] + '. Is that right? (y/n) ')
	if r == 'y':
		return homList[q - 1][1]
	else:
		print 'try again. '
		getHom(x, taxon, parDict, lineDict, taxDict)

###################################################
#From the taxonomy table entered by user, gets list of taxa and dictionary of parents by taxon
###################################################
		
def querylist(o): #from table, get uniquelist of taxa in the tree
	tablepar = {}
	taxlist = []
	for line in o:
		if line[0] != '#' and line != '\n':
			try:
				tax = line.split('\t')[0].strip()
				par = line.split('\t')[1].strip()
			except:
				tax = line.split()[0].strip()
				par = line.split()[1].strip()		
			
			
			tablepar[tax] = par
			if tax not in taxlist:
				taxlist.append(tax)
			if par not in taxlist:
				taxlist.append(par)
	return taxlist, tablepar

###################################################
#Gets the next unused number
###################################################
def findlastnum(filename):
	numlist = []
	infile = open(filename,'r').readlines()
	for line in infile:
		numlist.append(line.split('\t')[0])		
	numlist.sort()
	return int(numlist.pop()) + 1	
###################################################
#Using the taxonomy adds makes OTToL formatted lines to be checked and then added
###################################################
def makeLinesToAdd(lineagetable,ottol,nextnum, parDict, lineDict, taxDict):

	linkDict = {}
	try:
		in1 = open('Taxa_not_in_OTToL.txt','r').readlines()
	except:
		ans = raw_input( "there don't seem to be any taxa to add.  If this is not correct, find the file Taxa_not_in_OTToL.txt and put it in the directory with this script. Otherwise enter 'n'.  ")
		if ans[0] == 'n':
			return
		else:
			makeLinesToAdd(lineagetable,ottol,nextnum,taxDict)
	
	name = raw_input('What is your user name? ' )
	in2 = open(lineagetable,'r').readlines()
	
	#in3 = open(ottol,'r').readlines()
	out1 = open('formattedLines.txt','a')
	taxa2add = []
	for line2 in in2:
		if line2[0] != '#' and line2 != '\n':
			t = line2.split('\t')[0].strip()
			p = line2.split('\t')[1].strip()
			linkDict[t] = p	
	for line in in1:
		taxon2add = line.strip()
		taxa2add.append(taxon2add)
	for tax in 	taxa2add:
		for line3 in in2:
			if line3[0] != '#' and line3 != '\n':
				t1 = line3.split('\t')[0].strip() #new taxon name
				p1 = line3.split('\t')[1].strip() #new parent name
			

				if t1 == tax:
					if p1 not in taxa2add: #parent doesn't need to be added
						ans = raw_input('You will be adding the taxon ' + str(t1)  + ' to the parent ' + str(taxDict[p1][0].split('\t')[3]) + '.  Is this taxon a genus or species? (y/n) ')
						if ans[0] == 'y':
							rank = raw_input('What is the rank (i.e. genus or species) of the taxon you are adding? ')
							if rank in ['genus','species']:
								newtaxid = nextnum
								if len(taxDict[p1]) > 1:
									newparidnum = getHom(ottol, p1,parDict, lineDict, taxDict) #returns number, I think?
								else:
									newparidnum = taxDict[p1][0].split('\t')[0]
								newdb = 'added_by_' + name
								taxon = t1
								taxonplus = ""
								time = datetime.datetime.now()
							else:
								print "That rank isn't acceptable.  The taxon will be marked 'unranked' "
								rank = 'unranked'
							out1.write(str(newtaxid) + '\t' + str(newparidnum)  + '\t' + newdb  + '\t' + taxon  + '\t' + taxonplus + '\t' +  rank  + '\t' + str(time) + '\n')
							nextnum = nextnum + 1
						

					else:
							print 'add parent first' #this could probably be handled better!
					
def main():
	x = raw_input('What is the current version of OTToL? ')
#	x = 'preOTToL_092712.txt'
	try:
		p = open(x,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()
	query = raw_input('enter the file with your taxonomy table ')
#	query = 'Amoeba_sample.txt'
	try:
		o = open(query,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()	
	nextnum = findlastnum(x)
	qlist, tablepar = querylist(o)	
	parDict, lineDict, taxDict =  makeDicts(x)

	for taxon in qlist:
		try:
			par = tablepar[taxon] 
		except:
			par = 'no parent in table'
		
		searchOTToL(x,taxon.strip(), par ,parDict, lineDict, taxDict)
	print "###############################################################################"
	print " Now we will make the OTToL formatted lines to be added to OTToL"
	print "###############################################################################"

	makeLinesToAdd(query,x,nextnum, parDict, lineDict, taxDict)
	
	print "###############################################################################"
	print "Lines can be found in the file called formattedLines.txt.txt"
	print "###############################################################################"	
main()