from argparse import ArgumentParser, FileType
from helpers.find_input_matrices import find_matrices

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

    args = parser.parse_args()

    find_matrices( args.inputfolder )
