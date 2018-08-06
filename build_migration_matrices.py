import glob
import os, sys, math
from time import gmtime, strftime
from argparse import ArgumentParser, FileType

from helpers.check_filename import *
from histogramming.sample import *

if __name__ == '__main__':

    print """ 

    #############################   TOP MASS UPFOLDING   ############################
    #										    #
    # This script uses any ROOT file with histograms on reco/particle level, to	    #
    # compute migration matrices, efficiencies and fake hits.			    #
    #										    #
    #		R_i = 1 / f_acc,i * A_ij * (P_j e_eff,j)			    #
    #										    #
    # Additionally, some sanity tests are available:				    #
    #										    #
    #	> closure tests from same statistical sample				    #
    #	> cross-check closure tests from independent samples			    #
    #	> bias tests for top mass / MC parameters				    #
    #										    #
    #*******************************************************************************#
    #										    #
    # Author : Ludovic Scyboz (scyboz@mpp.mpg.de)				    #
    # Date	 : 28.02.2018							    #
    #										    #
    #################################################################################

    """

    parser = ArgumentParser(description='Create the migration matrices,\
				efficiencies and fake hits histograms.')
    parser.add_argument('textfile', metavar='input_mtXXX_DSID_xxxxxx_(FS).txt', type=str, 
				help='the text file containing a list of samples to run over (has to\
				be a simulated sample)')
    parser.add_argument("-N", "--numberOfEvents", required=False, type=str, \
				dest="EVTNUM", default="-99", help="Number of events in the sample for bookkeeping")
    parser.add_argument("-S", "--stats", required=False, type=str, \
				dest="STAT", default="gaussian", help="Multinomial efficiencies/fakes treatment \
				for comparison (default=gaussian) \n" + colors.WARNING + \
				"Beware: these uncertainties are not propagated, just plotted" + colors.ENDC)
    parser.add_argument("-C", "--closureTests", action='store_true', required=False, \
				dest="CLOS", default=False, help="Whether to run closure tests or not [False]")
    parser.add_argument("-D", "--draw", action='store_true', required=False, \
				dest="DRAW", default=False, help="Whether to draw histograms or not [False]")
    args = parser.parse_args()

    timestr = strftime("%d-%m-%y--%H.%M.%S", gmtime())
    evtNum = args.EVTNUM
    stat   = args.STAT
    clos   = args.CLOS
    draw   = args.DRAW

    identifier = check_filename( args.textfile, evtNum )

    ## Naming convention

    output_migr = "Aij_"+identifier
    output_eff  = "eps_"+identifier
    output_facc = "facc_"+identifier
    output_hists= "histograms_"+identifier
    output_clos = "closure_tests_"+identifier

    gROOT.ProcessLine('gErrorIgnoreLevel = 2000;')

    # List of observables from which to build migration matrices
    observables = [
		observable( 'Int_t',	'nbjets', 		 8,   0,	8,		'n_{b,jets}'	),
		observable( 'Double_t', 'pseudotop_mtop_param',	20,   0,	350e+03,	'm_t'		)
		]

    # Create output directories
    os.system( 'mkdir ' + ' '.join([output_migr, output_eff, output_facc, output_hists]) )
    if clos == True: os.system( 'mkdir ' + output_clos ) 

    # Declare migration matrices, reco/part. histograms, eff. & fake hits
    # Load ntuples, set up trees and various objects
    sample = sample( identifier, args.textfile, observables, stat, True )
    sample.import_data()
    sample.synchronize_trees()
    sample.init_objects()

    ## Fill the histograms for particle/reco level
    sample.populate_up(output_hists)
    sample.populate_down(output_hists)


    sample.migration_normalize()
    if draw == True: sample.migration_draw(output_migr)
    sample.migration_write_output(output_migr)

    sample.efficiencies_write_output(output_eff)
    sample.fakes_write_output(output_facc)

    if draw == True:
	sample.efficiencies_draw(output_eff)
	sample.fakes_draw(output_facc)

	## TODO: still some problem with the efficiency matrices w/ correct stats
	##	 (fakes OK though)
        if stat == 'binomial': 
	    sample.efficiencies_bi_draw(output_eff)
	    sample.fakes_bi_draw(output_facc)

    if clos == True: sample.closure_tests(output_clos)
