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
    # Date   : 28.02.2018							    #
    #										    #
    #################################################################################

    """

    parser = ArgumentParser(description='Create the migration matrices,\
				efficiencies and fake hits histograms.')
    parser.add_argument('textfile', metavar='input_mtXXX_DSID_xxxxxx_(FS).txt', type=str, 
				help='the text file containing a list of samples to run over (has to\
				be a simulated sample)')
    parser.add_argument("-n", "--numberOfEvents", required=False, type=str, \
				dest="EVTNUM", default="-99", help="Number of events in the sample for bookkeeping")
    parser.add_argument("-s", "--stats", required=False, type=str, \
				dest="STAT", default="gaussian", help="Multinomial efficiencies/fakes treatment \
				for comparison (default=gaussian) \n" + colors.WARNING + \
				"Beware: these uncertainties are not propagated, just plotted" + colors.ENDC)
    parser.add_argument("-c", "--closureTests", action='store_true', required=False, \
				dest="CLOS", default=False, help="Whether to run closure tests or not [False]")
    parser.add_argument("-d", "--draw", action='store_true', required=False, \
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
		observable( 'Int_t',	'nbjets', 		 8,   0.5,	8.5,		'n_{b,jets}'	),
		observable( 'Int_t',	'njets', 		15,   0.5,	15.5,		'n_{jets}'	),
		observable( 'Double_t', 'etdr',			20,   0,	400e+03,	'E_{T}#Delta R'	),
		observable( 'Double_t', 'pseudotop0_mtop_param',20,   0,	350e+03,	'm_{t}'		),
		observable( 'Double_t', 'pseudotop1_mtop_param',20,   0,	350e+03,	'm_{t}'		),
		observable( 'Double_t', 'pseudotop2_mtop_param',20,   0,	350e+03,	'm_{t}'		),
		observable( 'Double_t', 'pseudotop3_mtop_param',20,   0,	350e+03,	'm_{t}'		),
		observable( 'Double_t', 'pseudotop_mw',		20,   0,	350e+03,	'm_{W}'		),
		observable( 'Double_t', 'pseudotop_rbq',	20,   0,	3,		'R_{bq}'	),
		observable( 'Double_t', 'met',			20,   0,	800e+03,	'Missing E_{T}'	),
		observable( 'Double_t', 'met_ex',		20,   -800e+03,	800e+03,	'MET E_{x}'	),
		observable( 'Double_t', 'met_ey',		20,   -800e+03,	800e+03,	'MET E_{y}'	),
		observable( 'Double_t', 'met_phi',		20,   -3.14159,	3.14159,	'MET #phi'	),
		observable( 'Double_t', 'mlb_minavg',		20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'mlb_minavglow',	20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'mlb_minavghigh',	20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'mlb_minmax',		20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'mlb_minmaxlow',	20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'mlb_minmaxavg',	20,   0,	350e+03,	'm_{lb}'	),
		observable( 'Double_t', 'pTlb_1',		20,   0,	600e+03,	'p_{T}^{lb}_{1}'),
		observable( 'Double_t', 'pTlb_2',		20,   0,	600e+03,	'p_{T}^{lb}_{2}'),
		observable( 'Double_t', 'dRlb_1',		20,   0,	4,		'#Delta_{R}^{lb}_{1}'),
		observable( 'Double_t', 'dRlb_2',		20,   0,	4,		'#Delta_{R}^{lb}_{2}'),
		observable( 'Double_t', 'mll',			20,   0,	800e+03,	'm_{ll}'	),
		observable( 'Double_t', 'pTll',			20,   0,	500e+03,	'p_{T}^{ll}'	),
		observable( 'Double_t', 'dRll',			20,   0,	6,		'#Delta_{R}^{ll}'),
		observable( 'Double_t', 'mbb',			20,   0,	1000e+03,	'm_{bb}'	),
		observable( 'Double_t', 'pTbb',			20,   0,	500e+03,	'p_{T}^{bb}'	),
		observable( 'Double_t', 'dRbb',			20,   0,	6,		'#Delta_{R}^{bb}'),
		observable( 'float',	'top_pt',		20,   0,	800e+03,	'p_{T}(t)'	),
		observable( 'float',	'top_eta',		20,   -5,	5,		'#eta(t)'	),
		observable( 'float',	'top_phi',		20,   -3.14159, 3.14159,	'#phi(t)'	),
		observable( 'float',	'top_m',		 5,   170e+03,	175e+03,	'm_{t}'		),
		observable( 'float',	'top_e',		20,   0,	1400e+03,	'm_{t}'		),
		observable( 'float',	'top_y',		20,   -2.9,	2.9,		'y(t)'		),
		observable( 'float',	'tbar_pt',		20,   0,	800e+03,	'p_{T}(#bar{t})'),
		observable( 'float',	'tbar_eta',		20,   -5,	5,		'#eta(#bar{t})'	),
		observable( 'float',	'tbar_phi',		20,   -3.14159, 3.14159,	'#phi(#bar{t})'	),
		observable( 'float',	'tbar_m',		 5,   170e+03,	175e+03,	'm_{#bar{t}}'	),
		observable( 'float',	'tbar_e',		20,   0,	1400e+03,	'm_{#bar{t}}'	),
		observable( 'float',	'tbar_y',		20,   -2.9,	2.9,		'y(#bar{t})'	),
		observable( 'float',	'av_top_pt',		20,   0,	800e+03,	'Average p_{T}(t)'),
		observable( 'float',	'av_top_eta',		20,   -5,	5,		'Average #eta(t)'),
		observable( 'float',	'av_top_phi',		20,   -3.14159, 3.14159,	'Average #phi(t)'),
		observable( 'float',	'av_top_m',		 5,   170e+03,	175e+03,	'Average m_{t}'	),
		observable( 'float',	'av_top_e',		20,   0,	1400e+03,	'Average m_{t}'	),
		observable( 'float',	'av_top_y',		20,   -2.9,	2.9,		'Average y(t)'	),
		observable( 'float',	'ttbar_pt',		20,   0,	800e+03,	'p_{T}(t#bar{t})'),
		observable( 'float',	'ttbar_eta',		20,   -5,	5,		'#eta(t#bar{t})'),
		observable( 'float',	'ttbar_phi',		20,   -3.14159, 3.14159,	'#phi(t#bar{t})'),
		observable( 'float',	'ttbar_m',		20,   0,	2000e+03,	'm_{t#bar{t}}'	),
		observable( 'float',	'ttbar_e',		20,   0,	2500e+03,	'm_{t#bar{t}}'	),
		observable( 'float',	'ttbar_y',		20,   -2.9,	2.9,		'y(t#bar{t})'	),
		observable( 'float',	'ttbar_pout',		20,   -300e+03,	300e+03,	'p_{out}(t#bar{t})'),
		observable( 'float',	'nu_pt',		20,   0,	500e+03,	'p_{T}(#nu)'	),
		observable( 'float',	'nu_eta',		20,   -5,	5,		'#eta(#nu)'	),
		observable( 'float',	'nu_phi',		20,   -3.14159, 3.14159,	'#phi(#nu)'	),
		observable( 'float',	'nu_m',			20,   0,	10,		'm_{#nu}'	),
		observable( 'float',	'nu_e',			20,   0,	800e+03,	'm_{#nu}'	),
		observable( 'float',	'nu_y',			20,   -2.9,	2.9,		'y(#nu)'	),
		observable( 'float',	'nubar_pt',		20,   0,	500e+03,	'p_{T}(#bar{#nu})'),
		observable( 'float',	'nubar_eta',		20,   -5,	5,		'#eta(#bar{#nu})'),
		observable( 'float',	'nubar_phi',		20,   -3.14159, 3.14159,	'#phi(#bar{#nu})'),
		observable( 'float',	'nubar_m',		20,   0,	10,		'm_{#bar{#nu}}'	),
		observable( 'float',	'nubar_e',		20,   0,	800e+03,	'm_{#bar{#nu}}'	),
		observable( 'float',	'nubar_y',		20,   -2.9,	2.9,		'y(#bar{#nu})'	),
		observable( 'float',	'Wp_pt',		20,   0,	500e+03,	'p_{T}(W^{+})'	),
		observable( 'float',	'Wp_eta',		20,   -5,	5,		'#eta(W^{+})'	),
		observable( 'float',	'Wp_phi',		20,   -3.14159, 3.14159,	'#phi(W^{+})'	),
		observable( 'float',	'Wp_m',			20,   0,	400e+03,	'm_{W^{+}}'	),
		observable( 'float',	'Wp_e',			20,   0,	1500e+03,	'm_{W^{+}}'	),
		observable( 'float',	'Wp_y',			20,   -2.9,	2.9,		'y(W^{+})'	),
		observable( 'float',	'Wm_pt',		20,   0,	500e+03,	'p_{T}(W^{-})'	),
		observable( 'float',	'Wm_eta',		20,   -5,	5,		'#eta(W^{-})'	),
		observable( 'float',	'Wm_phi',		20,   -3.14159, 3.14159,	'#phi(W^{-})'	),
		observable( 'float',	'Wm_m',			20,   0,	400e+03,	'm_{W^{-}}'	),
		observable( 'float',	'Wm_e',			20,   0,	1500e+03,	'm_{W^{-}}'	),
		observable( 'float',	'Wm_y',			20,   -2.9,	2.9,		'y(W^{-})'	)
		]

    # Create output directories
    os.system( 'mkdir ' + ' '.join([output_migr, output_eff, output_facc, output_hists]) )
    if clos: os.system( 'mkdir ' + output_clos ) 

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
    if draw: sample.migration_draw(output_migr)
    sample.migration_write_output(output_migr)

    sample.efficiencies_write_output(output_eff)
    sample.fakes_write_output(output_facc)

    if draw:
	sample.efficiencies_draw(output_eff)
	sample.fakes_draw(output_facc)

        if stat == 'binomial': 
	    sample.efficiencies_bi_draw(output_eff)
	    sample.fakes_bi_draw(output_facc)

    if clos: sample.closure_tests(output_clos)
