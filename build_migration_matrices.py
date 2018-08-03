import glob
import os, sys, math
from time import gmtime, strftime
from argparse import ArgumentParser, FileType

from helpers.check_filename import *
from histogramming.sample import *

print """ 

#############################   TOP MASS UPFOLDING   ############################
#										#
# This script uses any ROOT file with histograms on reco/particle level, to	#
# compute migration matrices, efficiencies and fake hits.			#
#										#
#	R_i = 1 / f_acc,i * A_ij * (P_j e_eff,j)				#
#										#
# Additionally, some sanity tests are available:				#
#										#
#	> closure tests from same statistical sample				#
#	> cross-check closure tests from independent samples			#
#	> bias tests for top mass / MC parameters				#
#										#
#*******************************************************************************#
#										#
# Author : Ludovic Scyboz (scyboz@mpp.mpg.de)					#
# Date	 : 28.02.2018								#
#										#
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
args = parser.parse_args()

timestr = strftime("%d-%m-%y--%H.%M.%S", gmtime())
evtNum = args.EVTNUM
stat   = args.STAT

identifier = check_filename( args.textfile, evtNum )

## Naming convention

output_migr = "Aij_"+identifier
output_eff  = "eps_"+identifier
output_facc = "fak_"+identifier
output_hists= "histograms_"+identifier
output_clos = "closure_tests_"+identifier

#gStyle.SetOptStat("neou")
#gStyle.SetPaintTextFormat(".4f")
#gErrorIgnoreLevel = kInfo

def drawMigrationMatrices():
  os.system("mkdir " + outputMigr)
  migrFile = TFile(outputMigr + "/migration_matrices_"+mtop+".root", "NEW")
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    migrationMatrices[i].GetXaxis().SetTitle(obs[5] + "^{part}")
    migrationMatrices[i].GetYaxis().SetTitle(obs[5] + "^{reco}")
    migrationMatrices[i].GetZaxis().SetRangeUser(0,1)
    migrationMatrices[i].SetMarkerSize(0.3)
    migrationMatrices[i].Draw("COLZ TEXT E")
    c.SaveAs(outputMigr + "/migration_" + obs[1] + ".pdf")
    migrationMatrices[i].Draw("LEGO2Z")
    c.SaveAs(outputMigr + "/migration_" + obs[1] + "_lego.pdf")
    migrationMatrices[i].Write()
  for i,vec in enumerate(vectors):
    migrationMatrices[shift+i].GetXaxis().SetTitle(vec[5] + "1^{part}")
    migrationMatrices[shift+i].GetYaxis().SetTitle(vec[5] + "1^{reco}")
    migrationMatrices[shift+i].GetZaxis().SetRangeUser(0,1)
    migrationMatrices[shift+i].SetMarkerSize(0.3)
    migrationMatrices[shift+i].Draw("COLZ TEXT E")
    c.SaveAs(outputMigr + "/migration_" + vec[1] + "1.pdf")
    migrationMatrices[shift+i].Draw("LEGO2Z")
    c.SaveAs(outputMigr + "/migration_" + vec[1] + "1_lego.pdf")
    migrationMatrices[shift+i].Write()
  migrFile.Close()
  c.Close()

def efficiencies():
  os.system("mkdir " + outputEff)
  effFile = TFile(outputEff + "/efficiencies_"+mtop+".root", "NEW")
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    effHists[i].Sumw2()
    effHists[i].Divide(partHists[i])
    for bin in range(obs[2]+2):
	e = effHists[i].GetBinContent(bin)
	print partHists[i].GetBinContent(bin), e
	if partHists[i].GetBinContent(bin) > 0 and e > 0: effHists[i].SetBinError(bin,math.sqrt( e*(1-e)/partHists[i].GetBinContent(bin)))
	else: effHists[i].SetBinError(bin,0)
    effHists[i].GetXaxis().SetTitle(obs[5])
    effHists[i].GetYaxis().SetTitle("#epsilon_{eff} " + obs[5])
    effHists[i].GetYaxis().SetRangeUser(0.,1.)
    effHists[i].Draw("*HE")
    c.SaveAs(outputEff + "/efficiency_" + obs[1] + ".pdf")
    effHists[i].Write()
  for i,vec in enumerate(vectors):
    effHists[shift+i].Sumw2()
    effHists[shift+i].Divide(partHists[shift+i])
    for bin in range(vec[2]+2):
	e = effHists[shift+i].GetBinContent(bin)
	print partHists[i].GetBinContent(bin), e
	if partHists[shift+i].GetBinContent(bin) > 0 and e > 0 and e < 1: effHists[shift+i].SetBinError(bin,math.sqrt( e*(1-e)/partHists[shift+i].GetBinContent(bin)))
	else: effHists[shift+i].SetBinError(bin,0)
    effHists[shift+i].GetXaxis().SetTitle(vec[5])
    effHists[shift+i].GetYaxis().SetTitle("#epsilon_{eff} lead. " + vec[5])
    effHists[shift+i].GetYaxis().SetRangeUser(0.,1.)
    effHists[shift+i].Draw("*HE")
    c.SaveAs(outputEff + "/efficiency_" + vec[1] + "1.pdf")
    effHists[shift+i].Write()
  effFile.Close()
  c.Close()

def effDraw():
  os.system("mkdir " + outputEff)
  effFile = TFile(outputEff + "/efficiencies_class_"+mtop+".root", "NEW")
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
   # eff[i].SetTitle(obs[5])
   # eff[i].GetYaxis().SetTitle("#epsilon_{eff} " + obs[5])
   # eff[i].GetYaxis().SetRangeUser(0.,1.)
    eff[i].Draw("AP")
    gPad.Update(); 
    graph = eff[i].GetPaintedGraph(); 
    graph.SetMinimum(0);
    graph.SetMaximum(1); 
    gPad.Update(); 
    c.SaveAs(outputEff + "/efficiency_class_" + obs[1] + ".pdf")
    eff[i].Write()
  for i,vec in enumerate(vectors):
   # eff[shift+i].SetTitle(vec[5])
    #eff[shift+i].GetYaxis().SetTitle("#epsilon_{eff} lead. " + vec[5])
    #eff[shift+i].GetYaxis().SetRangeUser(0.,1.)
    eff[shift+i].Draw("AP")
    gPad.Update(); 
    graph = eff[shift+i].GetPaintedGraph(); 
    graph.SetMinimum(0);
    graph.SetMaximum(1); 
    gPad.Update(); 
    c.SaveAs(outputEff + "/efficiency_class_" + vec[1] + "1.pdf")
    eff[shift+i].Write()
  effFile.Close()
  c.Close()

def fakeHits():
  os.system("mkdir " + outputFacc)
  fakeFile = TFile(outputFacc + "/fake_hits_rates_"+mtop+".root", "NEW")
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    faccHists[i].Sumw2()
    faccHists[i].Divide(recoHists[i])
    for bin in range(obs[2]+2):
	e = faccHists[i].GetBinContent(bin)
	if recoHists[i].GetBinContent(bin) > 0 and e > 0 and e < 1: faccHists[i].SetBinError(bin,math.sqrt( e*(1-e)/recoHists[i].GetBinContent(bin)))
	else: faccHists[i].SetBinError(bin,0)
    faccHists[i].GetXaxis().SetTitle(obs[5])
    faccHists[i].GetYaxis().SetTitle("f_{acc} " + obs[5])
    faccHists[i].GetYaxis().SetRangeUser(0.,1.)
    faccHists[i].Draw("*HE")
    c.SaveAs(outputFacc + "/fake_hits_rate_" + obs[1] + ".pdf")
    faccHists[i].Write()
  for i,vec in enumerate(vectors):
    faccHists[shift+i].Sumw2()
    faccHists[shift+i].Divide(recoHists[shift+i])
    for bin in range(vec[2]+2):
	e = faccHists[shift+i].GetBinContent(bin)
	if recoHists[shift+i].GetBinContent(bin) > 0 and e > 0 and e < 1: faccHists[shift+i].SetBinError(bin,math.sqrt( e*(1-e)/recoHists[shift+i].GetBinContent(bin)))
	else: effHists[i].SetBinError(bin,0)
    faccHists[shift+i].GetXaxis().SetTitle(vec[5])
    faccHists[shift+i].GetYaxis().SetTitle("f_{acc} lead. " + vec[5])
    faccHists[shift+i].GetYaxis().SetRangeUser(0.,1.)
    faccHists[shift+i].Draw("*HE")
    c.SaveAs(outputFacc + "/fake_hits_rate_" + vec[1] + "1.pdf")
    faccHists[shift+i].Write()
  fakeFile.Close()
  c.Close()

def faccDraw():
  os.system("mkdir " + outputFacc)
  fakeFile = TFile(outputFacc + "/fake_hits_rates_class_"+mtop+".root", "NEW")
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    #faccHists[i].GetXaxis().SetTitle(obs[5])
    #faccHists[i].GetYaxis().SetTitle("f_{acc} " + obs[5])
    #faccHists[i].GetYaxis().SetRangeUser(0.,1.)
    facc[i].Draw("AP")
    gPad.Update(); 
    graph = eff[i].GetPaintedGraph(); 
    graph.SetMinimum(0);
    graph.SetMaximum(1); 
    gPad.Update(); 
    c.SaveAs(outputFacc + "/fake_hits_rate_class_" + obs[1] + ".pdf")
    facc[i].Write()
  for i,vec in enumerate(vectors):
    #faccHists[shift+i].GetXaxis().SetTitle(vec[5])
    #faccHists[shift+i].GetYaxis().SetTitle("f_{acc} lead. " + vec[5])
    #faccHists[shift+i].GetYaxis().SetRangeUser(0.,1.)
    facc[shift+i].Draw("AP")
    gPad.Update(); 
    graph = eff[shift+i].GetPaintedGraph(); 
    graph.SetMinimum(0);
    graph.SetMaximum(1); 
    gPad.Update(); 
    c.SaveAs(outputFacc + "/fake_hits_rate_class_" + vec[1] + "1.pdf")
    facc[shift+i].Write()
  fakeFile.Close()
  c.Close()

def drawHists():
  os.system("mkdir " + outputHists)
  for i,obs in enumerate(observables):
    ratioPlotATLAS(partHists[i], recoHists[i], outputHists + "/" + obs[1] + ".pdf",0)
  for i,vec in enumerate(vectors):
    ratioPlotATLAS(partHists[shift+i], recoHists[shift+i], outputHists + "/" + vec[1] + "1.pdf",0)

def closureTests():
  os.system("mkdir " + outputClos)
  for i,obs in enumerate(observables):
    for xbins in range(obs[2]+2):
	sum = 0.
	error1_2 = 0.
	error2_2 = 0.
	error3_2 = 0.
	for j in range(obs[2]+2): 
		sum += migrationMatrices[i].GetBinContent(j,xbins) * partHists[i].GetBinContent(j) \
			* effHists[i].GetBinContent(j)
		error1_2 += pow(migrationMatrices[i].GetBinError(j,xbins) * partHists[i].GetBinContent(j) \
			* effHists[i].GetBinContent(j), 2)
		error2_2 += pow(migrationMatrices[i].GetBinContent(j,xbins) * partHists[i].GetBinError(j) \
			* effHists[i].GetBinContent(j), 2)
		error3_2 += pow(migrationMatrices[i].GetBinContent(j,xbins) * partHists[i].GetBinContent(j) \
			* effHists[i].GetBinError(j), 2)
	print "Error parts for "+obs[1]
	if faccHists[i].GetBinContent(xbins) != 0: 
		error2 = 1./pow(faccHists[i].GetBinContent(xbins),4) * pow(faccHists[i].GetBinError(xbins)*sum,2)
		print faccHists[i].GetBinContent(xbins)
		print faccHists[i].GetBinError(xbins)
                error2 += 1./pow(faccHists[i].GetBinContent(xbins),2) * ( error1_2 + error2_2 + error3_2 )
		sum *= 1./(faccHists[i].GetBinContent(xbins))
        else: error2 = 0.
	recoFolded[i].SetBinContent(xbins, sum)
	#if recoFolded[i].GetBinContent(xbins)!=0: print 1./pow(faccHists[i].GetBinContent(xbins),2)*error1_2/pow(recoFolded[i].GetBinContent(xbins),2)
	#if recoFolded[i].GetBinContent(xbins)!=0: print 1./pow(faccHists[i].GetBinContent(xbins),2)*error2_2/pow(recoFolded[i].GetBinContent(xbins),2)
	#if sum!=0: print error3_2/pow(sum,2)
	#if recoFolded[i].GetBinContent(xbins)!=0: print error2/pow(recoFolded[i].GetBinContent(xbins),2)
	print recoFolded[i].GetBinContent(xbins)
	recoFolded[i].SetBinError(xbins,math.sqrt(error2))
	print recoFolded[i].GetBinError(xbins)
	#print recoFolded[i].GetBinContent(xbins)
	#print recoFolded[i].GetBinError(xbins)
    ratioPlotATLAS(recoHists[i], recoFolded[i], outputClos + "/" + obs[1] + ".pdf",1)
  for i,vec in enumerate(vectors):
    for xbins in range(vec[2]+2):
	sum = 0.
	error1_2 = 0.
	error2_2 = 0.
	error3_2 = 0.
	for j in range(vec[2]+2): 
		sum += migrationMatrices[shift+i].GetBinContent(j,xbins) * partHists[shift+i].GetBinContent(j) \
			* effHists[shift+i].GetBinContent(j)
		error1_2 += pow(migrationMatrices[shift+i].GetBinError(j,xbins) * partHists[shift+i].GetBinContent(j) \
			* effHists[shift+i].GetBinContent(j), 2)
		error2_2 += pow(migrationMatrices[shift+i].GetBinContent(j,xbins) * partHists[shift+i].GetBinError(j) \
			* effHists[shift+i].GetBinContent(j), 2)
		error3_2 += pow(migrationMatrices[shift+i].GetBinContent(j,xbins) * partHists[shift+i].GetBinContent(j) \
			* effHists[shift+i].GetBinError(j), 2)
	if faccHists[shift+i].GetBinContent(xbins) != 0:
		error2 = 1./pow(faccHists[shift+i].GetBinContent(xbins),4) * pow(faccHists[shift+i].GetBinError(xbins)*sum,2) 
                error2 += 1./pow(faccHists[shift+i].GetBinContent(xbins),2) * ( error1_2 + error2_2 + error3_2 ) 
		sum *= 1./(faccHists[shift+i].GetBinContent(xbins))
	recoFolded[shift+i].SetBinContent(xbins, sum)
	recoFolded[shift+i].SetBinError(xbins,math.sqrt(error2))
    ratioPlotATLAS(recoHists[shift+i], recoFolded[shift+i], outputClos + "/" + vec[1] + ".pdf",1)
    

# List of observables from which to build migration matrices
observables = [
		observable( 'Int_t',	'nbjets', 		 8,   0,	8,		'n_{b,jets}'	),
		observable( 'Double_t', 'pseudotop_mtop_param',	20,   0,	350e+03,	'm_t'		)
		]

# Create output directories
os.system( 'mkdir ' + ' '.join([output_migr, output_eff, output_facc, output_hists]) )

# Declare migration matrices, reco/part. histograms, eff. & fake hits

sample = sample( identifier, args.textfile, observables, None )
sample.import_data()
sample.synchronize_trees()
sample.init_objects()

sample.populate_up(output_hists)
sample.populate_down(output_hists)

sample.migration_normalize()
sample.migration_write_output(output_migr)

