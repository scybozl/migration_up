# Written by Vojtech Pleskot (vojtech.pleskot@cern.ch)

from plotting.__init__ import *
from plotting.TH1_helpers import TH1_helper
from plotting.layout_helpers import layout_helper
import ROOT
import math


#############################################
## The base class
#############################################

class plotting_base(TH1_helper):
    # Must be provided by the user
    # ----------------------------
    pad = None
    storage = None # storage of labels such that they don't get deleted
    
    def __init__(self):
        return

    #############################################
    ## Setters
    #############################################

    def setPad(self, pad):
        self.pad = pad
        if self.pad is None: return
        self.pad.cd()
        return

    def resetAttributesToNone(self):
        self.pad = None
        return
    
    def resetAttributes(self, pad = None):
        # Set all the variables to their initial values according to
        #    the user's input
        self.resetAttributesToNone()
        self.setPad(pad)
        return

    def clearStorage(self):
        self.storage = None
        return
    
    #############################################
    ## Methods for handling text objects
    #############################################

    def drawLegend(self, legList, coor):
        # legList is a list with one entry for each item in the legend;
        #    the entries are lists with the following structure:
        #    [myObject, "legend entry text", "type of picture, i.e. "f", "l" or "p""].
        # coor is dictionary with items "x1", "y1", "x2", "y2" and "nColumns".
        isGood = True
        if not isinstance(legList, list): isGood = False
        for e in legList:
            if not isinstance(e[0], TH1):
                if not isinstance(e[0], TGraph):
                    if not isinstance(e[0], THStack):
                        if not isinstance(e[0], TF1):
                            if not isinstance(e[0], TLine):
                                isGood = False
            if not isinstance(e[1], str): isGood = False
            if not isinstance(e[2], str): isGood = False
        if not isGood:
            print "In plotting_base.drawLegend():"
            print "    parameter legList must be a list like"
            print "    [myObject, \"legend entry text\", \"type of picture, i.e. \"f\", \"l\" or \"p\"\"]!"
            print "    myObject ... TH1, TGraph, THStack, TF1, TLine"
            print "    type of picture ... \"f\", \"l\" or \"p\""
            raise SystemExit()
        isGood = True
        if not isinstance(coor, dict): isGood = False
        if not "x1" in coor: isGood = False
        if not "y1" in coor: isGood = False
        if not "x2" in coor: isGood = False
        if not "y2" in coor: isGood = False
        if not "nColumns" in coor: isGood = False
        if not isGood:
            print "In plotting_base.drawLegend():"
            print "    parameter coor must be a dictionary with the following keys:"
            print "    \"x1\", \"y1\", \"x2\", \"y2\", \"nColumns\"."
            raise SystemExit()
        leg = TLegend(coor["x1"], coor["y1"], coor["x2"], coor["y2"])
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetBorderSize(0)
        leg.SetNColumns(coor["nColumns"])
        leg.SetTextSize(gStyle.GetTextSize())
        for e in legList:
            leg.AddEntry(e[0], e[1], e[2])
        leg.Draw()
        if self.storage is None:
            self.storage = []
        self.storage.append(leg)
        return
        
    def drawTextBox(self, entries, TLatexPositions):
        # entries is a list of str;
        # TLatexPositions is a list of dictionaries with items "x" and "y";
        #    there must be one dictionary corresponding to each str in entries.
        isGood = True
        if not isinstance(entries, list): isGood = False
        for e in entries:
            if not isinstance(e, str):
                isGood = False
        if not isGood:
            print "In plotting_base.drawTextBox():"
            print "    parameter entries must be a list of str!"
            raise SystemExit()
        isGood = True
        if not isinstance(TLatexPositions, list): isGood = False
        for pos in TLatexPositions:
            if not isinstance(pos, dict): isGood = False
            if not "x" in pos: isGood = False
            if not "y" in pos: isGood = False
        if not isGood:
            print "In plotting_base.drawTextBox():"
            print "    parameter TLatexPositions must be a list of dictionaries;"
            print "    the dictionaries must contain keys \"x\" and \"y\"."
            raise SystemExit()
        if len(entries) != len(TLatexPositions):
            print "In plotting_base.drawTextBox():"
            print "    different number of items in lists entries and TLatexPositions!"
            raise SystemExit()
        if self.storage is None:
            self.storage = []
        for i in range(len(entries)):
            t = TLatex(TLatexPositions[i]["x"], TLatexPositions[i]["y"], entries[i])
            t.SetNDC()
            t.Draw()
            self.storage.append(t)
        return
    
    def lineAtOne(self, xMin = None, xMax = None):
        if xMin is None or xMax is None:
            print "ERROR: in plotting_base.lineAtOne(): None provided as parameter!"
            print "       xMin", xMin, "xMax", xMax
            raise SystemExit()
        line = TLine(xMin, 1, xMax, 1)
        line.SetLineColor(2)
        line.SetLineStyle(1)
        line.SetLineWidth(1)
        return line

    def lineAtZero(self, xMin = None, xMax = None):
        if xMin is None or xMax is None:
            print "ERROR: in plotting_base.lineAtZero(): None provided as parameter!"
            print "       xMin", xMin, "xMax", xMax
            raise SystemExit()
        line = TLine(xMin, 0, xMax, 0)
        line.SetLineColor(1)
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        return line

    def lineAtY(self, y, xMin = None, xMax = None):
        if xMin is None or xMax is None:
            print "ERROR: in plotting_base.lineAtY(): None provided as parameter!"
            print "       xMin", xMin, "xMax", xMax
            raise SystemExit()
        line = TLine(xMin, y, xMax, y)
        line.SetLineColor(1)
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        return line


class ratioPlot(plotting_base):
    topTextPosY = 0.90
    bottomTextPosY = 0.06
    topRightTextPosX = 0.915
    bottomRightTextPosX = 0.915
    topLeftTextPosX = 0.195
    bottomLeftTextPosX = 0.195
    topTextPosY_ratio = 0.88
    bottomTextPosY_ratio = 0.4

    def __init__(self):
        return

    def canvasAndPads(self, setLogy = False, name = "c"):
        # Create canvas and pads for a ratio plot: two pads -
        #    absolute at the top and ratio at the bottom.
        gStyle.SetPadLeftMargin(0.16)
        gStyle.SetPadRightMargin(0.05)
        gStyle.SetPadBottomMargin(0.16)
        gStyle.SetPadTopMargin(0.05)
        cmother = TCanvas(name, name, 600, 600)
        cmother.cd()
        # Main pad
        n = "{0}_main".format(name)
        pmain = TPad(n, n, 0, 0.358, 1, 1)
        pmain.SetTopMargin(0.057)
        pmain.SetBottomMargin(0.03)
        if setLogy:
            pmain.SetLogy()
        pmain.Draw()
        # Ratio pad
        cmother.cd()
        n = "{0}_ratio".format(name)
        pratio = TPad(n, n, 0, 0, 1, 0.358)
        pratio.SetBottomMargin(0.33)
        pratio.Draw()
        SetOwnership(pmain, True)
        SetOwnership(pratio, True)
        SetOwnership(cmother, True)
        return [pmain, pratio, cmother]

    def drawTopFrame(self, frame, yAxTitle):
        # frame is typically obtained from the layout_helper()
        # x-axis
        frame.GetXaxis().SetTitleSize(0)
        frame.GetXaxis().SetLabelSize(0)
        frame.GetXaxis().SetNdivisions(505)
        frame.GetXaxis().SetTickLength(0.04)
        #frame.GetXaxis().SetNoExponent()
        #frame.GetXaxis().SetMoreLogLabels()
        # y-axis
        frame.GetYaxis().SetTitle(yAxTitle)
        frame.GetYaxis().SetTitleOffset(1.8)
        frame.GetYaxis().SetNdivisions(505)
        frame.GetYaxis().SetTickLength(0.022)
        #frame.GetYaxis().SetNoExponent()
        #frame.GetYaxis().SetMoreLogLabels()
        frame.GetYaxis().SetDecimals()
        frame.Draw()
        if self.storage is None:
            self.storage = []
        self.storage.append(frame)
        return

    def drawBottomFrame(self, frame, xAxTitle, yAxTitle):
        # frame is typically obtained from the layout_helper()
        # x-axis
        frame.GetXaxis().SetTitle(xAxTitle)
        frame.GetXaxis().SetTitleOffset(0.2)
        frame.GetXaxis().SetNdivisions(505)
        frame.GetXaxis().SetTickLength(0.073)
	frame.GetXaxis().SetLabelSize(0.2)
        #frame.GetXaxis().SetNoExponent()
        #frame.GetXaxis().SetMoreLogLabels()
        # y-axis
        frame.GetYaxis().SetTitle(yAxTitle)
        frame.GetYaxis().SetTitleOffset(1.8)
        frame.GetYaxis().SetNdivisions(505)
        frame.GetYaxis().SetTickLength(0.033)
	frame.SetMinimum(0.0)
	frame.SetMaximum(2.0)
        #frame.GetYaxis().SetNoExponent()
        #frame.GetYaxis().SetMoreLogLabels()
        frame.GetYaxis().SetDecimals()
        frame.Draw()
        if self.storage is None:
            self.storage = []
        self.storage.append(frame)
        return

    
class simplePlot(plotting_base):
    topTextPosY = 0.935
    bottomTextPosY = 0.14
    topRightTextPosX = 0.915
    bottomRightTextPosX = 0.915
    topLeftTextPosX = 0.195
    bottomLeftTextPosX = 0.195
    
    def __init__(self):
        return

    def canvasAndPads(self, setLogy = False, name = "c"):
        # Create canvas and pads for a ratio plot: two pads -
        #    absolute at the top and ratio at the bottom.
        gStyle.SetPadLeftMargin(0.16)
        gStyle.SetPadRightMargin(0.05)
        gStyle.SetPadBottomMargin(0.118)
        gStyle.SetPadTopMargin(0.037)
        c = TCanvas(name, name, 600, 600)
        c.cd()
        if setLogy:
            c.SetLogy()
        SetOwnership(c, True)
        return [c]

    def drawFrame(self, frame, xAxTitle, yAxTitle):
        # frame is typically obtained from the layout_helper()
        # x-axis
        frame.GetXaxis().SetTitle(xAxTitle)
        frame.GetXaxis().SetTitleOffset(0.0)
        frame.GetXaxis().SetNdivisions(505)
        frame.GetXaxis().SetTickLength(0.026)
        #frame.GetXaxis().SetNoExponent()
        #frame.GetXaxis().SetMoreLogLabels()
        # y-axis
        frame.GetYaxis().SetTitle(yAxTitle)
        frame.GetYaxis().SetTitleOffset(1.8)
        frame.GetYaxis().SetNdivisions(505)
        frame.GetYaxis().SetTickLength(0.0235)
        #frame.GetYaxis().SetNoExponent()
        #frame.GetYaxis().SetMoreLogLabels()
        frame.GetYaxis().SetDecimals()
        frame.Draw()
        if self.storage is None:
            self.storage = []
        self.storage.append(frame)
        return

    

