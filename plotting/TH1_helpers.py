# Written by Vojtech Pleskot (vojtech.pleskot@cern.ch)

from plotting.__init__ import *
from math import sqrt
import ROOT

class TH1_helper(object):
    fn = None
    canvasNo = 0
    date = ""

    def __init__(self, fn = None):
        self.fn = fn
        return
    
    def setDate(self, date):
        self.date = date
        return
    
    def setFileName(self, fn):
        self.fn = fn
        return
    
    def getFileName( self ):
        return self.fn
    
    def getRootFile(self, fn = None):
        rootFile = None
        if fn is None: fn = self.fn
        rootFile = TFile.Open(fn, "read")
        if rootFile is None: print "ERROR: file ", fn, " does not exist"
        return rootFile
    
    def getHisto(self, hn = None, fn = None):
        rootFile = self.getRootFile(fn)
        histo = None
        if hn is None:
            print "ERROR: in TH1_helper.getHisto():"
            print "    histogram name is not provided"
        histo = rootFile.Get(hn)
        if histo is None:
            print "ERROR: in TH1_helper.getHisto():"
            print "    histo", hn, "does not exist in the root file", fn
        histo.SetDirectory(0)
        rootFile.Close()
        return histo
    
    def setZero(self, histo):
        for ib in range(histo.GetNbinsX() + 2):
            histo.SetBinContent(ib, 0)
            histo.SetBinError(ib, 0)
        return
    
    def setErrorsToZero(self, histo):
        for ib in range(histo.GetNbinsX() + 2):
            histo.SetBinError(ib, 0)
        return
    
    def createCanvas(self, sizeX = 600, sizeY = 600, name = "c"):
        name = "{0}_{1}".format(name, self.canvasNo)
        c = TCanvas(name, name, sizeX, sizeY)
        self.canvasNo += 1
        return c
    
    def changeBinLimits(self, histo, axis):
        # Typically, histo has bin limits 1,2,3... as bootstraps have
        #    and the axis has the binning we want (e.g. pt-binning in case of JIXS).
        # Histo and axis must have the same number of bins!
        # This methods creates new histo and returns it.
        nbins = histo.GetNbinsX()
        if nbins != axis.GetNbins():
            print "ERROR: in TH1_helper.changeBinLimits(): different number of bins in histo {0}: {1} and provided axis: {2}".format( histo.GetName(), nbins, axis.GetNbins() )
            return None
        bins = []
        for ib in range(1, nbins + 2):
            bins.append(axis.GetBinLowEdge(ib))
        newHisto = TH1D( histo.GetName(), histo.GetTitle(), nbins, array("d", bins) )
        for ib in range(1, nbins + 1):
            newHisto.SetBinContent(ib, histo.GetBinContent(ib))
            newHisto.SetBinError(ib, histo.GetBinError(ib))
        return newHisto
    
    def changeBinLimitsBs(self, bs, axis):
        # Typically, bootstrap has bin limits 1,2,3...
        #    and the axis has the binning we want (e.g. pt-binning in case of JIXS).
        # Bootstrap and axis must have the same number of bins!
        # This method does nor create new bootstrap!
        #    It just changes the binning of each its histo axis.
        nbins = bs.GetNominal().GetNbinsX()
        if nbins != axis.GetNbins():
            print "ERROR: in TH1_helper.changeBinLimits(): different number of bins in histo {0}: {1} and provided axis: {2}".format(bs.GetNominal().GetName(), nbins, axis.GetNbins())
            return None
        bins = []
        for ib in range(1, nbins + 2):
            bins.append(axis.GetBinLowEdge(ib))
        bs.GetNominal().GetXaxis().Set(nbins, array("d", bins))
        for ir in range(bs.GetNReplica()):
            bs.GetReplica(ir).GetXaxis().Set(nbins, array("d", bins))
        return
    
    def checkCompatibility(self, axis1, axis2, epsilon = 1.e-6):
        # check whether axis1 and axis2 have compatible binning
        # return negative number if not
        # return 1 if their binning is exactly the same
        # return 0 if they have different number of bins
        #  but overlaping bin edges
        # epsilon defines an interval within which two edges
        #  are considered as overlaping
        nbins1 = axis1.GetNbins()
        nbins2 = axis2.GetNbins()
        shortAx = axis1
        shortNb = nbins1
        longAx = axis2
        if nbins2 < nbins1:
            shortAx = axis2
            shortNb = nbins2
            longAx = axis1
        for ib in range(1, shortNb + 2):
            shb = shortAx.GetBinLowEdge(ib)
            #x = shortAx.GetBinCenter(ib)
            x = shb + epsilon
            lb = longAx.GetBinLowEdge(longAx.FindBin(x))
            if not self.isZero(shb - lb, epsilon): return -1
        if nbins1 == nbins2: return 1
        return 0
    
    def getNonZeroMin(self, h, xMin = None, xMax = None):
        if xMin is None:
            xMin = h.GetBinLowEdge(1)
        if xMax is None:
            xMax = h.GetBinLowEdge(h.GetNbinsX() + 1)
        if xMax <= xMin:
            print "in getNonZeroMin()"
            print "xMax ({0}) is lower or equal to xMin ({1})".format(xMax, xMin)
            raise SystemExit()
        eps = 1.e-9
        if self.isAtBinEdge(xMin, h, eps):
            xMin = xMin + abs(xMin * eps)
        if self.isAtBinEdge(xMax, h, eps):
            xMax = xMax - abs(xMax * eps)
        bmin = h.GetXaxis().FindBin(xMin)
        bmax = h.GetXaxis().FindBin(xMax)
        minimum = -1
        for ib in range(bmin, bmax + 1):
            cont = h.GetBinContent(ib)
            if cont > 0:
                minimum = cont
                break
        if minimum < 0:
            return None
        for ib in range(bmin, bmax + 1):
            cont = h.GetBinContent(ib)
            if cont > 0 and cont < minimum:
                minimum = cont
        return minimum
    
    def hasSameBinLimits(self, his1, bin1, his2, bin2, epsilon = 1.e-6):
        xl1 = his1.GetBinLowEdge(bin1)
        xh1 = his1.GetBinLowEdge(bin1 + 1)
        xl2 = his2.GetBinLowEdge(bin2)
        xh2 = his2.GetBinLowEdge(bin2 + 1)
        if not self.isZero(xl1 - xl2, epsilon):
            return False
        if not self.isZero(xh1 - xh2, epsilon):
            return False
        return True

    def compareContent1D(self, h1, h2, epsilon, xmin = 1, xmax = -1):
        # Compares contents of all the bins between xmin and xmax
        # Both the xmin, xmax have meaning of bin numbers of h1;
        #   the corresponding bin numbers of h2 do not necessarily be the same but
        #   h2 must have compatible binning (see checkCompatibility()
        #   for the definition of compatibility).
        # The level of agreement required is set by the number epsilon.
        # return -1 if the histograms have incompatible binning
        # return 0 if the histograms have the same content
        # return (positive and non-zero) number of the bins where there is
        #   a different content
        if self.checkCompatibility(h1.GetXaxis(), h2.GetXaxis()) < 0:
            print "ERROR: incompatible binning of", h1.GetName(), "and", h2.GetName()
            return -1
        if xmin > xmax:
            xmin = 1
            xmax = h1.GetNbinsX()
        nDiffBins = 0
        for xb1 in range(xmin, xmax+1):
            cx = h1.GetXaxis().GetBinCenter(xb1)
            xb2 = h2.GetXaxis().FindBin(cx)
            cont1 = h1.GetBinContent(xb1)
            cont2 = h2.GetBinContent(xb2)
            #      print h1.GetBinLowEdge(xb1), h1.GetBinLowEdge(xb1+1), cont1, cont2
            denom = cont1
            if denom == 0.: denom = cont2
            if denom == 0.: continue
            if not self.isZero((cont1 - cont2) / denom, epsilon):
                nDiffBins += 1
        return nDiffBins

    def changeHistoRange(self, histo, xmin, xmax, epsilon = 1.e-6):
        # Returns a histogram whose binning starts at xmin and ends at xmax.
        # xmin and xmax must be some bin limits of the histogram histo!
        # Contents and errors of all the bins between xmin and xmax are 
        #   copied from histo to the newHisto.
        bin1 = histo.FindBin(xmin + epsilon)
        bin2 = histo.FindBin(xmax - epsilon)
        newNbins = bin2 - bin1 + 1
        newBins = []
        for ib in range(bin1, bin2 + 2):
            newBins.append(histo.GetBinLowEdge(ib))
        newHisto = TH1D(histo.GetName(), histo.GetTitle(), newNbins, array("d", newBins))
        for ib in range(bin1, bin2 + 1):
            newIB = ib - bin1 + 1
            newHisto.SetBinContent(newIB, histo.GetBinContent(ib))
            newHisto.SetBinError(newIB, histo.GetBinError(ib))
        return newHisto
    
    def changeBsRange(self, bs, xmin, xmax, epsilon = 1.e-6):
        # Returns a bootstrap whose binning starts at xmin and ends at xmax.
        # xmin and xmax must be some bin limits of the bootstap histograms!
        # Contents and errors of all the bins between xmin and xmax are 
        #   copied from bs to the newBs.
        hTempl = bs.GetNominal()
        bin1 = hTempl.FindBin(xmin + epsilon)
        bin2 = hTempl.FindBin(xmax - epsilon)
        newNbins = bin2 - bin1 + 1
        newBins = []
        for ib in range(bin1, bin2 + 2):
            newBins.append(hTempl.GetBinLowEdge(ib))
        nrep = bs.GetNReplica()
        newBs = ROOT.TH1DBootstrap(bs.GetName(), bs.GetTitle(), newNbins, array("d", newBins), nrep)
        for ir in range(nrep):
            for ib in range(bin1, bin2 + 1):
                newIB = ib - bin1 + 1
                newBs.GetReplica(ir).SetBinContent(newIB, bs.GetReplica(ir).GetBinContent(ib))
                newBs.GetReplica(ir).SetBinError(newIB, bs.GetReplica(ir).GetBinError(ib))
        return newBs
    
    def setBinContentBs(self, bs, xBin, cont):
        nrep = bs.GetNReplica()
        for ir in range(nrep):
            bs.GetReplica(ir).SetBinContent(xBin, cont)
        return
    
    def setBinErrorBs(self, bs, xBin, err):
        nrep = bs.GetNReplica()
        for ir in range(nrep):
            bs.GetReplica(ir).SetBinError(xBin, err)
        return
    
    def histoToGraph(self, histo, xmin = 0, xmax = -1, epsilon = 1.e-6):
        # epsilon is used to evaluate (non-)equalities;
        #    it must be set appropriately to the histogram!
        nb = histo.GetNbinsX()
        lowb = 1
        highb = nb
        if xmin > xmax:
            #print "INFO: In histoToGraph(): no limits provided, will convert all the histo range"
            xmin = histo.GetBinLowEdge(1)
            xmax = histo.GetBinLowEdge(nb + 1)
        else:
            lowb = histo.FindBin(xmin + epsilon)
            highb = histo.FindBin(xmax - epsilon)
            nb = highb - lowb + 1
        gr = TGraphAsymmErrors(nb)
        for ib in range(lowb, highb + 1):
            x = histo.GetBinCenter(ib)
            exlow = x - histo.GetBinLowEdge(ib)
            exhigh = histo.GetBinLowEdge(ib + 1) - x
            y = histo.GetBinContent(ib)
            eylow = histo.GetBinError(ib)
            eyhigh = histo.GetBinError(ib)
            gr.SetPoint(ib - lowb, x, y)
            gr.SetPointError(ib - lowb, exlow, exhigh, eylow, eyhigh)
        return gr

    def histoBandToGraph(self, errH, errL, nom = None, centralValue = None
                         , xmin = 0, xmax = -1, epsilon = 1.e-6):
        # This methods returns a graph whose meaning is 1 sigma error band
        #    around contents of a histogram nom.
        # If nom is not provided the band points are set to zero.
        # errH and errL are up and down boundaries of the 1 sigma error band.
        #    Their binning does not need to be the same but it must be 
        #    compatible, i.e. bin edges must overlap.
        # Binning of the graph will be the finer binning from errH, errL.
        # If xmin and xmax are not provided, range of the finer binned 
        #    histogram is used.
        if self.checkCompatibility(errH.GetXaxis(), errL.GetXaxis()) < 0:
            print "In histoBandToGraph(): incompatible binning of errH and errL"
            self.printBinEdges(errH, errL)
            raise SystemExit()
        if nom is not None:
            if self.checkCompatibility(nom.GetXaxis(), errH.GetXaxis()) < 0:
                print "In histoBandToGraph(): incompatible binning of nom and errH"
                self.printBinEdges(nom, errH)
                raise SystemExit()
        # Iteration will be over bins of the finer binned histogram.
        nbH = errH.GetNbinsX()
        nbL = errL.GetNbinsX()
        finer = errH
        nb = nbH
        if nbL > nbH:
            finer = errL
            nb = nbL
        if xmin > xmax:
            xmin = finer.GetBinLowEdge(1)
            xmax = finer.GetBinLowEdge(nb + 1)
        # Iterate over bins of the finer binned histogram.
        lowb = finer.FindBin(xmin + epsilon)
        highb = finer.FindBin(xmax - epsilon)
        nb = highb - lowb + 1
        gr = TGraphAsymmErrors(nb)
        for ib in range(lowb, highb + 1):
            x = finer.GetBinCenter(ib)
            binH = errH.FindBin(x)
            binL = errL.FindBin(x)
            exlow = x - finer.GetBinLowEdge(ib)
            exhigh = finer.GetBinLowEdge(ib + 1) - x
            y = 0.
            if nom is not None:
                binNom = nom.FindBin(x)
                y = nom.GetBinContent(binNom)
            eyhigh = errH.GetBinContent(binH) - y
            eylow = y - errL.GetBinContent(binL)
            gr.SetPoint(ib - lowb, x, y)
            gr.SetPointError(ib - lowb, exlow, exhigh, eylow, eyhigh)
        return gr
    
    def calculateRatio(self, h1, h2):
        if 0 > self.checkCompatibility(h1.GetXaxis(), h2.GetXaxis()):
            print "ERROR: in calculateRatio(): incompatible binning"
            return
        ratio = h2.Clone()
        self.setZero(ratio)
        for ib2 in range(1, h2.GetNbinsX() + 1):
            ib1 = h1.FindBin(h2.GetBinCenter(ib2))
            y1 = h1.GetBinContent(ib1)
            y2 = h2.GetBinContent(ib2)
            if y2 != 0.:
                ratio.SetBinContent(ib2, y1 / y2)
        return ratio
    
    def calculateRatioFromBs_asymErrors(self, bs1, bs2):
        if 0 > self.checkCompatibility(bs1.GetNominal().GetXaxis()
                                       , bs2.GetNominal().GetXaxis()):
            print "ERROR: in calculateRatioFromBs_asymErrors(): incompatible binning"
            return
        ratioBs = ROOT.TH1DBootstrap(bs1)
        ratioBs.Divide(bs2)
        ratio = ratioBs.GetNominal().Clone("ratio")
        errUp = ratio.Clone("errUp")
        errDown = ratio.Clone("errDown")
        self.setZero(errUp)
        self.setZero(errDown)
        for ib in range(1, ratio.GetNbinsX() + 1):
            eu2 = 0.
            ed2 = 0.
            mean = ratio.GetBinContent(ib)
            counterUp = 0.
            counterDown = 0.
            for ir in range(ratioBs.GetNReplica()):
                diff = ratioBs.GetReplica(ir).GetBinContent(ib) - mean
                if diff >= 0.:
                    eu2 += diff * diff
                    counterUp += 1.
                if diff <= 0.:
                    ed2 += diff * diff
                    counterDown += 1.
            if counterUp != 0.:
                errUp.SetBinContent(ib, TMath.Sqrt(eu2 / counterUp))
            else:
                errUp.SetBinContent(ib, 0.)
            if counterDown != 0.:
                errDown.SetBinContent(ib, TMath.Sqrt(ed2 / counterDown))
            else:
                errDown.SetBinContent(ib, 0.)
        return [ratio, errUp, errDown]
    
    def calculateProduct(self, h1, h2):
        if 0 > self.checkCompatibility(h1.GetXaxis(), h2.GetXaxis()):
            print "ERROR: in calculateProduct(): incompatible binning"
            print "   histo1:", h1.GetName(), "histo2:", h2.GetName
            return None
        prod = h2.Clone()
        self.setZero(prod)
        for ib2 in range(1, h2.GetNbinsX() + 1):
            ib1 = h1.FindBin(h2.GetBinCenter(ib2))
            y1 = h1.GetBinContent(ib1)
            y2 = h2.GetBinContent(ib2)
            prod.SetBinContent(ib2, y1 * y2)
        return prod
    
    def setStyle(self, textSizePixels):
        newStyle = TStyle("NEW", "New style")
        newStyle.SetFrameBorderMode(0)
        newStyle.SetFrameFillColor(0)
        newStyle.SetCanvasBorderMode(0)
        newStyle.SetCanvasColor(0)
        newStyle.SetPadBorderMode(0)
        newStyle.SetPadColor(0)
        newStyle.SetStatColor(0)
        newStyle.SetPaperSize(20,26)
        newStyle.SetPadTopMargin(0.)
        newStyle.SetPadRightMargin(0.)
        newStyle.SetPadBottomMargin(0.)
        newStyle.SetPadLeftMargin(0.)
        newStyle.SetTitleXOffset(2.5)
        newStyle.SetTitleYOffset(1.8)
        newStyle.SetTextFont(43)
        newStyle.SetTextSize(textSizePixels)
        newStyle.SetLabelFont(43, "x")
        newStyle.SetTitleFont(43, "x")
        newStyle.SetLabelFont(43, "y")
        newStyle.SetTitleFont(43, "y")
        newStyle.SetLabelFont(43, "z")
        newStyle.SetTitleFont(43, "z")
        newStyle.SetLabelSize(textSizePixels, "x")
        newStyle.SetTitleSize(textSizePixels, "x")
        newStyle.SetLabelSize(textSizePixels, "y")
        newStyle.SetTitleSize(textSizePixels, "y")
        newStyle.SetLabelSize(textSizePixels, "z")
        newStyle.SetTitleSize(textSizePixels, "z")
        newStyle.SetMarkerStyle(20)
        newStyle.SetMarkerSize(1.2)
        newStyle.SetLineWidth(2)
        #newStyle.SetHistLineWidth(2.)
        newStyle.SetLegendFont(43)
        newStyle.SetLineStyleString(2, "[12 12]")
        newStyle.SetEndErrorSize(0.)
        newStyle.SetOptTitle(0)
        newStyle.SetOptStat(0)
        newStyle.SetOptFit(0)
        newStyle.SetPadTickX(1)
        newStyle.SetPadTickY(1)
        newStyle.SetStripDecimals(False)
        gROOT.SetStyle("NEW")
        return newStyle
    
    def divideCanvas_ver1(self, NpadsX, NpadsY, leftMargin, rightMargin, topMargin, bottomMargin, spaceAlongX, spaceAlongY):
        # NpadsX is the number of subpads to be created "on the X axis".
        # NpadsY is the number of subpads to be created "on the Y axis".
        # Margins and spaces (between pads) are in percents of the corresponding subpads to be created:
        #    leftMargin   ... in percents of the left pads
        #    rightMargin  ... in percents of the right pads
        #    spaceAlongX  ... in percents of the right pads
        #    topMargin    ... in percents of the top pads
        #    bottomMargin ... in percents of the botton pads
        #    spaceAlongY  ... in percents of the top pads
        # The method does allow space between frames.
        #    By frame is meant the rectangle bounded by graph axes that goes to the subpads.
        # The method creates all the pads and stores them in a list of pads.
        #    The pads must be stored and returned not to be deleted at the end of the method.
        #    When they are not needed, they must deleted by hand; in your macro use:
        #    for ip in range(NpadsX*NpadsY):
        #      SetOwnership(pads[ip], True)
        #      pads[ip].IsA().Destructor(pads[ip])
        pads = []
        # The explanation of the method starts with the simple case of no space between frames.
        #    The generalization to the case of non-zero space between frames is then easy.
        # 1) Zero space between frames:
        # dx is the frame width (frame in each subpad) in percents of the mother canvas.
        #    Pay attention: dx is NOT the subpad width.
        #    Each subpad has different width depending on the left and right margins.
        #    To have all the frames with equal width, one must think and calculate:
        #    NpadsX * dx + lm + rm = 1
        #    ... lm is the left subpad margin in percents of the mother canvas
        #    ... rm is the right subpad margin in percents of the mother canvas
        #    lm = leftMargin * (dx + lm) = 
        #       = leftMargin * (dx + leftMargin * (dx + lm))
        #       = leftMargin * (dx + leftMargin * (dx + leftMargin * (dx + lm)))
        #       = leftMargin * dx + leftMargin^2 * dx + leftMargin^3 * dx + ...
        #       = leftMargin * dx * (1 + leftMargin + leftMargin^2 + ...)
        #       = leftMargin * dx * 1 / (1 - leftMargin)
        #    The same situation is for the right margin.
        #    Therefore, formula NpadsX * dx + lm + rm = 1 is equivalent to
        #    NpadsX * dx + leftMargin * dx * 1 / (1 - leftMargin) + rightMargin * dx * 1 / (1 - rightMargin) = 1
        #    and to
        #    dx = 1. / (NpadsX + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin))
        # The same situation as for dx and the left and the right margins is for
        #    dy and the top and the bottom margins.
        #    tm = topMargin * dy / (1 - topMargin)
        #        tm is the top margin in percents of the mother canvas
        #    bm = bottomMargin * dy / (1 - bottomMargin)
        #        bm is the bottom margin in percents of the mother canvas
        #    dy = 1. / (NpadsY + topMargin / (1 - topMargin) + bottomMargin / (1 - bottomMargin))
        #        dy is the frame height in percents of the mother canvas
        #
        # 2) Non-zero space between frames:
        # The space between pads in the horizontal rows is attached to the frame
        #    on the right from the space.
        #    Therefore, lm remains the same as in case 1).
        #    rm must be recomputed:
        #    ... sx is the space between frames in percents of the mother canvas.
        #    We start with:
        #        rm = rightMargin * (dx + rm + sx)
        #        sx = spaceAlongX * (dx + rm + sx)
        #    Therefore:
        #    rm = rightMargin * (dx + rm + sx) = 
        #       = rightMargin * (dx + (rightMargin + spaceAlongX) * (dx + rm + sx)) =
        #       = rightMargin * (dx + (rightMargin + spaceAlongX) * dx + (rightMargin + spaceAlongX)^2 * (dx + rm + sx)) =
        #       = rightMargin * dx / (1 - (rightMargin + spaceAlongX))
        #       = rightMargin * dx / (1 - rightMargin - spaceAlongX)
        #    In the same way we compute sx:
        #    sx = spaceAlongX * dx / (1 - rightMargin - spaceAlongX)
        #    The sum of all the horizontal elements in percents of the mother canvas must be equal to 1:
        #    NpadsX * dx + (NpadsX - 1) * sx + lm + rm = 1
        #    which is equivalent to:
        #    NpadsX * dx + (NpadsX - 1) * spaceAlongX * dx / (1 - rightMargin - spaceAlongX) +
        #        + leftMargin * dx / (1 - leftMargin) + rightMargin * dx / (1 - rightMargin - spaceAlongX) = 1
        #    which is equivalent to:
        #    dx = 1 / (NpadsX + (NpadsX - 1) * spaceAlongX / (1 - rightMargin - spaceAlongX) +
        #        + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin - spaceAlongX))
        
        # frame width in percents of the mother canvas
        dx = 1 / (NpadsX + (NpadsX - 1) * spaceAlongX / (1 - rightMargin - spaceAlongX) + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin - spaceAlongX))
        # left margin in percents of the mother canvas
        lm = leftMargin * dx / (1 - leftMargin)
        # right margin in percents of the mother canvas
        rm = rightMargin * dx / (1 - rightMargin - spaceAlongX)
        # space between frames in percents of the mother canvas
        sx = spaceAlongX * dx / (1 - rightMargin - spaceAlongX)
        # frame width in percents of the mother canvas
        dy = 1 / (NpadsY + (NpadsY - 1) * spaceAlongY / (1 - topMargin - spaceAlongY) + bottomMargin / (1 - bottomMargin) + topMargin / (1 - topMargin - spaceAlongY))
        # top margin in percents of the mother canvas
        tm = topMargin * dy / (1 - topMargin - spaceAlongY)
        # bottom margin in percents of the mother canvas
        bm = bottomMargin * dy / (1 - bottomMargin)
        # space between frames in percents of the mother canvas
        sy = spaceAlongY * dy / (1 - topMargin - spaceAlongY)
        # Now, create the subpads and assign them a unique number with 
        #    TPad::SetNumber() method so that it was possible to 
        #    cd to them from the mother canvas in the standard way
        #    canvas.cd(ipad).
        for ipy in range(1, NpadsY + 1):
            # Coordinates of the subpad to be created
            #    in percents of the mother canvas.
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            # Margins of the subpad to be created
            #    in percents of the subpad.
            lm_act = 0
            rm_act = 0
            tm_act = 0
            bm_act = 0
            for ipx in range(1, NpadsX + 1):
                name = "pad_{0}_{1}".format(ipx, ipy)
                if ipy == 1:
                    y1 = 1 - dy - tm
                    y2 = 1
                    bm_act = 0
                    tm_act = topMargin
                elif ipy != NpadsY:
                    y1 = 1 - ipy*dy - (ipy - 1)*sy - tm
                    y2 = 1 - (ipy - 1)*(dy + sy) - tm
                    bm_act = 0
                    tm_act = 0
                else:
                    y1 = 0
                    y2 = 1 - (ipy - 1)*(dy + sy) - tm
                    bm_act = bottomMargin
                    tm_act = 0
                if ipx == 1:
                    x1 = 0
                    x2 = dx + lm
                    lm_act = leftMargin
                    rm_act = 0
                    print "dx:", dx, "lm:", lm, "leftMargin:", leftMargin
                elif ipx != NpadsX:
                    x1 = (ipx - 1)*(dx + sx) + lm
                    x2 = ipx*dx + (ipx - 1)*sx + lm
                    lm_act = 0
                    rm_act = 0
                else:
                    x1 = (ipx - 1)*(dx + sx) + lm
                    x2 = 1
                    lm_act = 0
                    rm_act = rightMargin
                # Create the subpad and set its margins.
                # Note: the TPad constructor takes the coordinates
                #    in percents of the mother canvas.
                # Note: the TPad::Set...Margin methods take the
                #    coordinates in percents of the subpad.
                pad = TPad(name, name, x1, y1, x2, y2, -1, 0)
                pad.SetLeftMargin(lm_act)
                pad.SetRightMargin(rm_act)
                pad.SetBottomMargin(bm_act)
                pad.SetTopMargin(tm_act)
                pad.SetNumber((ipy - 1)*NpadsX + ipx)
                pad.Draw()
                pads.append(pad)
        return pads
    
    def divideCanvas_ver2(self, NpadsX, NpadsY, leftMargin, rightMargin, topMargin, bottomMargin, spaceAlongX, spaceAlongY):
        # This method does a very similar thing as divideCanvas(). The only
        #    exception is that it treats the space between pads in a
        #    different way. The previous method puts the frames into subpads
        #    with zero ("internal") borders whereas this method implements
        #    the spaces as borders of the subpads.
        # NpadsX is the number of subpads to be created "on the X axis".
        # NpadsY is the number of subpads to be created "on the Y axis".
        # Margins and spaces (between pads) are in percents of the corresponding subpads to be created:
        #    leftMargin   ... in percents of the left pads
        #    rightMargin  ... in percents of the right pads
        #    spaceAlongX  ... in percents of the right pads
        #    topMargin    ... in percents of the top pads
        #    bottomMargin ... in percents of the botton pads
        #    spaceAlongY  ... in percents of the top pads
        # The method does allow space between frames.
        #    By frame is meant the rectangle bounded by graph axes that goes to the subpads.
        # The method creates all the pads and stores them in a list of pads.
        #    The pads must be stored and returned not to be deleted at the end of the method.
        #    When they are not needed, they must deleted by hand; in your macro use:
        #    for ip in range(NpadsX*NpadsY):
        #      SetOwnership(pads[ip], True)
        #      pads[ip].IsA().Destructor(pads[ip])
        pads = []
        # The explanation of the method starts with the simple case of no space between frames.
        #    The generalization to the case of non-zero space between frames is then easy.
        # 1) Zero space between frames:
        # dx is the frame width (frame in each subpad) in percents of the mother canvas.
        #    Pay attention: dx is NOT the subpad width.
        #    Each subpad has different width depending on the left and right margins.
        #    To have all the frames with equal width, one must think and calculate:
        #    NpadsX * dx + lm + rm = 1
        #    ... lm is the left subpad margin in percents of the mother canvas
        #    ... rm is the right subpad margin in percents of the mother canvas
        #    lm = leftMargin * (dx + lm) = 
        #       = leftMargin * (dx + leftMargin * (dx + lm))
        #       = leftMargin * (dx + leftMargin * (dx + leftMargin * (dx + lm)))
        #       = leftMargin * dx + leftMargin^2 * dx + leftMargin^3 * dx + ...
        #       = leftMargin * dx * (1 + leftMargin + leftMargin^2 + ...)
        #       = leftMargin * dx * 1 / (1 - leftMargin)
        #    The same situation is for the right margin.
        #    Therefore, formula NpadsX * dx + lm + rm = 1 is equivalent to
        #    NpadsX * dx + leftMargin * dx * 1 / (1 - leftMargin) + rightMargin * dx * 1 / (1 - rightMargin) = 1
        #    and to
        #    dx = 1. / (NpadsX + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin))
        # The same situation as for dx and the left and the right margins is for
        #    dy and the top and the bottom margins.
        #    tm = topMargin * dy / (1 - topMargin)
        #        tm is the top margin in percents of the mother canvas
        #    bm = bottomMargin * dy / (1 - bottomMargin)
        #        bm is the bottom margin in percents of the mother canvas
        #    dy = 1. / (NpadsY + topMargin / (1 - topMargin) + bottomMargin / (1 - bottomMargin))
        #        dy is the frame height in percents of the mother canvas
        #
        # 2) Non-zero space between frames:
        # The space between pads in the horizontal rows is attached to the frame
        #    on the right from the space.
        #    Therefore, lm remains the same as in case 1).
        #    rm must be recomputed:
        #    ... sx is the space between frames in percents of the mother canvas.
        #    We start with:
        #        rm = rightMargin * (dx + rm + sx)
        #        sx = spaceAlongX * (dx + rm + sx)
        #    Therefore:
        #    rm = rightMargin * (dx + rm + sx) = 
        #       = rightMargin * (dx + (rightMargin + spaceAlongX) * (dx + rm + sx)) =
        #       = rightMargin * (dx + (rightMargin + spaceAlongX) * dx + (rightMargin + spaceAlongX)^2 * (dx + rm + sx)) =
        #       = rightMargin * dx / (1 - (rightMargin + spaceAlongX))
        #       = rightMargin * dx / (1 - rightMargin - spaceAlongX)
        #    In the same way we compute sx:
        #    sx = spaceAlongX * dx / (1 - rightMargin - spaceAlongX)
        #    The sum of all the horizontal elements in percents of the mother canvas must be equal to 1:
        #    NpadsX * dx + (NpadsX - 1) * sx + lm + rm = 1
        #    which is equivalent to:
        #    NpadsX * dx + (NpadsX - 1) * spaceAlongX * dx / (1 - rightMargin - spaceAlongX) +
        #        + leftMargin * dx / (1 - leftMargin) + rightMargin * dx / (1 - rightMargin - spaceAlongX) = 1
        #    which is equivalent to:
        #    dx = 1 / (NpadsX + (NpadsX - 1) * spaceAlongX / (1 - rightMargin - spaceAlongX) +
        #        + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin - spaceAlongX))
        
        # frame width in percents of the mother canvas
        dx = 1 / (NpadsX + (NpadsX - 1) * spaceAlongX / (1 - rightMargin - spaceAlongX) + leftMargin / (1 - leftMargin) + rightMargin / (1 - rightMargin - spaceAlongX))
        # left margin in percents of the mother canvas
        lm = leftMargin * dx / (1 - leftMargin)
        # right margin in percents of the mother canvas
        rm = rightMargin * dx / (1 - rightMargin - spaceAlongX)
        # space between frames in percents of the mother canvas
        sx = spaceAlongX * dx / (1 - rightMargin - spaceAlongX)
        # frame width in percents of the mother canvas
        dy = 1 / (NpadsY + (NpadsY - 1) * spaceAlongY / (1 - topMargin - spaceAlongY) + bottomMargin / (1 - bottomMargin) + topMargin / (1 - topMargin - spaceAlongY))
        # top margin in percents of the mother canvas
        tm = topMargin * dy / (1 - topMargin - spaceAlongY)
        # bottom margin in percents of the mother canvas
        bm = bottomMargin * dy / (1 - bottomMargin)
        # space between frames in percents of the mother canvas
        sy = spaceAlongY * dy / (1 - topMargin - spaceAlongY)
        # Now, create the subpads and assign them a unique number with 
        #    TPad::SetNumber() method so that it was possible to 
        #    cd to them from the mother canvas in the standard way
        #    canvas.cd(ipad).
        for ipy in range(1, NpadsY + 1):
            # Coordinates of the subpad to be created
            #    in percents of the mother canvas.
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            # Margins of the subpad to be created
            #    in percents of the subpad.
            lm_act = 0
            rm_act = 0
            tm_act = 0
            bm_act = 0
            for i in range(1, NpadsX + 1):
                # Invert the order of drawing pads into the canvas to avoid
                #    frame border lines being drawn too thin due to pads overlap.
                ipx = NpadsX + 1 - i
                name = "pad_{0}_{1}".format(ipx, ipy)
                if ipy == 1:
                    y1 = 1 - tm - dy - sy
                    y2 = 1
                    bm_act = spaceAlongY # by definition (see above)
                    tm_act = topMargin
                elif ipy != NpadsY:
                    y1 = 1 - tm - ipy*(dy + sy)
                    y2 = 1 - tm - (ipy - 1)*(dy + sy)
                    # The bottom margin of the "middle" pads is the
                    #    space along Y (sy) divided by the pad height
                    #    (sy + dy). Both are (and must be!) in the same
                    #    units, of course.
                    bm_act = sy / (sy + dy)
                    tm_act = 0
                else:
                    y1 = 0
                    y2 = 1 - tm - (ipy - 1)*(dy + sy)
                    print "y1 =", 1 - tm - (ipy - 1)*(dy + sy) - dy - bm
                    bm_act = bottomMargin
                    tm_act = 0
                if ipx == 1:
                    x1 = 0
                    x2 = lm + dx
                    lm_act = leftMargin
                    rm_act = 0
                elif ipx != NpadsX:
                    x1 = lm + (ipx - 1)*dx + (ipx - 2)*sx
                    x2 = lm + ipx*dx + (ipx - 1)*sx
                    # The left margin of the "middle" pads is the
                    #    space along X (sx) divided by the pad width
                    #    (sx + dx). Both are (and must be!) in the same
                    #    units, of course.
                    lm_act = sx / (sx + dx)
                    rm_act = 0
                else:
                    x1 = lm + (ipx - 1)*dx + (ipx - 2)*sx
                    x2 = 1
                    print "xN =", lm + ipx*dx + (ipx - 1)*sx + rm
                    lm_act = spaceAlongX # by definition (see above)
                    rm_act = rightMargin
                # Create the subpad and set its margins.
                # Note: the TPad constructor takes the coordinates
                #    in percents of the mother canvas.
                # Note: the TPad::Set...Margin methods take the
                #    coordinates in percents of the subpad.
                pad = TPad(name, name, x1, y1, x2, y2, -1, 0)
                pad.SetLeftMargin(lm_act)
                pad.SetRightMargin(rm_act)
                pad.SetBottomMargin(bm_act)
                pad.SetTopMargin(tm_act)
                pad.SetNumber((ipy - 1)*NpadsX + ipx)
                pad.Draw()
                pads.append(pad)
        return pads
    
    def createUnitHisto(self, h):
        unit = TH1D(h)
        for ib in range(unit.GetNbinsX() + 2):
            unit.SetBinContent(ib, 1)
            unit.SetBinError(ib, 0)
        unit.SetName("unit")
        unit.SetTitle("unit")
        return unit
    
    def getBinEdgesList(self, axis):
        nbins = axis.GetNbins()
        bins = []
        for ib in range(1, nbins + 2):
            bins.append(axis.GetBinLowEdge(ib))
        return bins
    
    def readProgramInputParameters(self, names):
        # This method reads in the user input parameters.
        # names is a list of lists of the type [keyword, letter]
        #    e.g. names = [["help", "h"], ["name=", "n:"]]
        # The method returns a dictionary of the input parameters (strings)
        #    keys are keywords from the list names.
        #    e.g. retrieve a value passed by -n like
        #        myname = readProgramInputParameters()["name="]
        # If a keyword does not expect a value (e.g. "help")
        #    the returned value of params[myKeyword] is an empty string
        #    (e.g. params["help"] == "").
        # A program can be passed parameters in two ways:
        #    -j 833
        #    --jobNumber=833
        # -j 833 corresponds to the letter "j:";
        #    ":" means that an argument needs to be passed after the letter
        # --jobNumber=833 corresponds to the keyword "--jobNumber=";
        #    "=" means that a value is expected after the keyword
        letters = ""
        #    letters can look like "hj:f:";
        keywords = []
        #    keywords can look like ['help','jobNumber=','file='];
        for i in range(len(names)):
            if len(names[i]) < 2:
                print "ERROR: in readProgramInputParameters(): wrong input"
                print names[i]
                return None
            keywords.append(names[i][0])
            letters += names[i][1]
        # getopt starts at the second element of argv since the first one is the script name.
        # extraparams are extra arguments passed after all option/keywords are assigned.
        # opts is a list containing the pair 'option'/'value'.
        opts, extraparams = getopt.getopt(sys.argv[1:], letters, keywords)
        params = {}
        for i in range(len(names)):
            keyword = "--{0}".format(names[i][0])
            if keyword[-1:] == "=":
                keyword = keyword[:-1]
            letter = "-{0}".format(names[i][1])
            if letter[-1:] == ":":
                letter = letter[:-1]
            for o, p in opts:
                if o in [keyword, letter]:
                    params[names[i][0]] = p
        return params
    
    def getMaxAndMin(self, h, xMin = None, xMax = None):
        # h is a histogram.
        # The method returns maximum and minimum value of the histogram
        #    in the selected range (xMin, xMax).
#        if xMin is None:
#            xMin = h.GetBinLowEdge(1)
#        if xMax is None:
#            xMax = h.GetBinLowEdge(h.GetNbinsX() + 1)
        xMin = h.GetBinLowEdge(1)
        xMax = h.GetBinLowEdge(h.GetNbinsX() + 1)
	
        if xMax <= xMin:
            print "in getMaxAndMin()"
            print "xMax ({0}) is lower or equal to xMin ({1})".format(xMax, xMin)
            raise SystemExit()
        eps = 1.e-9
        if self.isAtBinEdge(xMin, h, eps):
            xMin = xMin + abs(xMin * eps)
        if self.isAtBinEdge(xMax, h, eps):
            xMax = xMax - abs(xMax * eps)
        minB = h.FindBin(xMin)
        if minB < 1:
            minB = 1
        maxB = h.FindBin(xMax)
        if maxB > h.GetNbinsX():
            maxB = h.GetNbinsX()
        yMax = h.GetMinimum()
        yMin = h.GetMaximum()
        for ib in range(minB, maxB + 1):
            cont = h.GetBinContent(ib)
            if cont > yMax:
                yMax = cont
            if cont < yMin:
                yMin = cont
        return yMax, yMin
    
    def getMaxAndMinOfHistos(self, hList, xMin = None, xMax = None):
        # hList is a list of histograms
        # The method returns maximum and minimum value of all
        #    the histograms in the selected range (xMin, xMax).
        yMax, yMin = self.getMaxAndMin(hList[0], xMin, xMax)
        for h in hList:
            hMax, hMin = self.getMaxAndMin(h, xMin, xMax)
            if hMax > yMax:
                yMax = hMax
            if hMin < yMin:
                yMin = hMin
        return yMax, yMin
    
    def isAtBinEdge(self, value, histo, eps = 1.e-9):
        for ib in range(1, histo.GetNbinsX() + 2):
            if self.isZero(value - histo.GetBinLowEdge(ib), eps):
                return True
        return False

    def isZero(self, x, eps = None):
        if eps is None:
            eps = 1.e-9
        if abs(x) < eps:
            return True
        return False

    def isClose(self, x, y, eps_rel = 1.e-9, eps_abs = 0.):
        return abs(x - y) <= max(eps_rel * max(abs(x), abs(y)), eps_abs)
    
    def printBinEdges(self, h1, h2):
        # The method prints edges of histograms h1 and h2
        #    side by side to ease check of binning differences.
        bins1 = self.getBinEdgesList(h1.GetXaxis())
        nb1 = len(bins1)
        bins2 = self.getBinEdgesList(h2.GetXaxis())
        nb2 = len(bins2)
        longer = bins1
        if nb2 > nb1:
            longer = bins2
        for i in range(min(nb1, nb2)):
            print "{0}\t{1}".format(bins1[i], bins2[i])
        for i in range(min(nb1, nb2), max(nb1, nb2)):
            if nb1 > nb2:
                print "{0}\t{1}".format(bins1[i], "")
            else:
                print "{0}\t{1}".format("", bins2[i])
        return
    
    def TH1toTH1D(self, h):
        bins = self.getBinEdgesList(h.GetXaxis())
        Nbins = len(bins) - 1
        newH = TH1D(h.GetName(), h.GetTitle(), Nbins, array("d", bins))
        for ib in range(1, Nbins + 1):
            newH.SetBinContent(ib, h.GetBinContent(ib))
            newH.SetBinError(ib, h.GetBinError(ib))
        return newH
    
    def powHisto(self, h, exp):
        newH = h.Clone()
        self.setZero(newH)
        for ib in range(1, newH.GetNbinsX() + 1):
            newH.SetBinContent(ib, pow(h.GetBinContent(ib), exp))
        return newH
    
    def sumTHStack(self, s):
        sSum = s.GetHists()[0].Clone()
        ## ROOT 6 style
        #for ih in range(1, s.GetNhists()):
        #  sSum.Add(s.GetHists()[ih])
        # ROOT 5 style
        for ih in range(1, len(s.GetHists())):
            if ih == 0: continue
            sSum.Add(s.GetHists()[ih])
        return sSum
    
    def graphToHistos(self, gr):
        # Returns a list of three histograms:
        #   histos[0] ... nominal value (NV) of the graph
        #   histos[1] ... NV + up error
        #   histos[2] ... NV - down error
        x = ROOT.Double(0)
        y = ROOT.Double(0)
        # Get bin edges
        bins = []
        for i in range(gr.GetN()):
            gr.GetPoint(i, x, y)
            if (gr.GetErrorXlow(i) <= 0 
                or (i == gr.GetN() - 1 and gr.GetErrorXhigh(i) <= 0)
                ):
                print "ERROR: in graphToHistos(): a TGraph with no/unsupported uncertainties along the x-axis provided."
                print "       Zero or negative uncertainties along the x-axis are not supported"
                print "       since the TGraph needs to be converted to a histogram internally."
                print "       If you are using TGraph, switch to TGraphErrors or TGraphAsymmErrors!"
                print "       Set the uncertainties! Such that:"
                print "         - for all points: your_graph.GetErrorXlow(iPoint) > 0"
                print "         - for a point i: x(i) < x(i + 1) - your_graph.GetErrorXlow(i + 1)"
                print "         - for a point i = your_graph.GetN(): your_graph.GetErrorXhigh(i) > 0"
                print "       NOTE: You can try to use the method TH1_helper.setGraphErrorsX() but"
                print "             it is not guaranteed it will fit your needs."
                raise SystemExit()
            bins.append(x - gr.GetErrorXlow(i))
            if i == gr.GetN() - 1:
                bins.append(x + gr.GetErrorXhigh(i))
        # Create the histograms
        hNom = TH1D(gr.GetName(), gr.GetTitle(), len(bins) - 1, array("d", bins))
        hUp = hNom.Clone()
        hDown = hNom.Clone()
        # Fill the histograms
        for i in range(gr.GetN()):
            gr.GetPoint(i, x, y)
            ib = hNom.GetXaxis().FindBin(x)
            hNom.SetBinContent(ib, y)
            hUp.SetBinContent(ib, y + gr.GetErrorYhigh(i))
            hDown.SetBinContent(ib, y - gr.GetErrorYlow(i))
        return [hNom, hUp, hDown]
    
    def setGraphErrorsX(self, gr):
        # gr is a TGraph. Method returns a "copy" of gr.
        # This "copy" is TGraphAsymmErrors regardless of the type of gr.
        # The uncertainties along the x-axis are guessed
        #    from the positions of the points on the x-axis.
        np = gr.GetN()
        gr_new = TGraphAsymmErrors(np)
        x, y = ROOT.Double(0), ROOT.Double(0)
        x2, y2 = ROOT.Double(0), ROOT.Double(0)
        for i in range(np):
            gr.GetPoint(i, x, y)
            if np == 0:
                ex = abs(x) / 2.
            elif i < np - 1:
                gr.GetPoint(i + 1, x2, y2)
                ex = (x2 - x) / 2.
            else:
                gr.GetPoint(i - 1, x2, y2)
                ex = (x - x2) / 2.
            if ex <= 0:
                print "ERROR: in TH1_helper.setGraphErrorsX(): seems like points"
                print "       in the provided graph are not ordered according to x!"
                raise SystemExit()
            eyl, eyh = 0, 0
            if `type(gr)` != "<class 'ROOT.TGraph'>":
                eyl, eyh = gr.GetErrorYlow(i), gr.GetErrorYhigh(i)
            gr_new.SetPoint(i, x, y)
            gr_new.SetPointError(i, ex, ex, eyl, eyh)
        return gr_new

    def rebinViaTH1Method(self, h, newname, rebin):
        if isinstance(rebin, int):
            newH = h.Rebin(rebin, newname)
            return newH.Clone()
        if isinstance(rebin, list):
            nb = len(rebin) - 1
            newH = h.Rebin(nb, newname, array("d", rebin))
            return newH.Clone()
        print "ERROR: in rebinViaTH1Method(): parameter rebin must be int or list! Provided type is", type(rebin)
        return None

    def isEquidistantBinning(self, bins, epsilon = None):
        if epsilon is None:
            epsilon = self.minBinWidth(bins) * 1.e-6
        for ib in range(len(bins) - 2):
            w1 = abs(bins[ib + 1] - bins[ib])
            w2 = abs(bins[ib + 2] - bins[ib + 1])
            if not self.isZero(w1 - w2, epsilon):
                return False
        return True
    
    def minBinWidth(self, bins):
        if len(bins) < 2:
            print "ERROR: in minBinWidth(): tuple bins has less than 2 elements! Returning None"
            return None
        width = bins[1] - bins[0]
        for ib in range(len(bins) - 1):
            tmp = abs(bins[ib + 1] - bins[ib])
            if tmp < width and tmp > 0:
                width = tmp
        return width
                
    def setLine(self, h, color = 1, style = 1, width = 3):
        h.SetLineColor(color)
        h.SetLineStyle(style)
        h.SetLineWidth(width)
        return
    
    def setFill(self, h, color = 1, style = 1001):
        h.SetFillColor(color)
        h.SetFillStyle(style)
        return
    
    def setMarker(self, h, color = 1, style = 1, size = 3):
        h.SetMarkerColor(color)
        h.SetMarkerStyle(style)
        h.SetMarkerSize(size)
        return
    
    def colorScheme(self, col):
        if col == 0: return ROOT.kBlack
        if col == 1: return ROOT.kRed
        if col == 2: return ROOT.kBlue
        if col == 3: return ROOT.kOrange + 2
        if col == 4: return ROOT.kGreen + 2
        if col == 5: return ROOT.kViolet
        if col == 6: return ROOT.kRed - 6
        if col == 7: return ROOT.kCyan + 1
        print "ERROR: in colorScheme():"
        print "    parameter range is 0-7; provided parameter:", col
        raise SystemExit()

    def logarithmicBins(self, NBins, xMin, xMax):
        xMin = math.log(xMin, 10)
        xMax = math.log(xMax, 10)
        width = (xMax - xMin) / NBins
        bins = []
        for i in range(NBins + 1):
            bins.append(pow(10, xMin + i * width))
        return bins

    def graphWithPoissonErrors(self, h):
        # Returns TGraphAsymmErrors with poisson uncertainties.
        # ATTENTION: only works for unweighted histograms!
        gr = self.histoToGraph(h)
        h.Sumw2(False)
        h.SetBinErrorOption(ROOT.TH1.kPoisson)
        x, y = ROOT.Double(0), ROOT.Double(0)
        for ip in range(gr.GetN()):
            gr.GetPoint(ip, x, y)
            gr.SetPointEYlow(ip, h.GetBinErrorLow(ip + 1))
            gr.SetPointEYhigh(ip, h.GetBinErrorUp(ip + 1))
        return gr
    
    
    
    
    
    
    
    
    
    
    



class TH2_helper(TH1_helper):
    def __init__(self, fn = None):
        TH1_helper.__init__(self, fn)
        return
    
    def getNonZeroMin(self, histo, xmin = 1, xmax = -1, ymin = 1, ymax = -1):
        if xmin > xmax:
            xmin = 1
            xmax = histo.GetNbinsX()
        if ymin > ymax:
            ymin = 1
            ymax = histo.GetNbinsY()
        minimum = -1
        for ibx in range( xmin, xmax+1 ):
            for iby in range( ymin, ymax+1 ):
                cont = histo.GetBinContent(ibx, iby)
                if cont > 0:
                    minimum = cont
                    break
        if minimum < 0: return None
        for ibx in range( xmin, xmax+1 ):
            for iby in range( ymin, ymax+1 ):
                cont = histo.GetBinContent(ibx, iby)
                if cont > 0 and cont < minimum:
                    minimum = cont
        return minimum
    
    def compareContent2D(self, h1, h2, epsilon, xmin = 1, xmax = -1, ymin = 1, ymax = -1):
        # Compares contents of all the bins between xmin and xmax on the x-axis and
        #   between ymin and ymax on the y-axis.
        # All the xmin, xmax, ymin, ymax have meaning of bin numbers of h1;
        #   the corresponding bin numbers of h2 do not necessarily be the same but
        #   h2 must have compatible binning (see checkCompatibility()
        #   for the definition of compatibility).
        # The level of agreement required is set by the number epsilon.
        #   This method looks for RELATIVE DIFFERENCE of the bin contents.
        # return -1 if the histograms have incompatible binning
        # return 0 if the histograms have the same content
        # return (positive and non-zero) number of the bins where there is
        #   a different content
        if self.checkCompatibility(h1.GetXaxis(), h2.GetXaxis()) < 0:
            print "ERROR: incompatible binning of", h1.GetName(), "and", h2.GetName()
            return -1
        if self.checkCompatibility(h1.GetYaxis(), h2.GetYaxis()) < 0:
            print "ERROR: incompatible binning of", h1.GetName(), "and", h2.GetName()
            return -1
        if xmin > xmax:
            xmin = 1
            xmax = h1.GetNbinsX()
        if ymin > ymax:
            ymin = 1
            ymax = h1.GetNbinsY()
        nDiffBins = 0
        for xb1 in range(xmin, xmax+1):
            for yb1 in range(ymin, ymax+1):
                if yb1 != xb1: continue
                cx = h1.GetXaxis().GetBinCenter(xb1)
                xb2 = h2.GetXaxis().FindBin(cx)
                cy = h1.GetYaxis().GetBinCenter(yb1)
                yb2 = h2.GetYaxis().FindBin(cy)
                cont1 = h1.GetBinContent(xb1, yb1)
                cont2 = h2.GetBinContent(xb2, yb2)
                denom = cont1
                if denom == 0.: denom = cont2
                if denom == 0.: continue
                if not self.isZero((cont1 - cont2) / denom, epsilon):
                    nDiffBins += 1
                    #print cx, cont1, cont2
        return nDiffBins
    
    def change2DHistoRange(self, histo, xmin, xmax, ymin, ymax):
        # Returns a histogram whose binning starts at xmin (ymin)
        #   and ends at xmax (ymax).
        # xmin, ymin and xmax, ymax must be some bin limits of the histogram histo!
        # Contents and errors of all the bins between xmin and xmax are 
        #   copied from histo to the newHisto.
        bin1x = histo.GetXaxis().FindBin(xmin + 1.)
        bin2x = histo.GetXaxis().FindBin(xmax - 1.)
        newNbinsX = bin2x-bin1x+1
        newBinsX = []
        for ib in range(bin1x, bin2x + 2):
            newBinsX.append(histo.GetXaxis().GetBinLowEdge(ib))
        bin1y = histo.GetYaxis().FindBin(ymin + 1.)
        bin2y = histo.GetYaxis().FindBin(ymax - 1.)
        newNbinsY = bin2y-bin1y+1
        newBinsY = []
        for ib in range(bin1y, bin2y + 2):
            newBinsY.append(histo.GetYaxis().GetBinLowEdge(ib))
        newHisto = TH2D(histo.GetName(), histo.GetTitle()
                        , newNbinsX, array("d",newBinsX), newNbinsY, array("d",newBinsY))
        for ibx in range(bin1x, bin2x + 1):
            for iby in range(bin1y, bin2y + 1):
                newIBx = ibx - bin1x + 1
                newIBy = iby - bin1y + 1
                newHisto.SetBinContent(newIBx, newIBy, histo.GetBinContent(ibx, iby))
                newHisto.SetBinError(newIBx, newIBy, histo.GetBinError(ibx, iby))
        return newHisto
    
    def setBinContentBs2D(self, bs, xBin, yBin, cont):
        nrep = bs.GetNReplica()
        for ir in range(nrep):
            bs.GetReplica(ir).SetBinContent(xBin, yBin, cont)
        return
    
    def setBinErrorBs2D(self, bs, xBin, yBin, err):
        nrep = bs.GetNReplica()
        for ir in range(nrep):
            bs.GetReplica(ir).SetBinError(xBin, yBin, err)
        return
    
    def setZero2D(self, histo):
        for ibx in range(histo.GetNbinsX() + 2):
            for iby in range(histo.GetNbinsY() + 2):
                histo.SetBinContent(ibx, iby, 0)
                histo.SetBinError(ibx, iby, 0)
        return
    
    def calculateRatioFromBs2D_asymErrors(self, bs1, bs2):
        if 0 > self.checkCompatibility(bs1.GetNominal().GetXaxis()
                                       , bs2.GetNominal().GetXaxis()):
            print "ERROR: incompatible x-axis binning"
            return
        if 0 > self.checkCompatibility(bs1.GetNominal().GetYaxis()
                                       , bs2.GetNominal().GetYaxis()):
            print "ERROR: incompatible y-axis binning"
            return
        ratioBs = ROOT.TH2DBootstrap(bs1)
        ratioBs.Divide(bs2)
        ratio = ratioBs.GetNominal().Clone("ratio")
        errUp = ratio.Clone("errUp")
        errDown = ratio.Clone("errDown")
        self.setZero2D(errUp)
        self.setZero2D(errDown)
        for ibx in range(1, ratio.GetNbinsX() + 1):
            for iby in range(1, ratio.GetNbinsY() + 1):
                eu2 = 0.
                ed2 = 0.
                mean = ratio.GetBinContent(ibx, iby)
                counterUp = 0.
                counterDown = 0.
                for ir in range(ratioBs.GetNReplica()):
                    diff = ratioBs.GetReplica(ir).GetBinContent(ibx, iby) - mean
                    if diff >= 0.:
                        eu2 += diff * diff
                        counterUp += 1.
                    if diff <= 0.:
                        ed2 += diff * diff
                        counterDown += 1.
                    if counterUp != 0.:
                        errUp.SetBinContent(ibx, iby, TMath.Sqrt(eu2 / counterUp))
                    else:
                        errUp.SetBinContent(ibx, iby, 0.)
                    if counterDown != 0.:
                        errDown.SetBinContent(ibx, iby, TMath.Sqrt(ed2 / counterDown))
                    else:
                        errDown.SetBinContent(ibx, iby, 0.)
        return [ratio, errUp, errDown]
    
    def integral2D(self, histo):
        cont = 0.
        for ibx in range(1, histo.GetNbinsX() + 1):
            for iby in range(1, histo.GetNbinsY() + 1):
                cont += histo.GetBinContent(ibx, iby)
        return cont
    
    def bsIntegral2D(self, bs):
        name = "{0}_integral".format(bs.GetName())
        bsInt = ROOT.TH1DBootstrap(name, name, 1, 0., 1., bs.GetNReplica())
        # Integrate the nominal histogram
        integral = self.integral2D(bs.GetNominal())
        bsInt.GetNominal().SetBinContent(1, integral)
        # Integrate the replicas one by one
        for ir in range(bs.GetNReplica()):
            integral = self.integral2D(bs.GetReplica(ir))
            bsInt.GetReplica(ir).SetBinContent(1, integral)
        return bsInt
      



