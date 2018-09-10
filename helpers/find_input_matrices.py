import os
from glob import glob
from sys import exit
from warnings import *

def findDirs( d, pattern ):

	return filter( os.path.isdir, [f for f in os.listdir( d ) if pattern in f] )

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

	for i, dirs in enumerate( findDirs(inputfolder, 'Aij_') ):

	  [DSID, mtopshow, sim, tag] = check_nomenclature( dirs )
	  if DSID != 'f':
		dir_list.append( dirs )
		print '    * ' + str(i) + '\t * ' + DSID + '   * ' + mtopshow + '\t* ' + sim + '\t *' + tag + '\t\t\t\t' + '    *'

	print """    *    *          *   	        *        * 			            *
    *********************************************************************************"""

	MESSAGE('Which sample\'s migration matrices/efficiencies should be used to up-fold? [0,1,...]')

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
	reco = inputfolder + '/histograms_' + sampledir + '/reco_level.root'

	if not os.path.exists( migr ):
	    ERROR('The given sample does not appear to contain a migration matrix')
	if not os.path.exists( eff ):
	    ERROR('The given sample does not appear to contain an efficiencies matrix')
	if not os.path.exists( facc ):
	    ERROR('The given sample does not appear to contain a fake rates matrix')
	if not os.path.exists( reco ):
	    WARNING('The given sample does not appear to containt a truth reco level')

	## Return the full path for migration matrices, efficiencies and fake rates

	else:

	    return [migr, eff, facc, reco]

def find_part_hists( inputfolder ):

	## List the produced migration matrices/efficiencies and let the user
	## choose the sample from which to upfold

	print """

    *********************************************************************************
    *   Directories containing particle-level histograms                            *
    *********************************************************************************
    *    * DSID     * MTOP [GeV]        * SIM    *  TAG                             *
    *********************************************************************************
    *    *          *   	        *        * 			            *"""

	## Check that the input directories are following the nomenclature to help
	## with the bookkeeping

	dir_list = []

	for i, dirs in enumerate( findDirs(inputfolder, 'histograms_') ):

	  [DSID, mtopshow, sim, tag] = check_nomenclature( dirs )
	  if DSID != 'f':
		dir_list.append( dirs )
		print '    * ' + str(i) + '\t * ' + DSID + '   * ' + mtopshow + '\t* ' + sim + '\t *' + tag + '\t\t\t\t' + '    *'

	print """    *    *          *   	        *        * 			            *
    *********************************************************************************"""

	MESSAGE('Which sample\'s particle-level should be up-folded? [0,1,...]')


	## Check that all needed ingredients are here

	choice = raw_input()
	try: index = int(choice)
	except ValueError: ERROR('Not an integer')

        if index in range(len(dir_list)):
            sample    = choice
	    sampledir = dir_list[int(choice)].split('histograms_')[1]
        else:
            ERROR('Couldn\'t find the sample you asked for.')
            print 'Exiting...'
            exit()

	part = inputfolder + '/histograms_' + sampledir + '/part_level.root'

	if not os.path.exists( part ):
	    ERROR('The given sample does not appear to contain particle-level histograms.')

	## Return the full path for migration matrices, efficiencies and fake rates

	else:

	    return part

def check_nomenclature( directory ):

	correct = True

	if directory.find('mt_') == -1:
	    WARNING('The directory ' + directory + ' does not explicitly contain the top mass \
		    used to produced the matrices. Be sure to check your bookkeeping.')
	    correct = False
        try: mtopp = directory.split('mt_')[1].split('.')[0].split('_')[0].find('p')
	except IndexError:
	    WARNING('The input file must contain the top mass under the form \'mt_XXXpXX\'')
	    mtop = ''
	    correct = False
        else:
            gev1 = directory.split('mt_')[1].split('_')[0].split('p')[0]
            gev2 = directory.split('mt_')[1].split('_')[0].split('p')[1]
            mtopshow = gev1 + '.' + gev2 + ' [GeV]'
            mtop = directory.split('mt_')[1].split('_')[0]

        ## DSID

        if directory.find('DSID') == -1:
	    WARNING('The directory ' + directory + ' does not explicitly contain the sample DSID. \
		    Be sure to check your bookkeeping.')
            DSID = ''
	    correct = False
        else: DSID = directory.split('DSID_')[1].split('_')[0]

        ## Simulation

        if directory.find('AFII') == -1 and directory.find('FS') == -1:
#	    WARNING('The directory ' + directory + ' does not explicitly contain the simulation description. \
#		    Be sure to check your bookkeeping.')
            sim = ''
	    correct = True
        else: sim = 'AFII' if directory.find('AFII') != -1 else 'FS'

        if directory.find('tag') != -1:
            tag = directory.split('tag_')[1].split('_')[0]
        else: tag = ''

	if correct: return [DSID, mtopshow, sim, tag]
	else: return ['f','f','f','f']
