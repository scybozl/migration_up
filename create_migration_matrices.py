from time import gmtime, strftime
from ROOT import *
import os, sys, math
import glob
from argparse import ArgumentParser, FileType
from ratio_plot import ratioPlot

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

class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def ERROR(msg):
  print colors.FAIL + "ERROR: " + colors.ENDC + msg
  print "Exiting..."
  sys.exit()

def WARNING(msg):
# raw_input returns the empty string for "enter"
  print colors.WARNING + "WARNING: " + colors.ENDC + msg

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

## Top mass must be explicitly stated in the filename to avoid confusion

if not os.path.exists(args.textfile):
  ERROR('The input file containing the samples location could not be found')
if args.textfile.find("mt_") == -1:
  ERROR('The input file must contain the top mass under the form \'mt_172p5\'')
if args.textfile.split("mt_")[1].split(".")[0].split("_")[0].find("p") == -1:
  ERROR('The input file must contain the top mass under the form \'mt_XXXpXX\'')
mtop = args.textfile.split("mt_")[1].split("_")[0]

## DSID

if args.textfile.find("DSID") == -1:
  ERROR('The input file must contain the sample DSID, i.e. \'DSID_xxxxxx\'')
DSID = args.textfile.split("DSID_")[1].split("_")[0]

if args.textfile.find("AFII") == -1 and args.textfile.find("FS") == -1:
  ERROR('The input file must contain the simulation description, AFII or FS')
sim = "AFII" if args.textfile.find("AFII") != -1 else "FS"

## Naming convention

identifier = "DSID_"+DSID+"_mt_"+mtop+"_"+sim
if evtNum!="-99":  identifier += "_"+evtNum

outputMigr = "Aij_"+identifier
outputEff  = "eps_"+identifier
outputFacc = "fak_"+identifier
outputHists= "histograms_"+identifier
outputClos = "closureTests_"+identifier

if glob.glob("*"+identifier):
  WARNING('The identifier for this sample already exists in this folder. Are you\
  sure you want to overwrite the plots / root files? [y/n]')
  yes = ['yes','y', 'ye', '']
  no = ['no','n']
  choice = raw_input().lower()
  if choice in yes:
    os.system("rm -r *"+identifier)
  elif choice in no:
    print "Exiting..."
    sys.exit()
  else:
    sys.stdout.write("Please respond with 'yes' or 'no'")
    print "Exiting..."
    sys.exit()

gStyle.SetOptStat("neou")
gStyle.SetPaintTextFormat(".4f")
#gErrorIgnoreLevel = kInfo

def populateHistsUp(reco, obsR, part, obsP):
  os.system("mkdir " + outputHists)
  global recoOnly
  recoFile = TFile(outputHists + "/reco_level_"+mtop+".root", "NEW")
  for i in range(reco.GetEntries()):
    if ((i+1) % 1000) == 0: print "Processing event number " + str(i+1) + "..."
    reco.GetEntry(i)
    for j,obs in enumerate(observables):
	y = obs[1] + "_reco"
	recoHists[j].Fill(getattr(obsR,y),reco.weight_mc)
    for j,vec in enumerate(vectors):
	y = vec[1] + "_reco"
	if globals()[y].size() > 0: recoHists[shift+j].Fill(globals()[y][0],reco.weight_mc)
    # Check if the event only exists at reco level
    if part.GetEntryWithIndex(obsR.runNumber, obsR.eventNumber) < 0:
	recoOnly += 1
	for j,obs in enumerate(observables):
	  y = obs[1] + "_reco"
	  facc[j].FillWeighted(kFALSE,reco.weight_mc,getattr(obsR,y))
	for j,vec in enumerate(vectors):
  	  y = vec[1] + "_reco"
	  if globals()[y].size() > 0:  facc[shift+j].FillWeighted(kFALSE,reco.weight_mc,globals()[y][0])
    # If not, it was matched . fill out the migration matrices
    else:
	# Fill the reco/particle histograms, and the migration matrices
	for j,obs in enumerate(observables):
	  x = obs[1] + "_part"
	  y = obs[1] + "_reco"
	  effHists[j].Fill(getattr(obsP,x),part.weight_mc)
	  faccHists[j].Fill(getattr(obsR,y),reco.weight_mc)
	  eff[j].FillWeighted(kTRUE,part.weight_mc,getattr(obsP,x))
	  facc[j].FillWeighted(kTRUE,reco.weight_mc,getattr(obsR,y))
	  migrationMatrices[j].Fill(getattr(obsP,x), getattr(obsR,y),part.weight_mc)
	for j,vec in enumerate(vectors):
	  x = vec[1] + "_part"
	  y = vec[1] + "_reco"
	  if globals()[x].size() > 0: 
	    effHists[shift+j].Fill(globals()[x][0],part.weight_mc)
	    eff[shift+j].FillWeighted(kTRUE,part.weight_mc,globals()[x][0])
	  if globals()[y].size() > 0: 
	    faccHists[shift+j].Fill(globals()[y][0],reco.weight_mc)
	    facc[shift+j].FillWeighted(kTRUE,reco.weight_mc,globals()[y][0])
	  if globals()[x].size() > 0 and globals()[y].size() > 0:
	    migrationMatrices[shift+j].Fill(globals()[x][0],globals()[y][0],part.weight_mc)
  for j,obs in enumerate(observables):
    recoHists[j].Write()
  for j,vec in enumerate(vectors):
    recoHists[shift+j].Write()
  recoFile.Close()

def populateHistsDown(reco, obsR, part, obsP):
  os.system("mkdir " + outputHists)
  global partOnly
  partFile = TFile(outputHists + "/part_level_"+mtop+".root", "NEW")
  for i in range(part.GetEntries()):
    if ((i+1) % 1000) == 0: print "Processing event number " + str(i+1) + "..."
    part.GetEntry(i)
    for j,obs in enumerate(observables):
        x = obs[1] + "_part"
        partHists[j].Fill(getattr(obsP,x),part.weight_mc)
    for j,vec in enumerate(vectors):
        x = vec[1] + "_part"
        if globals()[x].size() > 0: partHists[shift+j].Fill(globals()[x][0],part.weight_mc)
    if reco.GetEntryWithIndex(obsP.runNumber, obsP.eventNumber) < 0: 
	partOnly += 1
	for j,obs in enumerate(observables):
          x = obs[1] + "_part"
          eff[j].FillWeighted(kFALSE,part.weight_mc,getattr(obsP,x))	
	for j,vec in enumerate(vectors):
          x = vec[1] + "_part"
          if globals()[x].size() > 0: eff[shift+j].FillWeighted(kFALSE,part.weight_mc,globals()[x][0])
  for j,obs in enumerate(observables):
    partHists[j].Write()
  for j,vec in enumerate(vectors):
    partHists[shift+j].Write()
  partFile.Close()

def normalize():
  for i,obs in enumerate(observables):
    # Normalize each x-bin to 1
    for xbins in range(obs[2]+2):
	sum = 0.
##	errori = []
	for ybins in range(obs[2]+2): 
		sum += migrationMatrices[i].GetBinContent(xbins, ybins)
##		errori.append(migrationMatrices[i].GetBinError(xbins, ybins))
	for ybins in range(obs[2]+2): 
	  if sum != 0: 
		migrationMatrices[i].SetBinContent(xbins, ybins,
			migrationMatrices[i].GetBinContent(xbins, ybins) / float(sum))
#		migrationMatrices[i].SetBinError(xbins, ybins,
#			migrationMatrices[i].GetBinError(xbins, ybins) / float(sum))
#		migrationMatrices[i].SetBinError( xbins, ybins,
#			migrationMatrices[i].GetBinError(xbins, ybins) / float(sum) 
#			* (1 - migrationMatrices[i].GetBinError(xbins, ybins) / float(sum)) )
		e = migrationMatrices[i].GetBinContent(xbins,ybins)
		if e > 0 and e < 1:
		        migrationMatrices[i].SetBinError( xbins, ybins,
			math.sqrt( e*(1-e) / float(sum)))
##		error2 = 1./pow(float(sum),2) * pow(errori[ybins],2)
##		for ys in range(obs[2]+2):
##		  error2 +=  pow(migrationMatrices[i].GetBinContent(xbins, ybins),2) / pow(float(sum),4) * pow(errori[ys],2)
##		migrationMatrices[i].SetBinError(xbins, ybins, math.sqrt(error2))
		
  for i,vec in enumerate(vectors):
    # Normalize each x-bin to 1
    for xbins in range(vec[2]+2):
	sum = 0.
##	errori = []
	for ybins in range(vec[2]+2): 
		sum += migrationMatrices[shift+i].GetBinContent(xbins, ybins)
##		errori.append(migrationMatrices[shift+i].GetBinError(xbins, ybins))
	for ybins in range(vec[2]+2): 
	  if sum != 0: 
		migrationMatrices[shift+i].SetBinContent(xbins, ybins,
			migrationMatrices[shift+i].GetBinContent(xbins, ybins) / float(sum))
#		migrationMatrices[shift+i].SetBinError(xbins, ybins,
#			migrationMatrices[shift+i].GetBinError(xbins, ybins) / float(sum))
		e = migrationMatrices[shift+i].GetBinContent(xbins, ybins)
		if e > 0 and e < 1:
			migrationMatrices[shift+i].SetBinError( xbins, ybins,
			math.sqrt( e*(1-e) / float(sum)))
##		error2 = 1./pow(float(sum),2) * pow(errori[ybins],2)
##		for ys in range(vec[2]+2):
##		  error2 +=  pow(migrationMatrices[shift+i].GetBinContent(xbins, ybins),2) / pow(float(sum),4) * pow(errori[ys],2)
##		migrationMatrices[shift+i].SetBinError(xbins, ybins, math.sqrt(error2))

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
    ratioPlot(partHists[i], recoHists[i], outputHists + "/" + obs[1] + ".pdf",0)
  for i,vec in enumerate(vectors):
    ratioPlot(partHists[shift+i], recoHists[shift+i], outputHists + "/" + vec[1] + "1.pdf",0)

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
    ratioPlot(recoHists[i], recoFolded[i], outputClos + "/" + obs[1] + ".pdf",1)
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
    ratioPlot(recoHists[shift+i], recoFolded[shift+i], outputClos + "/" + vec[1] + ".pdf",1)
    

recoOnly = 0
partOnly = 0

# List of observables from which to build migration matrices
observables = [
		["Int_t",	"nbjets", 8, 0, 8, "n_{b,jets}"],
		["Int_t",	"njets", 15, 0, 15, "n_{jets}"],
		["Double_t",    "etdr", 20, 0, 400e+03, "E_{T}#Delta R"],
                ["Double_t",    "pseudotop_mtop_param", 20, 0, 350e+03, "m_t"],
                ["Double_t",    "pseudotop_mw", 20, 0, 350e+03, "m_W"],
                ["Double_t",    "pseudotop_rbq", 20, 0, 3, "R_{bq}"],
#                ["Double_t",    "met", 20, 0, 1100e+03, "Missing E_{T}"],
                ["Double_t",    "met_ex", 20, -800e+03, 800e+03, "MET E_{x}"],
                ["Double_t",    "met_ey", 20, -800e+03, 800e+03, "MET E_{y}"],
#                ["Double_t",    "met_phi", 20, -3.1416, 3.1416, "MET \phi"],
                ["Double_t",    "mlb_minavg", 20, 0, 350e+03, "m_{lb,minavg}"],
                ["Double_t",    "mlb_minavglow", 20, 0, 200e+03, "m_{lb,minavglow}"],
                ["Double_t",    "mlb_minavghigh", 20, 0, 400e+03, "m_{lb,minavghigh}"],
                ["Double_t",    "mlb_minmax", 20, 0, 200e+03, "m_{lb,minmax}"],
                ["Double_t",    "mlb_minmaxlow", 20, 0, 200e+03, "m_{lb,minmaxlow}"],
#                ["Double_t",    "mlb_minmaxhigh", 20, 0, 300e+03, "m_{lb}"],
                ["Double_t",    "pTlb_1", 20, 0, 600e+03, "p_{T,lb}_{1}"],
                ["Double_t",    "pTlb_2", 20, 0, 500e+03, "p_{T,lb}_{2}"],
                ["Double_t",    "dRlb_1", 20, 0, 4, "#Delta R_{lb}_{1}"],
                ["Double_t",    "dRlb_2", 20, 0, 4, "#Delta R_{lb}_{2}"],
                ["Double_t",    "mll", 20, 0, 800e+03, "m_{ll}"],
                ["Double_t",    "pTll", 20, 0, 500e+03, "p_{T,ll}"],
                ["Double_t",    "dRll", 20, 0, 6, "#Delta R_{ll}"],
                ["Double_t",    "mbb", 20, 0, 1600e+03, "m_{bb}"],
                ["Double_t",    "pTbb", 20, 0, 800e+03, "p_{T,bb}"],
                ["Double_t",    "dRbb", 20, 0, 6, "#Delta R_{bb}"],
                ["float",    "top_pt", 20, 0, 800e+03, "Top p_{T}"],
                ["float",    "top_eta", 20, -5, 5, "Top #eta"],
                ["float",    "top_phi", 20, -3.1416, 3.1416, "Top #phi"],
                ["float",    "top_m", 20, 0, 500e+03, "Top m"],
                ["float",    "top_e", 20, 0, 2000e+03, "Top E"],
                ["float",    "top_y", 20, -2.9, 2.9, "Top y"],
 #               ["float",    "top_ratio", 20, 0, 1, "m_{lb}"],
                ["float",    "tbar_pt", 20, 0, 800e+03, "tbar p_{T}"],
                ["float",    "tbar_eta", 20, -5, 5, "tbar #eta"],
                ["float",    "tbar_phi", 20, -3.1416, 3.1416, "tbar #phi"],
                ["float",    "tbar_m", 20, 0, 600e+03, "tbar m"],
                ["float",    "tbar_e", 20, 0, 2000e+03, "tbar E"],
                ["float",    "tbar_y", 20, -2.9, 2.9, "tbar y"],
 #               ["float",    "tbar_ratio", 20, 0, 1, "m_{lb}"],
                ["float",    "av_top_pt", 20, 0, 900e+03, "Av. top p_{T}"],
                ["float",    "av_top_eta", 20, -5, 5, "Av. top #eta"],
                ["float",    "av_top_phi", 20, -3.1416, 3.1416, "Av. top #phi"],
                ["float",    "av_top_m", 20, 0, 500e+03, "Av. top m"],
                ["float",    "av_top_e", 20, 0, 2400e+03, "Av. top E"],
                ["float",    "av_top_y", 20, -2.9, 2.9, "Av. top y"],
                ["float",    "ttbar_pt", 20, 0, 800e+03, "ttbar p_{T}"],
                ["float",    "ttbar_eta", 20, -10, 10, "ttbar #eta"],
                ["float",    "ttbar_phi", 20, -3.1416, 3.1416, "ttbar #phi"],
                ["float",    "ttbar_m", 20, 0, 2500e+03, "ttbar m"],
                ["float",    "ttbar_e", 20, 0, 3000e+03, "ttbar E"],
                ["float",    "ttbar_y", 20, -2.9, 2.9, "ttbar y"], 
                ["float",    "ttbar_pout", 20, -400e+03, 400e+03, "ttbar p_{out}"],
                ["float",    "nu_pt", 20, 0, 500e+03, "#nu p_{T}"], 
                ["float",    "nu_eta", 20, -6, 6, "#nu #eta"],
                ["float",    "nu_phi", 20, -3.1416, 3.1416, "#nu #phi"],
                ["float",    "nu_m", 20, -0.2e+03, 0.2e+03, "#nu m"],
                ["float",    "nu_e", 20, 0, 1400e+03, "#nu E"],
                ["float",    "nu_y", 20, -2.9, 2.9, "#nu y"],
                ["float",    "nubar_pt", 20, 0, 500e+03, "#nu bar p_{T}"],
                ["float",    "nubar_eta", 20, -5, 5, "#nu bar #eta"],
                ["float",    "nubar_phi", 20, -3.1416, 3.1416, "#nu bar #phi"],
                ["float",    "nubar_m", 20, -0.3e+03, 0.3e+03, "#nu bar m"],
                ["float",    "nubar_e", 20, 0, 1400e+03, "#nu bar E"],
                ["float",    "nubar_y", 20, -2.9, 2.9, "#nu bar y"],
                ["float",    "Wp_pt", 20, 0, 500e+03, "W^{+} p_{T}"],
                ["float",    "Wp_eta", 20, -6, 6, "W^{+} #eta"],
                ["float",    "Wp_phi", 20, -3.1416, 3.1416, "W^{+} #phi"],
                ["float",    "Wp_m", 20, 0, 400e+03, "W^{+} m"],
                ["float",    "Wp_e", 20, 0, 1500e+03, "W^{+} E"],
                ["float",    "Wp_y", 20, -2.9, 2.9, "W^{+} y"], 
                ["float",    "Wm_pt", 20, 0, 500e+03, "W^{-} p_{T}"],
                ["float",    "Wm_eta", 20, -6, 6, "W^{-} #eta"],
                ["float",    "Wm_phi", 20, -3.1416, 3.1416, "W^{-} #phi"],
                ["float",    "Wm_m", 20, 0, 400e+03, "W^{-} m"],
                ["float",    "Wm_e", 20, 0, 1500e+03, "W^{-} E"],
                ["float",    "Wm_y", 20, -2.9, 2.9, "W^{-} y"]
#                ["Int_t",       "nu_n", 20, 0, 100e+03, "m_{lb}"]
		]

vectors = [
		["double",	"bjet_pt", 20, 0, 990e+03, "b_{jet} p_{T}"],
		["float",	"el_pt", 20, 0, 700e+03, "Electron p_{T}"]
		]

# Declare migration matrices, reco/part. histograms, eff. & fake hits
migrationMatrices = []
partHists = []
recoHists = []
effHists = []
faccHists = []
eff = []
facc = []

for obs in observables:
  mig = "tMatrix_" + obs[1]
  histP = "tPart_" + obs[1]
  histR = "tReco_" + obs[1]
  epsilon = "tEff_"+ obs[1]
  fake = "tFacc_" + obs[1]
  effName = "tEff_"+ obs[1]
  faccName = "tFacc_" + obs[1]
  nBins = obs[2]
  xMin = obs[3]
  xMax = obs[4]
  obsName = obs[5]
  migrationMatrices.append( TH2F(mig, "A_{ij} "+obsName, nBins, xMin, xMax, nBins, xMin, xMax ) )
  partHists.append( TH1F(histP, obsName+"^{part}", nBins, xMin, xMax ) )
  recoHists.append( TH1F(histR, obsName+"^{reco}", nBins, xMin, xMax ) )
  effHists.append( TH1F(epsilon, "#epsilon_{epsilon} "+obsName, nBins, xMin, xMax ) )
  faccHists.append( TH1F(fake, "f_{acc} "+obsName, nBins, xMin, xMax ) )
  eff.append( TEfficiency(effName, "#epsilon_{epsilon} "+obsName, nBins, xMin, xMax ) )
  facc.append( TEfficiency(faccName, "f_{acc} "+obsName, nBins, xMin, xMax ) )

for vec in vectors:
  mig = "tMatrix_lead_" + vec[1]
  histP = "tPart_lead_" + vec[1]
  histR = "tReco_lead_" + vec[1]
  epsilon = "tEff_lead_"+ vec[1]
  fake = "tFacc_lead_" + vec[1]
  effName = "tEff_"+ vec[1]
  faccName = "tFacc_" + vec[1]
  nBins = vec[2]
  xMin = vec[3]
  xMax = vec[4]
  obsName = vec[5]
  migrationMatrices.append( TH2F(mig, "A_{ij} lead. "+obsName, nBins, xMin, xMax, nBins, xMin, xMax ) )
  partHists.append( TH1F(histP, obsName+"1^{part}", nBins, xMin, xMax ) )
  recoHists.append( TH1F(histR, obsName+"1^{reco}", nBins, xMin, xMax ) )
  effHists.append( TH1F(epsilon, "#epsilon_{epsilon} lead. "+obsName, nBins, xMin, xMax ) )
  faccHists.append( TH1F(fake, "f_{acc} lead. "+obsName, nBins, xMin, xMax ) )
  eff.append( TEfficiency(effName, "#epsilon_{epsilon} lead. "+obsName, nBins, xMin, xMax ) )
  facc.append( TEfficiency(faccName, "f_{acc} lead. "+obsName, nBins, xMin, xMax ) ) 

shift = len(observables)

recoLevel = TChain("nominal")
partLevel = TChain("particleLevel")

fileh = open(args.textfile, 'r')
for sample in fileh:
  filename = sample.split("\n")[0]
  print "Adding " + filename + " to the samples list..."
  recoLevel.Add(filename)
  partLevel.Add(filename)
fileh.close()

#myFile = TFile.Open("output_172.5_120K_AF2.root")

# Get the reco (nominal) and particle level branches
#
# Use the indexing to cross-find events matched on both levels and
# fill the histograms

#recoLevel = myFile.Get("nominal")
#partLevel = myFile.Get("particleLevel")

recoIndex = TTreeIndex(recoLevel, "runNumber", "eventNumber")
partIndex = TTreeIndex(partLevel, "runNumber", "eventNumber")
recoLevel.SetTreeIndex(recoIndex)
partLevel.SetTreeIndex(partIndex)

#recoLevel.BuildIndex("runNumber", "eventNumber")
#partLevel.BuildIndex("runNumber", "eventNumber")

# Structs to loop through the branches (needed by SetBranchAddress)
struct1 = 'struct nominal_t{UInt_t runNumber;ULong64_t eventNumber;'
struct2 = 'struct particleLevel_t{UInt_t runNumber;ULong64_t eventNumber;'

for obs in observables:
  struct1 += obs[0] + ' ' + obs[1] + '_reco;'
  struct2 += obs[0] + ' ' + obs[1] + '_part;'

struct1 += '}'
struct2 += '}'

for vec in vectors:
  globals()[vec[1]+'_reco'] = vector(vec[0])()
  globals()[vec[1]+'_part'] = vector(vec[0])()

gROOT.ProcessLine(struct1)
gROOT.ProcessLine(struct2)

nominal = nominal_t()
particleLevel = particleLevel_t()

# Set all the branch addresses for observables defined above

recoLevel.SetBranchAddress("runNumber", AddressOf(nominal,'runNumber'))
recoLevel.SetBranchAddress("eventNumber", AddressOf(nominal,'eventNumber'))

for obs in observables:
  recoLevel.SetBranchAddress('tma_'+obs[1], AddressOf(nominal,obs[1]+'_reco'))
  partLevel.SetBranchAddress('tma_'+obs[1], AddressOf(particleLevel,obs[1]+'_part'))

for vec in vectors:
  if vec[1].find("el_") == -1 and vec[1].find("mu_") == -1:
    recoLevel.SetBranchAddress('tma_'+vec[1], AddressOf(globals()[vec[1]+'_reco']))
    partLevel.SetBranchAddress('tma_'+vec[1], AddressOf(globals()[vec[1]+'_part']))
  else:
    recoLevel.SetBranchAddress(vec[1], AddressOf(globals()[vec[1]+'_reco']))
    partLevel.SetBranchAddress(vec[1], AddressOf(globals()[vec[1]+'_part']))
  

# Loop through the events at reco level & fill the histograms

populateHistsUp(recoLevel, nominal, partLevel, particleLevel)  # First migration matrices, effs, fakes
normalize()	# Then normalize every column there to 1
drawMigrationMatrices()	# Save them as pdfs

# Loop through the particle level this time

recoLevel.ResetBranchAddresses()
partLevel.SetBranchAddress("runNumber", AddressOf(particleLevel,'runNumber'))
partLevel.SetBranchAddress("eventNumber", AddressOf(particleLevel,'eventNumber'))

populateHistsDown(recoLevel, nominal, partLevel, particleLevel)
partLevel.ResetBranchAddresses()

# Draw the particle/reco level histograms in ratio plots

drawHists()

# Compute the efficiencies / fake hit rates and draw them

efficiencies()
effDraw()
fakeHits()
faccDraw()

# Do closure tests to check if the computed folding to reco-level works properly

recoFolded = []
for obs in observables:
  name = "tRecoFolded_" + obs[1]
  nBins = obs[2]
  xMin = obs[3]
  xMax = obs[4]
  obsName = obs[5]
  recoFolded.append( TH1F(name, obsName+"^{reco} folded.", nBins, xMin, xMax ) )

for vec in vectors:
  name = "tRecoFolded_lead_" + vec[1]
  nBins = vec[2]
  xMin = vec[3]
  xMax = vec[4]
  obsName = vec[5]
  recoFolded.append( TH1F(name, obsName+"^{reco} folded.", nBins, xMin, xMax ) )

closureTests()

