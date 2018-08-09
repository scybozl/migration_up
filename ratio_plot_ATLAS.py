from ROOT import *
from plotting.TH1_helpers import TH1_helper
from plotting.layout_helpers import layout_helper
from plotting.plotting_helpers import simplePlot
from plotting.plotting_helpers import ratioPlot

## Ratio plot class

def ratioPlotATLAS(firstHist,secondHist,title,legHist1,legHist2,particleLevel=0):

    hist1 = firstHist.Clone("hist1")
    hist2 = secondHist.Clone("hist2")
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerColor(1)
    hist1.SetMarkerSize(0.5)
    hist1.SetLineColor(1)
    hist2.SetLineColor(2)
    ph = ratioPlot()
    ph.setStyle(24)
    lh = layout_helper()
    # Prepare canvas and pads
    pads = ph.canvasAndPads(True)
    #pads[0].SetLogy()
    #pads[1].SetLogy()
    #pads[1].SetLogx()
    # ----------------------
    # Top pad
    # ----------------------
    # Setup layout helper
    plots = [hist1, hist2]
    lh.resetAttributes(pad = pads[0], plots = plots
    		       , xMin = None
    		       , xMax = None
                       , yMin = None
                       , legendNCol = 1
                       , letAtlasLabelFloat = False, yMaxOffset = 0.05, yMinOffset = 0.05
                       , textPlotsDist = 0.04999
                       , considerUncertainties = True
                       , topTextPosY = ph.topTextPosY, bottomTextPosY = ph.bottomTextPosY
                       , verbose = False, entryHeight = 0.065
                       , putTextAtTheTop = True, putTextAtTheBottom = True
    )
    atlasLabels = ["#font[72]{ATLAS} Preliminary", "#font[12]{Simulation}", "13 TeV"]
    if ( particleLevel ): atlasLabels += ["Particle level"]
    else: atlasLabels += ["Reco level"]
    lh.addLabel(atlasLabels)
    legList = []
    legList.append([hist1, legHist1, "l"])
    legList.append([hist2, legHist2, "l"])

    lh.addLegend([l[1] for l in legList])
    decorations = [""]
    lh.addText(decorations)
    # Calculate the optimal layout
    if not lh.placeAllTextToPad():
        return
    # Drawing the top pad frame
    ph.drawTopFrame(lh.getFrame().Clone(), "Events")
    # Drawing text objects to the top pad frame
    ph.drawTextBox(atlasLabels, lh.labelCoordinates()["TLatexPositions"])
    ph.drawLegend(legList, lh.legendCoordinates(0))
    ph.drawTextBox(decorations, lh.textCoordinates(0)["TLatexPositions"])
    hist1.Draw("same ep")
    hist2.Draw("same eh")
    pads[0].RedrawAxis()

    hRat = hist1.Clone()
    line = ph.lineAtOne(hist1.GetBinLowEdge(1),hist1.GetBinLowEdge(hist1.GetNbinsX()+1))

    hOne = hist1.Clone()
    hOne.Divide(hist1)
    hOne.SetFillColorAlpha(kRed, 0.5)
    hOne.SetMarkerSize(0)

    # Setup layout_helper
    lh.resetAttributes(pad = pads[1], plots = [hRat, line]
    		       , xMin = None
    		       , xMax = None
                       , verbose = False
                       , considerUncertainties = False
                       , yMinOffset = 0.06, yMaxOffset = 0.06
    )
    # Calculate the optimal layout
    if not lh.placeAllTextToPad():
        lh.clearStorage()
        lh.resetAttributesToNone()
        for p in pads:
            p.IsA().Destructor(p)
        return
    # Draw objects
    ph.drawBottomFrame(lh.getFrame().Clone(), hist1.GetXaxis().GetTitle(), "Ratio ")
    hRat.Divide(hist2)
    hOne.SetMinimum(0.)
    hOne.SetMaximum(2.)
    hOne.Draw("E2")
    hRat.Draw("same")
    line.Draw()
    pads[len(pads) - 1].SaveAs(title + "_log.pdf")
    lh.pad.RedrawAxis()
    # Terminate the session
    lh.clearStorage()
    lh.resetAttributesToNone()
    for p in pads:
        p.IsA().Destructor(p)

