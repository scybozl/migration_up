
from time import gmtime, strftime
from ROOT import *
import os, sys
from math import ceil,floor
observables = [
		["Int_t",	"nbjets", 8, 0, 8, "n_{b,jets}"],
		["Int_t",	"njets", 15, 0, 15, "n_{jets}"],
		["Double_t",	"etdr", 15, 0, 15, "n_{jets}"],
		["Double_t",	"met", 15, 0, 15, "n_{jets}"],
		["Double_t",	"met_ex", 15, 0, 15, "n_{jets}"],
		["Double_t",	"met_ey", 15, 0, 15, "n_{jets}"],
		["Double_t",	"met_phi", 15, 0, 15, "n_{jets}"],
		["Double_t",	"mlb_minavg", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mlb_minavglow", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mlb_minavghigh", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mlb_minmax", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mlb_minmaxlow", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mlb_minmaxhigh", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"pTlb_1", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"pTlb_2", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"dRlb_1", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"dRlb_2", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mll", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"pTll", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"dRll", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"mbb", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"pTbb", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"dRbb", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"top_ratio", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"tbar_ratio", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"av_top_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"ttbar_pout", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nu_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"nubar_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wp_y", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_pt", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_eta", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_phi", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_m", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_e", 20, 0, 350e+03, "m_{lb}"],
		["Double_t",	"Wm_y", 20, 0, 350e+03, "m_{lb}"],
		["Int_t",	"nu_n", 20, 0, 350e+03, "m_{lb}"]
		]

vectors = [
		["double",	"bjet_pt", 100, 0, 990e+03, "b_{jet} p_T"]
		]

recoLevel = TChain("nominal")
partLevel = TChain("particleLevel")

recoLevel.Add("output_172.5_120K_AF2.root")
partLevel.Add("output_172.5_120K_AF2.root")


recoIndex = TTreeIndex(recoLevel, "runNumber", "eventNumber")
partIndex = TTreeIndex(partLevel, "runNumber", "eventNumber")
recoLevel.SetTreeIndex(recoIndex)
partLevel.SetTreeIndex(partIndex)

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
#  recoLevel.SetBranchAddress('tma_'+obs[1] AddressOf(nominal,obs[1]+'_reco'))
#  partLevel.SetBranchAddress('tma_'+obs[1] AddressOf(particleLevel,obs[1]+'_part'))
  minR = recoLevel.GetMinimum('tma_'+obs[1])
  minP = partLevel.GetMinimum('tma_'+obs[1])
  minn = min(minR,minP)

  maxR = recoLevel.GetMaximum('tma_'+obs[1])
  maxP = partLevel.GetMaximum('tma_'+obs[1])
  maxx = max(maxR,maxP)


  fl = floor(minn / 100000.) * 100000.
  cl = ceil(maxx / 100000.) * 100000

  print 'tma_'+obs[1] + "\t" + str(minn) + "\t" + str(maxx) + "\n\t\t" + str(fl) + "\t" + str(cl)+ "\n"


