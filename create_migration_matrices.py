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
import os

timestr = strftime("%d-%m-%y--%H.%M.%S", gmtime())

outputMigr = "migration_matrices_"+timestr
outputEff  = "efficiencies_"+timestr
outputFacc = "fake_hits_rates_"+timestr


def populateHists(reco, obsR, part, obsP):
  global recoOnly
  global partOnly
  for i in range(reco.GetEntries()):
    if ((i+1) % 1000) == 0: print "Processing event number " + str(i+1) + "..."
    reco.GetEntry(i)
    for j,obs in enumerate(observables):
	y = obs[1] + "_reco"
	recoHists[j].Fill(getattr(obsR,y))
    # Check if the event only exists at reco level
    if part.GetEntryWithIndex(obsR.runNumber, obsR.eventNumber) < 0: recoOnly += 1
    # If not, it was matched -> fill out the migration matrices
    else:
	# Fill the reco/particle histograms, and the migration matrices
	for j,obs in enumerate(observables): 
	  x = obs[1] + "_part"
	  y = obs[1] + "_reco"
	  print i
	  print getattr(obsP,x)
	  print getattr(obsR,y)
	  effHists[j].Fill(getattr(obsP,x))
	  faccHists[j].Fill(getattr(obsR,y))
	  migrationMatrices[j].Fill(getattr(obsP,x), getattr(obsR,y))

def normalize():
  for i,obs in enumerate(observables):
    # Normalize each x-bin to 1
    for xbins in range(obs[2]):
	sum = 0
	for ybins in range(obs[2]): sum += migrationMatrices[i].GetBinContent(xbins, ybins)
	for ybins in range(obs[2]): 
	  if sum != 0: migrationMatrices[i].SetBinContent(xbins, ybins,
			migrationMatrices[i].GetBinContent(xbins, ybins) / float(sum))

def drawHists():
  os.system("mkdir " + outputMigr)
  c = TCanvas("c","c",900,900)
  c.cd()
  for i,obs in enumerate(observables):
    migrationMatrices[i].GetXaxis().SetTitle(obs[5] + "^{part}")
    migrationMatrices[i].GetYaxis().SetTitle(obs[5] + "^{reco}")
    migrationMatrices[i].Draw("COLZ")
    c.SaveAs(outputMigr + "/migration_" + obs[1] + ".pdf")



recoOnly = 0
partOnly = 0

# List of observables from which to build migration matrices
observables = [["Double_t", "mlb_minavg", 20, 0, 350e+03, "m_{lb}"]]

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
  migrationMatrices.append( TH2F(mig, "", nBins, xMin, xMax, nBins, xMin, xMax ) )
  partHists.append( TH1F(histP, "", nBins, xMin, xMax ) )
  recoHists.append( TH1F(histR, "", nBins, xMin, xMax ) )
  effHists.append( TH1F(eff, "", nBins, xMin, xMax ) )
  faccHists.append( TH1F(facc, "", nBins, xMin, xMax ) )

myFile = TFile.Open("output_172.5_120K_AF2.root")

# Get the reco (nominal) and particle level branches
#
# Use the indexing to cross-find events matched on both levels and
# fill the histograms

recoLevel = myFile.Get("nominal")
partLevel = myFile.Get("particleLevel")


recoLevel.BuildIndex("runNumber", "eventNumber")
partLevel.BuildIndex("runNumber", "eventNumber")

# Structs to loop through the branches (needed by SetBranchAddress)
struct1 = 'struct nominal_t{UInt_t runNumber;ULong64_t eventNumber;'
struct2 = 'struct particleLevel_t{UInt_t runNumber;ULong64_t eventNumber;'

for obs in observables:
  struct1 += obs[0] + ' ' + obs[1] + '_reco;'
  struct2 += obs[0] + ' ' + obs[1] + '_part;'

struct1 += '}'
struct2 += '}'

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

# Loop through the events & fill the histograms

populateHists(recoLevel, nominal, partLevel, particleLevel)
normalize()
drawHists()
