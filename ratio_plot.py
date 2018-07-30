from ROOT import *
from atlas_labels import *

AtlasStyle = atlasStyle()
AtlasStyle.SetErrorX(0.5)
AtlasStyle.SetPaintTextFormat("4.2f");
AtlasStyle.SetPalette(1)
gROOT.SetStyle("ATLAS")
gROOT.ForceStyle()
gROOT.SetBatch(True)

txt_size = 15

def ratioPlot(firstHist,secondHist,title,leg=0):

  hist1 = firstHist.Clone("hist1")
  hist2 = secondHist.Clone("hist2")
  c2 = TCanvas("c2","c2",800,800)
  pad1 = TPad("pad1","pad1", 0, 0.32, 1, 1.0)
  pad1.SetBottomMargin(0.01) # Upper and lower plot are joined
  pad1.SetLeftMargin(0.1) # Upper and lower plot are joined
  pad1.SetRightMargin(0.1) # Upper and lower plot are joined
  pad1.SetGridx()         # Vertical grid
  pad1.Draw()             # Draw the upper pad: pad1
  pad1.cd()               # pad1 becomes the current pad

  hist1.SetStats(0)
  hist1.SetTitle("")
  hist1.SetLineColor(kBlue+1)
  hist1.SetLineWidth(2)

  hist1.GetXaxis().SetLabelSize(0)
  hist2.GetXaxis().SetLabelSize(0)
  hist1.GetYaxis().SetTitleSize(txt_size/(pad1.GetWh()*pad1.GetAbsHNDC()))
  hist1.GetYaxis().SetLabelSize(txt_size/(pad1.GetWh()*pad1.GetAbsHNDC()))
  hist1.GetYaxis().SetTitle("N_{events}")
  hist2.GetYaxis().SetTitleSize(txt_size/(pad1.GetWh()*pad1.GetAbsHNDC()))
  hist2.GetYaxis().SetLabelSize(txt_size/(pad1.GetWh()*pad1.GetAbsHNDC()))
#  hist1.GetYaxis().SetTitleFont(43)
#  hist1.GetYaxis().SetTitleOffset(1.55)

  hist2.SetLineColor(kRed)
  hist2.SetLineWidth(2)


  hist1.Draw("eh")            # Draw hist1
  hist2.Draw("eh same")      # Draw hist2

  legend = TLegend(0.66, 0.70, 0.40, 0.80);
  legend.SetFillColor(0)
  legend.SetLineColor(0)
  legend.SetTextSize(0.033)
  if leg == 0:
    legend.AddEntry(hist1,"Particle level","l");
    legend.AddEntry(hist2,"Reco level","l");
  elif leg == 1:
    legend.AddEntry(hist1,"Truth reco level","l");
    legend.AddEntry(hist2,"Folded reco level","l");
  legend.Draw();

  # lower plot will be in pad
  c2.cd()          # Go back to the main canvas before defining pad2
  pad2 = TPad("pad2", "pad2", 0, 0.15, 1, 0.3)
  pad2.SetTopMargin(0.)
  pad2.SetBottomMargin(0.1)
  pad2.SetLeftMargin(0.1)
  pad2.SetRightMargin(0.1)
  pad2.SetGridx() # vertical grid
  pad2.Draw()
  pad2.cd()       # pad2 becomes the current pad

  # Define the ratio plot
  h3 = hist1.Clone("h3")
  h3.SetLineColor(kBlue+1)
#  h3.SetMinimum(0.0)  # Define Y ..
#  h3.SetMaximum(3.0) # .. range
  h3.Sumw2()
#  h3.SetStats(0)      # No statistics on lower plot
  h3.Divide(hist2)
#  h3.SetMarkerStyle(21)


  h3.SetStats(0)
  h3.SetTitle("")
  h3.GetYaxis().SetTitle("Ratio "+firstHist.GetTitle()+"/"+secondHist.GetTitle())
  h3.GetYaxis().SetTitleOffset(1.2)
#  h3.GetYaxis().SetNdivisions(505)
#  h3.GetYaxis().SetTitleSize(20)
#  h3.GetYaxis().SetTitleFont(43)
#  h3.GetYaxis().SetTitleOffset(1.55)
#  h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
#  h3.GetYaxis().SetLabelSize(25)

  h3.GetXaxis().SetTitle(firstHist.GetTitle().split("^{part}")[0])
  h3.GetXaxis().SetTitleSize(txt_size*2/(pad1.GetWh()*pad1.GetAbsHNDC()))
  h3.GetYaxis().SetTitleSize(txt_size*2/(pad1.GetWh()*pad1.GetAbsHNDC()))
  h3.GetXaxis().SetLabelSize(txt_size*2/(pad1.GetWh()*pad1.GetAbsHNDC()))
  h3.GetYaxis().SetLabelSize(txt_size*2/(pad1.GetWh()*pad1.GetAbsHNDC()))
#  h3.GetXaxis().SetTitleOffset(1.55)
#  h3.GetXaxis().SetTitleSize(25)
#  h3.GetXaxis().SetTitleFont(43)
#  h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
#  h3.GetXaxis().SetLabelSize(25)


  h3.Draw("ep")       # Draw the ratio plot



  c2.SaveAs(title)
  c2.Close()
