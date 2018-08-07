import os
from glob import glob
from sys import exit
from warnings import *

def findDirs( d ):

	return filter( os.path.isdir, [f for f in os.listdir( d ) if 'Aij' in f] )

def find_matrices( inputfolder ):

	## List the produced migration matrices/efficiencies and let the user
	## choose the sample from which to upfold

	print """

    *********************************************************************************
    *   Directories containing migration matrices                                   *
    *********************************************************************************
    *    * DSID     * MTOP [GeV]        * SIM    *  TAG                             *
    *********************************************************************************
    *    *          *   	        *        * 			            *"""

	dir_list = []

	for i, dirs in enumerate( findDirs(inputfolder) ):

	  if dirs.find('mt_') == -1:
		WARNING('The directory ' + dirs + ' does not explicitly contain the top mass \
			used to produced the matrices. Be sure to check your bookkeeping.')
	  if dirs.split('mt_')[1].split('.')[0].split('_')[0].find('p') == -1:
		WARNING('The input file must contain the top mass under the form \'mt_XXXpXX\'')
		mtop = ''
	  else:
		gev1 = dirs.split('mt_')[1].split('_')[0].split('p')[0]
		gev2 = dirs.split('mt_')[1].split('_')[0].split('p')[1]
		mtopshow = gev1 + '.' + gev2 + ' [GeV]'
		mtop = dirs.split('mt_')[1].split('_')[0]

	## DSID

	  if dirs.find('DSID') == -1:
		WARNING('The directory ' + dirs + ' does not contain the sample DSID. \
			Be sure to check your bookkeeping.')
		DSID = ''
	  else: DSID = dirs.split('DSID_')[1].split('_')[0]

	  if dirs.find('AFII') == -1 and dirs.find('FS') == -1:
		WARNING('The directory ' + dirs + ' does not contain the simulation description, AFII or FS. \
			Be sure to check your bookkeeping.')
		sim = ''
	  else: sim = 'AFII' if dirs.find('AFII') != -1 else 'FS'

	  if dirs.find('tag') != -1:
		tag = dirs.split('tag_')[1].split('_')[0]
	  else: tag = ''

	  print '    * ' + str(i) + '\t * ' + DSID + '   * ' + mtopshow + '\t* ' + sim + '\t *' + tag + '\t\t\t\t' + '    *'

	print '    *********************************************************************************'

	identifier = 'DSID_'+DSID+'_mt_'+mtop+'_'+sim
	if tag != '': identifier += '_'+tag

	## Check that the output directory doesn't already exist


	return identifier

