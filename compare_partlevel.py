from ROOT import *
import os, sys, math
from ratio_plot_ATLAS import ratioPlotATLAS


outputClosX1 = "particle_level_X1"

migr1 = sys.argv[1]
effic1= sys.argv[2]
fake1 = sys.argv[3]

hist1 = sys.argv[4]
hist2 = sys.argv[5]
reco1 = sys.argv[6]
reco2 = sys.argv[7]

file1 = TFile.Open(migr1)
effF1  = TFile.Open(effic1)
fakeF1 = TFile.Open(fake1)
histF1 = TFile.Open(hist1)
recoF1 = TFile.Open(reco1)
histF2 = TFile.Open(hist2)
recoF2 = TFile.Open(reco2)

mtop1 = migr1.split("/")[-1].split("_mt")[1].split("_")[0]
mtop2 = hist2.split("/")[-1].split("part_level_")[1].split(".")[0]

migrationMatrices1 = []
migrationMatrices2 = []

efficiencies1 = []
fakes1 = []
partHists1 = []
recoTruth1 = []
recoFolded1 = []
efficiencies2 = []
fakes2 = []
partHists2 = []
recoTruth2 = []
recoFolded2 = []

diff = []


for i in file1.GetListOfKeys():
  hist = i.GetName()
  print "Adding " + hist + " to the migration matrices..."
  hist1 = hist + "_" + mtop1
  globals()[hist1] = TH2F()
  file1.GetObject(hist, globals()[hist1])
  migrationMatrices1.append(globals()[hist1])

for i in histF1.GetListOfKeys():
  hist = i.GetName().split("tPart_")[1]
  eff = TH1F()
  fak = TH1F()
  part= TH1F()
  reco= TH1F()
  recoFolded=TH1F()
  effF1.GetObject("tEff_"+hist,eff)
  fakeF1.GetObject("tFacc_"+hist,fak)
  histF1.GetObject("tPart_"+hist,part)
  recoF1.GetObject("tReco_"+hist,reco)
  efficiencies1.append(eff)
  fakes1.append(fak)
  partHists1.append(part)
  recoTruth1.append(reco)
  recoFolded=reco.Clone("recoFolded")
  recoFolded1.append(recoFolded)

for i in histF2.GetListOfKeys():
  hist = i.GetName().split("tPart_")[1]
  part= TH1F()
  reco= TH1F()
  recoFolded=TH1F()
  histF2.GetObject("tPart_"+hist,part)
  recoF2.GetObject("tReco_"+hist,reco)
  partHists2.append(part)
  recoTruth2.append(reco)
  recoFolded=reco.Clone("recoFolded")
  recoFolded2.append(recoFolded)

os.system("mkdir "+outputClosX1)
for i, Aij1 in enumerate(migrationMatrices1):
  nbins = Aij1.GetXaxis().GetNbins()
  xmin = Aij1.GetXaxis().GetBinLowEdge(1)
  xmax = Aij1.GetXaxis().GetBinUpEdge(nbins)
  n1=partHists1[i].Integral()
  partHists1[i].Sumw2(kTRUE)
  partHists1[i].Scale(1./n1)
  n2=partHists2[i].Integral()
  partHists2[i].Sumw2(kTRUE)
  partHists2[i].Scale(1./n2)
  ratioPlotATLAS(partHists1[i], partHists2[i], outputClosX1 + "/" + Aij1.GetName().split("tMatrix_")[1], 1, 1)

