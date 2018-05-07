from ROOT import *
import os, sys, math

output = "migration_matrices_bias"
outputEff = "efficiencies_bias"
outputFacc = "fakes_bias"
outputClosX1 = "migration_matrices_bias_X1"
outputClosX2 = "migration_matrices_bias_X2"
os.system("mkdir "+output)
os.system("mkdir "+outputEff)
os.system("mkdir "+outputFacc)

migr1 = sys.argv[1]
migr2 = sys.argv[2]

effic1= sys.argv[3]
effic2= sys.argv[4]
fake1 = sys.argv[5]
fake2 = sys.argv[6]
hist1 = sys.argv[7]
hist2 = sys.argv[8]
reco1 = sys.argv[9]
reco2 = sys.argv[10]

file1 = TFile.Open(migr1)
file2 = TFile.Open(migr2)
effF1  = TFile.Open(effic1)
fakeF1 = TFile.Open(fake1)
histF1 = TFile.Open(hist1)
recoF1 = TFile.Open(reco1)
effF2  = TFile.Open(effic2)
fakeF2 = TFile.Open(fake2)
histF2 = TFile.Open(hist2)
recoF2 = TFile.Open(reco2)

mtop1 = migr1.split("/")[-1].split("_mt")[1].split("_")[0]
mtop2 = migr2.split("/")[-1].split("_mt")[1].split("_")[0]

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

def ratioPlot(firstHist,secondHist,title):
  hist1 = firstHist.Clone("hist1")
  hist2 = secondHist.Clone("hist2")
  c2 = TCanvas("c2","c2",800,800)
  pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0.01) # Upper and lower plot are joined
  pad1.SetGridx()         # Vertical grid
  pad1.Draw()             # Draw the upper pad: pad1
  pad1.cd()               # pad1 becomes the current pad
  hist1.SetStats(0)       # No statistics on upper plot
  hist1.Draw("He")            # Draw hist1
  hist2.Draw("He same")      # Draw hist2
  legend = TLegend(0.75,0.8,0.95,0.95);
  legend.AddEntry(hist1,"Folded reco. level","l");
  legend.AddEntry(hist2,"Truth reco. level","l");
  legend.Draw();

  # lower plot will be in pad
  c2.cd()          # Go back to the main canvas before defining pad2
  pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.29)
  pad2.SetTopMargin(0.01)
  pad2.SetBottomMargin(0.3)
  pad2.SetGridx() # vertical grid
  pad2.Draw()
  pad2.cd()       # pad2 becomes the current pad

  # Define the ratio plot
  h3 = hist1.Clone("h3")
  h3.SetLineColor(kBlack)
  h3.SetMinimum(0.5)  # Define Y ..
  h3.SetMaximum(1.5) # .. range
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

#  h3.GetYaxis().SetTitle("Ratio "+firstHist.GetTitle()+"/"+secondHist.GetTitle())
  h3.GetYaxis().SetTitle("Ratio folded/truth")
  h3.GetYaxis().SetNdivisions(505)
  h3.GetYaxis().SetTitleSize(20)
  h3.GetYaxis().SetTitleFont(43)
  h3.GetYaxis().SetTitleOffset(1.55)
  h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h3.GetYaxis().SetLabelSize(15)

  h3.GetXaxis().SetTitle(firstHist.GetTitle().split("^{part}")[0])
  h3.GetXaxis().SetTitleOffset(3.0)
  h3.GetXaxis().SetTitleSize(25)
  h3.GetXaxis().SetTitleFont(43)
  h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h3.GetXaxis().SetLabelSize(15)

  c2.SaveAs(title)
  c2.Close()


for i in file1.GetListOfKeys():
  hist = i.GetName()
  print "Adding " + hist + " to the migration matrices..."
  hist1 = hist + "_" + mtop1
  hist2 = hist + "_" + mtop2
  globals()[hist1] = TH2F()
  file1.GetObject(hist, globals()[hist1])
  migrationMatrices1.append(globals()[hist1])
  if file2.GetListOfKeys().Contains(hist):
    globals()[hist2] = TH2F()
    file2.GetObject(hist, globals()[hist2])
    migrationMatrices2.append(globals()[hist2])
  else:
    migrationMatrices2.append("")
    print "Branch " + hist + " not found in " + migr2

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
  eff = TH1F()
  fak = TH1F()
  part= TH1F()
  reco= TH1F()
  recoFolded=TH1F()
  effF2.GetObject("tEff_"+hist,eff)
  fakeF2.GetObject("tFacc_"+hist,fak)
  histF2.GetObject("tPart_"+hist,part)
  recoF2.GetObject("tReco_"+hist,reco)
  efficiencies2.append(eff)
  fakes2.append(fak)
  partHists2.append(part)
  recoTruth2.append(reco)
  recoFolded=reco.Clone("recoFolded")
  recoFolded2.append(recoFolded)

os.system("mkdir "+outputClosX1)
for i, Aij1 in enumerate(migrationMatrices1):
  nbins = Aij1.GetXaxis().GetNbins()
  for xbins in range(nbins+2):
        sum = 0.
	error1_2 = 0.
	error2_2 = 0.
	error3_2 = 0.
        for j in range(nbins+2): 
		sum += Aij1.GetBinContent(j,xbins) * partHists2[i].GetBinContent(j) \
                        * efficiencies1[i].GetBinContent(j)
		error1_2 += pow(Aij1.GetBinError(j,xbins) * partHists2[i].GetBinContent(j) \
                        * efficiencies1[i].GetBinContent(j), 2)
		error2_2 += pow(Aij1.GetBinContent(j,xbins) * partHists2[i].GetBinError(j) \
                        * efficiencies1[i].GetBinContent(j), 2)
		error3_2 += pow(Aij1.GetBinContent(j,xbins) * partHists2[i].GetBinContent(j) \
                        * efficiencies1[i].GetBinError(j), 2)
        if fakes1[i].GetBinContent(xbins) != 0: 
 		error2 = 1./pow(fakes1[i].GetBinContent(xbins),4) * pow(fakes1[i].GetBinError(xbins)*sum,2) 
		error2 += 1./pow(fakes1[i].GetBinContent(xbins),2) * ( error1_2 + error2_2 + error3_2 ) 
		sum *= 1./(fakes1[i].GetBinContent(xbins))
	else: error2 = 0.
        recoFolded2[i].SetBinContent(xbins, sum)
	recoFolded2[i].SetBinError(xbins, math.sqrt(error2))
	print error1_2
	print error2_2
	print error3_2
	print sum
	print math.sqrt(error2)
  ratioPlot(recoFolded2[i], recoTruth2[i], outputClosX1 + "/" + Aij1.GetName().split("tMatrix_")[1] + ".pdf")

os.system("mkdir "+outputClosX2)
for i, Aij2 in enumerate(migrationMatrices2):
  nbins = Aij2.GetXaxis().GetNbins()
  for xbins in range(nbins+2):
        sum = 0.
	error1_2 = 0.
	error2_2 = 0.
	error3_2 = 0.
        for j in range(nbins+2): 
		sum += Aij2.GetBinContent(j,xbins) * partHists1[i].GetBinContent(j) \
                        * efficiencies2[i].GetBinContent(j)
		error1_2 += pow(Aij2.GetBinError(j,xbins) * partHists1[i].GetBinContent(j) \
                        * efficiencies2[i].GetBinContent(j), 2)
		error2_2 += pow(Aij2.GetBinContent(j,xbins) * partHists1[i].GetBinError(j) \
                        * efficiencies2[i].GetBinContent(j), 2)
		error3_2 += pow(Aij2.GetBinContent(j,xbins) * partHists1[i].GetBinContent(j) \
                        * efficiencies2[i].GetBinError(j), 2)
        if fakes2[i].GetBinContent(xbins) != 0: 
		error2 = 1./pow(fakes2[i].GetBinContent(xbins),4) * pow(fakes2[i].GetBinError(xbins)*sum,2)
		error2 += 1./pow(fakes2[i].GetBinContent(xbins),2) * ( error1_2 + error2_2 + error3_2 ) 
		sum *= 1./(fakes2[i].GetBinContent(xbins))
	else: error2 = 0.
        recoFolded1[i].SetBinContent(xbins, sum)
	recoFolded1[i].SetBinError(xbins, math.sqrt(error2))
  ratioPlot(recoFolded1[i], recoTruth1[i], outputClosX2 + "/" + Aij2.GetName().split("tMatrix_")[1] + ".pdf")


for i, Aij1 in enumerate(migrationMatrices1):
  if migrationMatrices2[i] != "":
    print "Now treating " + Aij1.GetName()
    xmin = Aij1.GetXaxis().GetXmin()
    xmax = Aij1.GetXaxis().GetXmax()
    print "Preparing the fit function..."
    fit = TF2("fit", "[0]+0*x*y", xmin, xmax, xmin, xmax)
    fit.SetNpx(Aij1.GetXaxis().GetNbins()+1)
    fit.SetNpy(Aij1.GetXaxis().GetNbins()+1)
    Aij2 = migrationMatrices2[i]
    diff = Aij1.Clone("diff")
    diff.Add(Aij2, -1)
    toPlot = diff.Clone("A_{ij}^1 - A_{ij}^2")
    fitResult = diff.Fit("fit", "S")
    fitResult.Print()
    const = "%.4f" % fitResult.Value(0)
    err = "%.4f" % fitResult.Error(0)
    c = TCanvas("c","c",900,900)
    c.cd()
    fit.SetParameter(0, fitResult.Value(0))
    fit.SetTitle("")
    fit.GetZaxis().SetRangeUser(-1.,1.)
    fit.Draw("surf")
    toPlot.GetXaxis().SetLabelSize(0.001)
    toPlot.GetYaxis().SetLabelSize(0.001)
    toPlot.GetXaxis().SetTitleOffset(0.01)
    toPlot.GetYaxis().SetTitleOffset(0.01)
    toPlot.GetZaxis().SetRangeUser(-1.,1.)
    toPlot.Draw("surfe same")
    xlabel = TText();
    xlabel.SetNDC();
    xlabel.SetTextFont(1);
    xlabel.SetTextColor(1);
    xlabel.SetTextSize(0.02);
    xlabel.SetTextAlign(22);
    xlabel.SetTextAngle(0);
    result = "offset = " + str(const) + " +/- " + str(err)
    xlabel.DrawText(0.3, 0.9, result);
    c.SaveAs(output + "/" + Aij1.GetName() + "_" + mtop1 + "_" + mtop2 + ".pdf")
    c.Close()
    diff.Delete()
    fit.Delete()


for i, efficiencies1 in enumerate(efficiencies1):
  if efficiencies2[i] != "":
    print "Now treating " + efficiencies1.GetName()
    xmin = efficiencies1.GetXaxis().GetXmin()
    xmax = efficiencies1.GetXaxis().GetXmax()
    print "Preparing the fit function..."
    fit = TF1("fit", "[0]+0*x", xmin, xmax)
    diff = efficiencies1.Clone("diff")
    diff.Add(efficiencies2[i], -1)
    toPlot = diff.Clone("#epsilon_{eff}^1 - #epsilon_{eff}^2")
    fitResult = diff.Fit("fit", "S")
    fitResult.Print()
    const = "%.4f" % fitResult.Value(0)
    err = "%.4f" % fitResult.Error(0)
    c = TCanvas("c","c",900,900)
    c.cd()
    fit.SetParameter(0, fitResult.Value(0))
    fit.SetTitle("")
    fit.GetYaxis().SetRangeUser(-1.,1.)
    fit.Draw("cont")
    toPlot.GetXaxis().SetLabelSize(0.001)
    toPlot.GetYaxis().SetLabelSize(0.001)
    toPlot.GetXaxis().SetTitleOffset(0.01)
    toPlot.GetYaxis().SetTitleOffset(0.01)
    toPlot.Draw("pe same")
    xlabel = TText();
    xlabel.SetNDC();
    xlabel.SetTextFont(1);
    xlabel.SetTextColor(1);
    xlabel.SetTextSize(0.02);
    xlabel.SetTextAlign(22);
    xlabel.SetTextAngle(0);
    result = "offset = " + str(const) + " +/- " + str(err)
    xlabel.DrawText(0.3, 0.9, result);
    c.SaveAs(outputEff + "/" + efficiencies1.GetName() + "_" + mtop1 + "_" + mtop2 + ".pdf")
    c.Close()
    diff.Delete()
    fit.Delete()

for i, fakes1 in enumerate(fakes1):
  if fakes2[i] != "": 
    print "Now treating " + fakes1.GetName()
    xmin = fakes1.GetXaxis().GetXmin()
    xmax = fakes1.GetXaxis().GetXmax()
    print "Preparing the fit function..."
    fit = TF1("fit", "[0]+0*x", xmin, xmax)
    diff = fakes1.Clone("diff")
    diff.Add(fakes2[i], -1)
    toPlot = diff.Clone("f_{acc}^1 - f_{acc}^2")
    fitResult = diff.Fit("fit", "S")
    fitResult.Print()
    const = "%.4f" % fitResult.Value(0)
    err = "%.4f" % fitResult.Error(0)
    c = TCanvas("c","c",900,900)
    c.cd()
    fit.SetParameter(0, fitResult.Value(0))
    fit.SetTitle("")
    fit.GetYaxis().SetRangeUser(-1.,1.)
    fit.Draw("cont")
    toPlot.GetXaxis().SetLabelSize(0.001)
    toPlot.GetYaxis().SetLabelSize(0.001)
    toPlot.GetXaxis().SetTitleOffset(0.01)
    toPlot.GetYaxis().SetTitleOffset(0.01)
    toPlot.Draw("pe same")
    xlabel = TText();
    xlabel.SetNDC();
    xlabel.SetTextFont(1);
    xlabel.SetTextColor(1);
    xlabel.SetTextSize(0.02);
    xlabel.SetTextAlign(22);
    xlabel.SetTextAngle(0);
    result = "offset = " + str(const) + " +/- " + str(err)
    xlabel.DrawText(0.3, 0.9, result);
    c.SaveAs(outputFacc + "/" + fakes1.GetName() + "_" + mtop1 + "_" + mtop2 + ".pdf")
    c.Close()
    diff.Delete()
    fit.Delete()
