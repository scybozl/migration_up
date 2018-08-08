import os
from glob import glob
from sys import exit
from warnings import *

def check_filename( name, evtNum ):

	## Top mass must be explicitly stated in the filename to avoid confusion
	## For the moment, to force a correct bookkeeping, DSID's, m_t, and so on
	## have to be explicitly stated in the input filename

	## Not all production samples have metadata or referenced setup info

	if not os.path.exists(name):
	  ERROR('The input file containing the samples location could not be found')
	if name.find('mt_') == -1:
	  ERROR('The input file must contain the top mass under the form \'mt_172p5\'')
	try: mtopp = name.split('mt_')[1].split('.')[0].split('_')[0].find('p')
	except ValueError: 
	  ERROR('The input file must contain the top mass under the form \'mt_XXXpXX\'')
	mtop = name.split('mt_')[1].split('_')[0]

	## DSID

	if name.find('DSID') == -1:
	  ERROR('The input file must contain the sample DSID, i.e. \'DSID_xxxxxx\'')
	DSID = name.split('DSID_')[1].split('_')[0]

	if name.find('AFII') == -1 and name.find('FS') == -1:
	  ERROR('The input file must contain the simulation description, AFII or FS')
	sim = 'AFII' if name.find('AFII') != -1 else 'FS'

	if name.find('tag') != -1:
	  tag = name.split('tag_')[1].split('_')[0]
	else: tag = ''

	identifier = 'DSID_'+DSID+'_mt_'+mtop+'_'+sim
	if evtNum!='-99':  identifier += '_'+evtNum
	if tag != '': identifier += '_'+tag

	## Check that the output directory doesn't already exist

	if glob( '*'+identifier ):
	  WARNING('The identifier for this sample already exists in this folder. Are you' +
	  ' sure you want to overwrite the plots / root files? [y/n]')
	  yes = ['yes','y', 'ye', '']
	  no = ['no','n']
	  choice = raw_input().lower()
	  if choice in yes:
	    os.system('rm -r *'+identifier)
	  elif choice in no:
	    print 'Exiting...'
	    exit()
	  else:
	    print 'Please respond with \'yes\' or \'no\''
	    print 'Exiting...'
	    exit()


	return identifier
