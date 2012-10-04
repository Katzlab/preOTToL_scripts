'''
Given a file with a list of OTToL formatted lines, check that they aren't already
there and make a list to add to make a new OTToL.  Also outputs files of taxa in the file
that are already in OTToL marked as homonyms or not.
If the taxon id is already used, or if the parent id doesn't exist, the line will be 
written to an error log
'''
import re

print '#########################################################'
print 'This script will take a file of OTToL formatted lines and check to see if they can be added to OTToL.'
print ' It will output 3 files. one to concatenate to OTToL, one with lines that are already in OTToL but not marked as homonyms and one of homonys to check before adding. '
print '#########################################################'
	
	
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
	print 'taxlist made'
	
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
			
def main():

	try:
		file = raw_input('what is the latest version of OTToL? ')
		file2 = raw_input('what is the file you want to add? ')
		add(file,file2)
	except:
		print '#########################################################'
		print 'Trouble opening files.  Make sure they are in the correct directory'
		print '#########################################################'
		main()
main()