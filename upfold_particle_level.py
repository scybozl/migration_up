from ROOT import TFile, TH1F, TH2F
from argparse import ArgumentParser, FileType
from helpers.find_input_matrices import find_matrices, find_part_hists
import os

if __name__ == '__main__':

    print """

    #############################   TOP MASS UPFOLDING   ############################
    #                                                                               #
    # This script uses existing migration matrices / efficiencies to up-fold an     #
    # sample produced at particle level to the reco level:                          #
    #                                                                               #
    #           R_i = 1 / f_acc,i * A_ij * (P_j e_eff,j)                            #
    #                                                                               #
    #                                                                               #
    #*******************************************************************************#
    #                                                                               #
    # Author : Ludovic Scyboz (scyboz@mpp.mpg.de)                                   #
    # Date       : 28.02.2018                                                       #
    #                                                                               #
    #################################################################################

    """

    parser = ArgumentParser(description='Up-fold an existing sample from particle \
				level to reco-level.')
    parser.add_argument('inputfolder', type=str, default='.',
				help='Folder containing the produced \
				migration matrices and efficiencies')
    parser.add_argument('-o', '--output', required=False, dest='OUTPUT',
				default='comp_histos', metavar = 'Plot directory',
				type=str, help='Name of the directory where the \
				plots will be generated')

    args = parser.parse_args()

    output_directory = args.OUTPUT
    os.system( 'mkdir ' + output_directory )

    [migr, eff, facc, reco] = find_matrices( args.inputfolder )
    part = find_part_hists( args.inputfolder )

    migr_file	= TFile.Open( migr )
    eff_file    = TFile.Open( eff )
    fake_file   = TFile.Open( facc )
    reco_file   = TFile.Open( reco )

    part_file   = TFile.Open( part )

    migration_matrix= []
    efficiencies    = []
    fakes 	    = []
    reco_histograms = [] ## Truth reco from file 1 for comparison

    part_histograms = [] ## Truth part from file 2 to up-fold
    reco_folded     = [] ## Folded reco for file 2

    ## Loop through all observables listed in migration matrix
    ## TODO: just plotting, should also save files for easier handling later

    for i in migr_file.GetListOfKeys():

	## Get all migration matrices and copy them

	obs_name = i.GetName().split('tMatrix_')[1]

	migr_tmp = TH2F()
	eff_tmp  = TH1F()
	facc_tmp = TH1F()
	reco_tmp = TH1F() ## Truth reco from first file

	part_tmp = TH1F() ## Truth part from second file

	migr_file.GetObject( 'tMatrix_' + obs_name, migr_tmp )
	eff_file.GetObject(  'tEff_'    + obs_name, eff_tmp )
	fake_file.GetObject( 'tFacc_'   + obs_name, facc_tmp )
	reco_file.GetObject( 'tReco_'   + obs_name, reco_tmp )

	part_file.GetObject( 'tPart_'   + obs_name, part_tmp )
	reco_fold = reco_tmp.Clone( 'reco_fold' )

	migration_matrix.append( migr_tmp )
	efficiencies.append( eff_tmp )
	fakes.append( facc_tmp )
	reco_histograms.append( reco_tmp )

	part_histograms.append( part_tmp )
	reco_folded.append( reco_fold )


    ## Fold the particle-level histos from file 2 and plot
    for i, Aij in enumerate( migration_matrix ):
	for j in range(8):
		for k in range(8): print Aij.GetBinContent(j,k)
	nbins = Aij.GetXaxis.GetNbins()
	for xbins in range( nbins + 2 ):

	    sum = 0.
	    error1_2 = 0.
	    error2_2 = 0.
	    error3_2 = 0.

	    for j in range( nbins+2 ):
		sum += Aij.GetBinContent( j,xbins ) * part_histograms[i].GetBinContent(j) \
			* efficiencies[i].GetBinContent(j)
		error1_2 += pow( Aij.GetBinError( j,xbins ) * part_histograms[i].GetBinContent(j) \
			* efficiencies[i].GetBinContent(j), 2 )
		error2_2 += pow( Aij.GetBinContent( j,xbins ) * part_histograms[i].GetBinError(j) \
			* efficiencies[i].GetBinContent(j), 2 )
		error3_2 += pow( Aij.GetBinContent( j,xbins ) * part_histograms[i].GetBinContent(j) \
			* efficiencies[i].GetBinError(j), 2 )

	    if fakes[i].GetBinContent( xbins ) != 0:
		error2 = 1./pow( fakes[i].GetBinContent(xbins),4 ) * pow( fakes[i].GetBinError(xbins)*sum,2 )
		error2 += 1./pow( fakes[i].GetBinContent(xbins),2 ) * ( error1_2 + error2_2 + error3_2 )
                sum *= 1./fakes[i].GetBinContent(xbins)
	    else: error2 = 0.

        reco_folded[i].SetBinContent( xbins, sum )
        reco_folded[i].SetBinError( xbins, sqrt(error2) )

	ratioPlotATLAS( reco_folded[i], reco_histograms[i], output_directory + '/' + Aij.GetName().split('tMatrix_')[1] )
