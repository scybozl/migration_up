#################################################################################
#										#
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

from time import gmtime, strftime
from ROOT import *
import os, sys

timestr = strftime("%d-%m-%y--%H.%M.%S", gmtime())

inputfile = sys.argv[1]

outputMigr = "migration_matrices_"+timestr
outputHists= "histograms_"+timestr
outputEff  = "efficiencies_"+timestr
outputFacc = "fake_hits_rates_"+timestr
outputClos = "closure_tests_"+timestr

def ratioPlot(firstHist,secondHist,title):
  hist1 = firstHist.Clone("hist1")
  hist2 = secondHist.Clone("hist2")
  c2 = TCanvas("c2","c2",800,800)
  pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0) # Upper and lower plot are joined
  pad1.SetGridx()         # Vertical grid
  pad1.Draw()             # Draw the upper pad: pad1
  pad1.cd()               # pad1 becomes the current pad
#  hist1.SetStats(0)       # No statistics on upper plot
  hist1.Draw()            # Draw hist1
  hist2.Draw("same")      # Draw hist2
  # lower plot will be in pad
  c2.cd()          # Go back to the main canvas before defining pad2
  pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
  pad2.SetTopMargin(0.1)
  pad2.SetBottomMargin(0.2)
  pad2.SetGridx() # vertical grid
  pad2.Draw()
  pad2.cd()       # pad2 becomes the current pad

  # Define the ratio plot
  h3 = hist1.Clone("h3")
  h3.SetLineColor(kBlack)
  h3.SetMinimum(0.0)  # Define Y ..
  h3.SetMaximum(3.0) # .. range
  h3.Sumw2()
  h3.SetStats(0)      # No statistics on lower plot
  h3.Divide(hist2)
  h3.SetMarkerStyle(21)
  h3.Draw("ep")       # Draw the ratio plot

  hist1.SetTitle("")
  hist1.SetLineColor(kBlue+1)
  hist1.SetLineWidth(2)

  hist1.GetYaxis().SetTitle("N_{events}")
  hist1.GetYaxis().SetTitleSize(20)
  hist1.GetYaxis().SetTitleFont(43)
  hist1.GetYaxis().SetTitleOffset(1.55)
  hist1.GetXaxis().SetTitleSize(0)
  hist1.GetXaxis().SetLabelSize(0)

  hist2.SetLineColor(kRed)
  hist2.SetLineWidth(2)

  h3.SetTitle("")

  h3.GetYaxis().SetTitle("Ratio "+firstHist.GetTitle()+"/"+secondHist.GetTitle())
  h3.GetYaxis().SetNdivisions(505)
  h3.GetYaxis().SetTitleSize(20)
  h3.GetYaxis().SetTitleFont(43)
  h3.GetYaxis().SetTitleOffset(1.55)
  h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h3.GetYaxis().SetLabelSize(25)

  h3.GetXaxis().SetTitle(firstHist.GetTitle().split("^{part}")[0])
  h3.GetXaxis().SetTitleOffset(1.55)
  h3.GetXaxis().SetTitleSize(25)
  h3.GetXaxis().SetTitleFont(43)
  h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h3.GetXaxis().SetLabelSize(25)

  c2.SaveAs(title)
  c2.Close()

def populateHistsUp(reco, obsR, part, obsP):
  global recoOnly
  for i in range(reco.GetEntries()):
    if ((i+1) % 1000) == 0: print "Processing event number " + str(i+1) + "..."
    reco.GetEntry(i)
    for j,obs in enumerate(observables):
	y = obs[1] + "_reco"
	recoHists[j].Fill(getattr(obsR,y))
    for j,vec in enumerate(vectors):
	y = vec[1] + "_reco"
	if globals()[y].size() > 0: recoHists[shift+j].Fill(globals()[y][0])
    # Check if the event only exists at reco level
    if part.GetEntryWithIndex(obsR.runNumber, obsR.eventNumber) < 0: recoOnly += 1
    # If not, it was matched . fill out the migration matrices
    else:
	# Fill the reco/particle histograms, and the migration matrices
	for j,obs in enumerate(observables):
	  x = obs[1] + "_part"
	  y = obs[1] + "_reco"
	  effHists[j].Fill(getattr(obsP,x))
	  faccHists[j].Fill(getattr(obsR,y))
	  migrationMatrices[j].Fill(getattr(obsP,x), getattr(obsR,y))
	for j,vec in enumerate(vectors):
	  x = vec[1] + "_part"
	  y = vec[1] + "_reco"
	  if globals()[x].size() > 0: effHists[shift+j].Fill(globals()[x][0])
	  if globals()[y].size() > 0: faccHists[shift+j].Fill(globals()[y][0])
	  if globals()[x].size() > 0 and globals()[y].size() > 0:
	    migrationMatrices[shift+j].Fill(globals()[x][0],globals()[y][0])

def populateHistsDown(reco, obsR, part, obsP):
  global partOnly
  for i in range(part.GetEntries()):
    if ((i+1) % 1000) == 0: print "Processing event number " + str(i+1) + "..."
    part.GetEntry(i)
    for j,obs in enumerate(observables):
        x = obs[1] + "_part"
        partHists[j].Fill(getattr(obsP,x))
    for j,vec in enumerate(vectors):
        x = vec[1] + "_part"
        if globals()[x].size() > 0: partHists[shift+j].Fill(globals()[x][0])
    if reco.GetEntryWithIndex(obsP.runNumber, obsP.eventNumber) < 0: partOnly += 1


def normalize():
  for i,obs in enumerate(observables):
    # Normalize each x-bin to 1
    for xbins in range(obs[2]):
	sum = 0
	for ybins in range(obs[2]): sum += migrationMatrices[i].GetBinContent(xbins, ybins)
	for ybins in range(obs[2]): 
	  if sum != 0: migrationMatrices[i].SetBinContent(xbins, ybins,
			migrationMatrices[i].GetBinContent(xbins, ybins) / float(sum))
  for i,vec in enumerate(vectors):
    # Normalize each x-bin to 1
    for xbins in range(vec[2]):
	sum = 0
	for ybins in range(vec[2]): sum += migrationMatrices[shift+i].GetBinContent(xbins, ybins)
	for ybins in range(vec[2]): 
	  if sum != 0: migrationMatrices[shift+i].SetBinContent(xbins, ybins,
			migrationMatrices[shift+i].GetBinContent(xbins, ybins) / float(sum))

def drawMigrationMatrices():
  os.system("mkdir " + outputMigr)
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    migrationMatrices[i].GetXaxis().SetTitle(obs[5] + "^{part}")
    migrationMatrices[i].GetYaxis().SetTitle(obs[5] + "^{reco}")
    migrationMatrices[i].Draw("COLZ")
    c.SaveAs(outputMigr + "/migration_" + obs[1] + ".pdf")
    migrationMatrices[i].Draw("LEGO2Z")
    c.SaveAs(outputMigr + "/migration_" + obs[1] + "_lego.pdf")
  for i,vec in enumerate(vectors):
    migrationMatrices[shift+i].GetXaxis().SetTitle(vec[5] + "1^{part}")
    migrationMatrices[shift+i].GetYaxis().SetTitle(vec[5] + "1^{reco}")
    migrationMatrices[shift+i].Draw("COLZ")
    c.SaveAs(outputMigr + "/migration_" + vec[1] + "1.pdf")
    migrationMatrices[shift+i].Draw("LEGO2Z")
    c.SaveAs(outputMigr + "/migration_" + vec[1] + "1_lego.pdf")
  c.Close()

def efficiencies():
  os.system("mkdir " + outputEff)
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    effHists[i].Divide(partHists[i])
    effHists[i].GetXaxis().SetTitle(obs[5])
    effHists[i].GetYaxis().SetTitle("\epsilon_{eff} " + obs[5])
    effHists[i].Draw("P")
    c.SaveAs(outputEff + "/efficiency_" + obs[1] + ".pdf")
  for i,vec in enumerate(vectors):
    effHists[shift+i].Divide(partHists[shift+i])
    effHists[shift+i].GetXaxis().SetTitle(vec[5])
    effHists[shift+i].GetYaxis().SetTitle("\epsilon_{eff} lead. " + vec[5])
    effHists[shift+i].Draw("P")
    c.SaveAs(outputEff + "/efficiency_" + vec[1] + "1.pdf")
  c.Close()

def fakeHits():
  os.system("mkdir " + outputFacc)
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    faccHists[i].Divide(recoHists[i])
    faccHists[i].GetXaxis().SetTitle(obs[5])
    faccHists[i].GetYaxis().SetTitle("f_{acc} " + obs[5])
    faccHists[i].Draw("P")
    c.SaveAs(outputFacc + "/fake_hits_rate_" + obs[1] + ".pdf")
  for i,vec in enumerate(vectors):
    faccHists[shift+i].Divide(recoHists[shift+i])
    faccHists[shift+i].GetXaxis().SetTitle(vec[5])
    faccHists[shift+i].GetYaxis().SetTitle("f_{acc} lead. " + vec[5])
    faccHists[shift+i].Draw("P")
    c.SaveAs(outputFacc + "/fake_hits_rate_" + vec[1] + "1.pdf")
  c.Close()

def drawHists():
  os.system("mkdir " + outputHists)
  for i,obs in enumerate(observables):
    ratioPlot(partHists[i], recoHists[i], outputHists + "/" + obs[1] + ".pdf")
  for i,vec in enumerate(vectors):
    ratioPlot(partHists[shift+i], recoHists[shift+i], outputHists + "/" + vec[1] + "1.pdf")

def closureTests():
  os.system("mkdir " + outputClos)
  for i,obs in enumerate(observables):
    for xbins in range(obs[2]):
	sum = 0.
	for j in range(obs[2]): sum += migrationMatrices[i].GetBinContent(j,xbins) * partHists[i].GetBinContent(j) \
			* effHists[i].GetBinContent(j)
	if faccHists[i].GetBinContent(xbins) != 0: sum *= 1./(faccHists[i].GetBinContent(xbins))
	recoFolded[i].SetBinContent(xbins, sum)
    ratioPlot(recoHists[i], recoFolded[i], outputClos + "/" + obs[1] + ".pdf")
  for i,vec in enumerate(vectors):
    for xbins in range(vec[2]):
	sum = 0.
	for j in range(vec[2]): sum += migrationMatrices[shift+i].GetBinContent(j,xbins) * partHists[shift+i].GetBinContent(j) \
			* effHists[shift+i].GetBinContent(j)
	if faccHists[shift+i].GetBinContent(xbins) != 0: sum *= 1./(faccHists[shift+i].GetBinContent(xbins))
	recoFolded[shift+i].SetBinContent(xbins, sum)
    ratioPlot(recoHists[shift+i], recoFolded[shift+i], outputClos + "/" + vec[1] + ".pdf")
    

recoOnly = 0
partOnly = 0

# List of observables from which to build migration matrices
observables = [
		["Int_t",	"nbjets", 8, 0, 8, "n_{b,jets}"],
		["Int_t",	"njets", 15, 0, 15, "n_{jets}"],
		["Double_t",    "etdr", 20, 0, 400e+03, "E_{T}\DeltaR"],
                ["Double_t",    "met", 20, 0, 1100e+03, "Missing E_{T}"],
                ["Double_t",    "met_ex", 20, -1000e+03, 1000e+03, "MET E_{x}"],
                ["Double_t",    "met_ey", 20, -1000e+03, 1000e+03, "MET E_{y}"],
                ["Double_t",    "met_phi", 20, -3.1416, 3.1416, "MET \phi"],
                ["Double_t",    "mlb_minavg", 20, 0, 400e+03, "m_{lb}"],
                ["Double_t",    "mlb_minavglow", 20, 0, 300e+03, "m_{lb}"],
                ["Double_t",    "mlb_minavghigh", 20, 0, 700e+03, "m_{lb}"],
                ["Double_t",    "mlb_minmax", 20, 0, 700e+03, "m_{lb}"],
                ["Double_t",    "mlb_minmaxlow", 20, 0, 300e+03, "m_{lb}"],
#                ["Double_t",    "mlb_minmaxhigh", 20, 0, 300e+03, "m_{lb}"],
                ["Double_t",    "pTlb_1", 20, 0, 600e+03, "p_{T,lb}_{1}"],
                ["Double_t",    "pTlb_2", 20, 0, 500e+03, "p_{T,lb}_{2}"],
                ["Double_t",    "dRlb_1", 20, 0, 6, "\DeltaR_{lb}_{1}"],
                ["Double_t",    "dRlb_2", 20, 0, 6, "\DeltaR_{lb}_{2}"],
                ["Double_t",    "mll", 20, 0, 900e+03, "m_{ll}"],
                ["Double_t",    "pTll", 20, 0, 500e+03, "p_{T,ll}"],
                ["Double_t",    "dRll", 20, 0, 6, "\DeltaR_{ll}"],
                ["Double_t",    "mbb", 20, 0, 2300e+03, "m_{bb}"],
                ["Double_t",    "pTbb", 20, 0, 900e+03, "p_{T,bb}"],
                ["Double_t",    "dRbb", 20, 0, 6, "\DeltaR_{bb}"],
                ["float",    "top_pt", 20, 0, 900e+03, "Top p_{T}"],
                ["float",    "top_eta", 20, -5, 5, "Top \eta"],
                ["float",    "top_phi", 20, -3.1416, 3.1416, "Top \phi"],
                ["float",    "top_m", 20, 0, 500e+03, "Top m"],
                ["float",    "top_e", 20, 0, 4100e+03, "Top E"],
                ["float",    "top_y", 20, -2.9, 2.9, "Top y"],
 #               ["float",    "top_ratio", 20, 0, 1, "m_{lb}"],
                ["float",    "tbar_pt", 20, 0, 900e+03, "Tbar p_{T}"],
                ["float",    "tbar_eta", 20, -5, 5, "Tbar \eta"],
                ["float",    "tbar_phi", 20, -3.1416, 3.1416, "Tbar \phi"],
                ["float",    "tbar_m", 20, 0, 600e+03, "Tbar m"],
                ["float",    "tbar_e", 20, 0, 2700e+03, "Tbar E"],
                ["float",    "tbar_y", 20, -2.9, 2.9, "Tbar y"],
 #               ["float",    "tbar_ratio", 20, 0, 1, "m_{lb}"],
                ["float",    "av_top_pt", 20, 0, 900e+03, "Av. top p_{T}"],
                ["float",    "av_top_eta", 20, -5, 5, "Av. top \eta"],
                ["float",    "av_top_phi", 20, -3.1416, 3.1416, "Av. top \phi"],
                ["float",    "av_top_m", 20, 0, 500e+03, "Av. top m"],
                ["float",    "av_top_e", 20, 0, 2400e+03, "Av. top E"],
                ["float",    "av_top_y", 20, -2.9, 2.9, "Av. top y"],
                ["float",    "ttbar_pt", 20, 0, 900e+03, "ttbar p_{T}"],
                ["float",    "ttbar_eta", 20, -10, 10, "ttbar \eta"],
                ["float",    "ttbar_phi", 20, -3.1416, 3.1416, "ttbar \phi"],
                ["float",    "ttbar_m", 20, 0, 2500e+03, "ttbar m"],
                ["float",    "ttbar_e", 20, 0, 4700e+03, "ttbar E"],
                ["float",    "ttbar_y", 20, -2.9, 2.9, "ttbar y"], 
                ["float",    "ttbar_pout", 20, -700e+03, 700e+03, "ttbar p_{out}"],
                ["float",    "nu_pt", 20, 0, 600e+03, "\nu p_{T}"], 
                ["float",    "nu_eta", 20, -10, 10, "\nu \eta"],
                ["float",    "nu_phi", 20, -3.1416, 3.1416, "\nu \phi"],
                ["float",    "nu_m", 20, -0.2e+03, 0.2e+03, "\nu m"],
                ["float",    "nu_e", 20, 0, 3500e+03, "\nu E"],
                ["float",    "nu_y", 20, -2.9, 2.9, "\nu y"],
                ["float",    "nubar_pt", 20, 0, 600e+03, "\nubar p_{T}"],
                ["float",    "nubar_eta", 20, -10, 10, "\nubar \eta"],
                ["float",    "nubar_phi", 20, -3.1416, 3.1416, "\nubar \phi"],
                ["float",    "nubar_m", 20, -0.5e+03, 0.5e+03, "\nubar m"],
                ["float",    "nubar_e", 20, 0, 1800e+03, "\nubar E"],
                ["float",    "nubar_y", 20, -2.9, 2.9, "\nubar y"],
                ["float",    "Wp_pt", 20, 0, 800e+03, "W^{+} p_{T}"],
                ["float",    "Wp_eta", 20, -10, 10, "W^{+} \eta"],
                ["float",    "Wp_phi", 20, -3.1416, 3.1416, "W^{+} \phi"],
                ["float",    "Wp_m", 20, 0, 1000e+03, "W^{+} m"],
                ["float",    "Wp_e", 20, 0, 3600e+03, "W^{+} E"],
                ["float",    "Wp_y", 20, -2.9, 2.9, "W^{+} y"], 
                ["float",    "Wm_pt", 20, 0, 800e+03, "W^{-} p_{T}"],
                ["float",    "Wm_eta", 20, -10, 10, "W^{-} \eta"],
                ["float",    "Wm_phi", 20, -3.1416, 3.1416, "W^{-} \phi"],
                ["float",    "Wm_m", 20, 0, 1000e+03, "W^{-} m"],
                ["float",    "Wm_e", 20, 0, 1900e+03, "W^{-} E"],
                ["float",    "Wm_y", 20, -2.9, 2.9, "W^{-} y"]
#                ["Int_t",       "nu_n", 20, 0, 100e+03, "m_{lb}"]
		]

vectors = [
		["double",	"bjet_pt", 100, 0, 990e+03, "b_{jet} p_{T}"],
		["double",	"el_pt", 100, 0, 990e+03, "Electron p_{T}"]
		]

# Declare migration matrices, reco/part. histograms, eff. & fake hits
migrationMatrices = []
partHists = []
recoHists = []
effHists = []
faccHists = []

for obs in observables:
  mig = "tMatrix_" + obs[1]
  histP = "tPart_" + obs[1] 
  histR = "tReco_" + obs[1]
  eff = "tEff_"+ obs[1]
  facc = "tFacc_" + obs[1]
  nBins = obs[2]
  xMin = obs[3]
  xMax = obs[4]
  obsName = obs[5]
  migrationMatrices.append( TH2F(mig, "A_ij "+obsName, nBins, xMin, xMax, nBins, xMin, xMax ) )
  partHists.append( TH1F(histP, obsName+"^{part}", nBins, xMin, xMax ) )
  recoHists.append( TH1F(histR, obsName+"^{reco}", nBins, xMin, xMax ) )
  effHists.append( TH1F(eff, "\epsilon_{eff} "+obsName, nBins, xMin, xMax ) )
  faccHists.append( TH1F(facc, "f_{acc} "+obsName, nBins, xMin, xMax ) )

for vec in vectors:
  mig = "tMatrix_lead_" + vec[1]
  histP = "tPart_lead_" + vec[1]
  histR = "tReco_lead_" + vec[1]
  eff = "tEff_lead_"+ vec[1]
  facc = "tFacc_lead_" + vec[1]
  nBins = vec[2]
  xMin = vec[3]
  xMax = vec[4]
  obsName = vec[5]
  migrationMatrices.append( TH2F(mig, "A_ij lead. "+obsName, nBins, xMin, xMax, nBins, xMin, xMax ) )
  partHists.append( TH1F(histP, obsName+"1^{part}", nBins, xMin, xMax ) )
  recoHists.append( TH1F(histR, obsName+"1^{reco}", nBins, xMin, xMax ) )
  effHists.append( TH1F(eff, "\epsilon_{eff} lead. "+obsName, nBins, xMin, xMax ) )
  faccHists.append( TH1F(facc, "f_{acc} lead. "+obsName, nBins, xMin, xMax ) )

shift = len(observables)

recoLevel = TChain("nominal")
partLevel = TChain("particleLevel")

fileh = open(inputfile, 'r')
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
  globals()[vec[1]+'_reco'] = vector(obs[0])()
  globals()[vec[1]+'_part'] = vector(obs[0])()

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
fakeHits()

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

