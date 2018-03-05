from ROOT import *
import os, sys

output = "migration_matrices_bias"
os.system("mkdir "+output)

migr1 = sys.argv[1]
migr2 = sys.argv[2]

file1 = TFile.Open(migr1)
file2 = TFile.Open(migr2)

mtop1 = migr1.split("/")[-1].split("_mt")[1].split("_")[0]
mtop2 = migr2.split("/")[-1].split("_mt")[1].split("_")[0]

migrationMatrices1 = []
migrationMatrices2 = []

diff = []

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
    diff.Add(Aij2, -2)
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

