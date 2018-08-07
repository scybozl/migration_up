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

	## Check that the input directories are following the nomenclature to help
	## with the bookkeeping

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

	  ## Simulation

	  if dirs.find('AFII') == -1 and dirs.find('FS') == -1:
		WARNING('The directory ' + dirs + ' does not contain the simulation description, AFII or FS. \
			Be sure to check your bookkeeping.')
		sim = ''
	  else: sim = 'AFII' if dirs.find('AFII') != -1 else 'FS'

	  if dirs.find('tag') != -1:
		tag = dirs.split('tag_')[1].split('_')[0]
	  else: tag = ''

	  dir_list.append( dirs )
	  print '    * ' + str(i) + '\t * ' + DSID + '   * ' + mtopshow + '\t* ' + sim + '\t *' + tag + '\t\t\t\t' + '    *'

	print """    *    *          *   	        *        * 			            *
    *********************************************************************************"""

	print 'Which sample\'s migration matrices/efficiencies should be used to up-fold? [0,1,...]'


	## Check that all needed ingredients are here

	choice = raw_input()
	try: index = int(choice)
	except ValueError: ERROR('Not an integer')

        if index in range(len(dir_list)):
            sample    = choice
	    sampledir = dir_list[int(choice)].split('Aij_')[1]
        else:
            ERROR('Couldn\'t find the sample you asked for.')
            print 'Exiting...'
            exit()

	migr = inputfolder + '/Aij_' + sampledir + '/migration_matrix.root'
	eff  = inputfolder + '/eps_' + sampledir + '/efficiencies.root'
	facc = inputfolder + '/facc_' + sampledir + '/fake_rates.root'

	if not os.path.exists( migr ):
	    ERROR('The given sample does not appear to contain a migration matrix')
	if not os.path.exists( eff ):
	    ERROR('The given sample does not appear to contain an efficiencies matrix')
	if not os.path.exists( facc ):
	    ERROR('The given sample does not appear to contain a fake rates matrix')

	## Return the full path for migration matrices, efficiencies and fake rates

	else:

	    return [migr, eff, facc]

