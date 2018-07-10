from ROOT import *

def ratioPlot(firstHist,secondHist,title,leg=0):
  hist1 = firstHist.Clone("hist1")
  hist1.SetStats(0)
  hist2 = secondHist.Clone("hist2")
  c2 = TCanvas("c2","c2",800,800)
  pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0) # Upper and lower plot are joined
  pad1.SetGridx()         # Vertical grid
  pad1.Draw()             # Draw the upper pad: pad1
  pad1.cd()               # pad1 becomes the current pad
#  hist1.SetStats(0)       # No statistics on upper plot
  hist1.Draw("eh")            # Draw hist1
  hist2.Draw("eh same")      # Draw hist2
  legend = TLegend(0.75,0.8,0.95,0.95);
  if leg == 0:
    legend.AddEntry(hist1,"Particle level","l");
    legend.AddEntry(hist2,"Reco level","l");
  elif leg == 1:
    legend.AddEntry(hist1,"Truth reco level","l");
    legend.AddEntry(hist2,"Folded reco level","l");
  legend.Draw();
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
