#################################################################################
#										#
#############################   TOP MASS UPFOLDING   ############################
#										#
# This script uses any ROOT file with histograms on reco/particle level, to	#
# compute migration matrices, efficiencies and fake hits.			#
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

from ROOT import *

def populateHists(reco, obsR, part, obsP):
  global recoOnly
  global partOnly
  for i in range(reco.GetEntries()):
    if part.GetEntryWithIndex(obsR.runNumber, obsR.eventNumber) < 0: recoOnly += 1
    else:
	# Fill the reco/particle histograms, and the migration matrices
	for i,obs in enumerate(observables): 
	  x = obs[1] + "_part"
	  y = obs[1] + "_reco"
	  migrationMatrices[i].Fill(getattr(obsP,x), getattr(obsR.y))
	   

recoOnly = 0
partOnly = 0
observables = [["Double_t", "mlb_minavg", 20, 0, 350e+03]]

migrationMatrices = []
for obs in observables:
  name = "tMatrix_" + obs[1]
  nBins = obs[2]
  xMin = obs[3]
  xMax = obs[4]
  migrationMatrices.append( TH2F(name, "", nBins, xMin, xMax, nBins, xMin, xMax ) )
  
print migrationMatrices

myFile = TFile.Open("output_172.5_120K_AF2.root")

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

# Get the reco (nominal) and particle level branches
#
# Use the indexing to cross-find events matched on both levels and
# fill the histograms

nominal = nominal_t()
particleLevel = particleLevel_t()

recoLevel.SetBranchAddress("runNumber", AddressOf(nominal,'runNumber'))
recoLevel.SetBranchAddress("eventNumber", AddressOf(nominal,'eventNumber'))

for obs in observables:
  recoLevel.SetBranchAddress('tma_'+obs[1], AddressOf(nominal,obs[1]+'_reco'))
  partLevel.SetBranchAddress('tma_'+obs[1], AddressOf(particleLevel,obs[1]+'_part'))

populateHists(recoLevel, nominal, partLevel, particleLevel)
