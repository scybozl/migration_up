# Written by Vojtech Pleskot (vojtech.pleskot@cern.ch)
#    based on idea and code of Daniel Scheirich.

from plotting.__init__ import *
from plotting.TH1_helpers import TH1_helper
import ROOT
import math
import itertools


#############################################
## Helper class to allow list to have attributes
#############################################

class CustomList(list):
    pass

class CustomDict(dict):
    pass

#############################################
## The main class
#############################################

class layout_helper(TH1_helper):
    # Must be provided by the user
    # ----------------------------
    pad = None
    plots = None
    # ----------------------------
    # Optional parameters
    # -------------------
    xMin = None # minimum of the x-axis; set according to plots[0] if None
    xMax = None # maximum of the x-axis; set according to plots[0] if None
    yMin = None # only set if need fixed y-axis minimum
    yMax = None # only set if need fixed y-axis maximum
    # -------------------
    # Must be set for the class to work
    # ---------------------------------
    entryHeight = None # recomm.: 0.07 (in NDC)
    topLeftTextPosX = None # recomm.: 0.2 (in NDC)
    topRightTextPosX = None # recomm.: 0.92 (in NDC)
    topTextPosY = None # recomm.: 0.9 (in NDC)
    bottomLeftTextPosX = None # recomm.: to be the same as topLeftTextPosX
    bottomRightTextPosX = None # recomm.: to be the same as topRightTextPosX
    bottomTextPosY = None # recomm.: 0.2 (in NDC)
    legendNCol = None # recomm.: 1
    considerUncertainties = None # when checking overlap between text and plots
    textPlotsDist = None # recomm.: 0.04 (in NDC; fractional minimal distance between plots and text)
                         # it is recommended to set it to slightly different number (e.g. 0.0499) than yMinOffset and yMaxOffset
                         # to avoid potential bad behaviour in these "edge" cases.
    yMinOffset = None # recomm.: 0.05 (units relative to axis range; get lower value than is minimum of a plot from plots)
    yMaxOffset = None # recomm.: 0.05 (units relative to axis range; get higher value than is maximum of a plot from plots)
                      # yMinOffset (yMaxOffset) is only considered if yMin (yMax) is None.
    verbose = None # 0 = no messages; 1 = summary and warnings; 2 = infos
    ignoreHorizontalBoxOverlaps = None # Consider layouts with overlapping text boxes as valid
    putTextAtTheTop = None # Use layouts with text at the top of the pad.
    putTextAtTheBottom = None # Use layouts with text at the bottom of the pad.
    letAtlasLabelFloat = None # Treat the atlas label as other objects - don't constrain its position.
    placePredefinedPanels = None # Switch to True only if you defined panels yourself via add[Legend, Text]ToPredefinedPanel() methods.
                                 # ATLAS label is set with the addTextToPredefinedPanel() method since it makes no sense to make
                                 # difference between label box and other text boxes.
                                 # Note: predefinition of panels goes to some extent against the idea of this plotting tool.
                                 #       Therefore, this option is not super-optimized and can give pathological output
                                 #       if the input is also pathological, i.e. too much text in a panel.
                                 #       Although the functionality should be OK in most "normal" cases, bear in mind
                                 #       that you use this option on your own risk.
    # ---------------------------------
    # Internal attributes; must not be touched by user
    # ------------------------------------------------
    yMinDyn = None
    yMaxDyn = None
    tBox = None
    bBox = None
    textStorage = None # storage of labels such that they don't get deleted
    frame = None # TH1D drawn to have axes in a pad
    atlasLabel = None # CustomList with labels like "ATLAS", "13 TeV" etc.
    legends = None # list of CustomLists with legend texts
    texts = None # list of CustomLists with any additional text
    nLayoutsTried = None
    nLayoutsWithNonSuitedPanel = None
    nLayoutsWithOverlapedBoxes = None
    outAtlasLab = None
    outListLeg = None
    outDicLeg = None
    outListTexts = None
    outDicTexts = None
    predefinedPanels = None # dictionary with predefined panels; only use if self.placePredefinedPanels == True
    
    def __init__(self):
        return

    #############################################
    ## Methods for user input definition
    #############################################

    def setPad(self, pad):
        self.pad = pad
        if self.pad is None: return
        self.pad.cd()
        return

    def setPlots(self, plots):
        if plots is None:
            self.plots = None
            return
        if type(plots) is not list or len(plots) == 0:
            print "In setPlots(): no plot in plots!"
            raise SystemExit()
        self.plots = plots
        return

    def setXMin(self, xMin):
        self.xMin = xMin
        return

    def setXMax(self, xMax):
        self.xMax = xMax
        return

    def setYMin(self, yMin):
        self.yMin = yMin
        return

    def setYMax(self, yMax):
        self.yMax = yMax
        return

    def setEntryHeight(self, entryHeight):
        if self.pad is None:
            print "in layout_helper.setEntryHeight():"
            print "    cannot set self.entryHeight: self.pad missing!"
            raise SystemExit()
        self.entryHeight = entryHeight * self.universalTextScaleConstant()
        return

    def setTopLeftTextPosX(self, topLeftTextPosX):
        self.topLeftTextPosX = topLeftTextPosX
        return

    def setTopRightTextPosX(self, topRightTextPosX):
        self.topRightTextPosX = topRightTextPosX
        return

    def setTopTextPosY(self, topTextPosY):
        self.topTextPosY = topTextPosY
        return

    def setBottomLeftTextPosX(self, bottomLeftTextPosX):
        self.bottomLeftTextPosX = bottomLeftTextPosX
        return

    def setBottomRightTextPosX(self, bottomRightTextPosX):
        self.bottomRightTextPosX = bottomRightTextPosX
        return

    def setBottomTextPosY(self, bottomTextPosY):
        self.bottomTextPosY = bottomTextPosY
        return

    def setLegendNCol(self, legendNCol):
        self.legendNCol = legendNCol
        return
    
    def setConsiderUncertainties(self, considerUncertainties):
        self.considerUncertainties = considerUncertainties
        return
    
    def setTextPlotsDist(self, textPlotsDist):
        self.textPlotsDist = textPlotsDist
        return
    
    def setYMinOffset(self, yMinOffset):
        self.yMinOffset = yMinOffset
        return
    
    def setYMaxOffset(self, yMaxOffset):
        self.yMaxOffset = yMaxOffset
        return
    
    def setVerbose(self, verbose):
        self.verbose = verbose
        return
    
    def setIgnoreHorizontalBoxOverlaps(self, ignoreHorizontalBoxOverlaps):
        self.ignoreHorizontalBoxOverlaps = ignoreHorizontalBoxOverlaps
        return
    
    def setPutTextAtTheTop(self, putTextAtTheTop):
        self.putTextAtTheTop = putTextAtTheTop
        return
    
    def setPutTextAtTheBottom(self, putTextAtTheBottom):
        self.putTextAtTheBottom = putTextAtTheBottom
        return
    
    def setLetAtlasLabelFloat(self, letAtlasLabelFloat):
        self.letAtlasLabelFloat = letAtlasLabelFloat
        return
    
    def setPlacePredefinedPanels(self, placePredefinedPanels):
        self.placePredefinedPanels = placePredefinedPanels
        return
    
    def setNLayoutsTried(self, nLayoutsTried):
        self.nLayoutsTried = nLayoutsTried
        return
    
    def setNLayoutsWithNonSuitedPanel(self, nLayoutsWithNonSuitedPanel):
        self.nLayoutsWithNonSuitedPanel = nLayoutsWithNonSuitedPanel
        return
    
    def setNLayoutsWithOverlapedBoxes(self, nLayoutsWithOverlapedBoxes):
        self.nLayoutsWithOverlapedBoxes = nLayoutsWithOverlapedBoxes
        return
    
    def resetAttributesToNone(self):
        self.pad = None
        self.plots = None
        self.xMin = None
        self.xMax = None
        self.yMin = None
        self.yMax = None
        self.entryHeight = None
        self.topLeftTextPosX = None
        self.topRightTextPosX = None
        self.topTextPosY = None
        self.bottomLeftTextPosX = None
        self.bottomRightTextPosX = None
        self.bottomTextPosY = None
        self.legendNCol = None
        self.considerUncertainties = None
        self.textPlotsDist = None
        self.yMinOffset = None
        self.yMaxOffset = None
        self.verbose = None
        self.ignoreHorizontalBoxOverlaps = None
        self.putTextAtTheTop = None
        self.putTextAtTheBottom = None
        self.letAtlasLabelFloat = None
        self.placePredefinedPanels = None
        self.yMinDyn = None
        self.yMaxDyn = None
        self.tBox = None
        self.bBox = None
        self.frame = None
        self.atlasLabel = None
        self.legends = None
        self.texts = None
        self.nLayoutsTried = None
        self.nLayoutsWithNonSuitedPanel = None
        self.nLayoutsWithOverlapedBoxes = None
        self.outAtlasLab = None
        self.outListLeg = None
        self.outDicLeg = None
        self.outListTexts = None
        self.outDicTexts = None
        self.predefinedPanels = None
        return
    
    def resetAttributes(self, pad = None, plots = None
                        , xMin = None, xMax = None
                        , yMin = None, yMax = None
                        , entryHeight = 0.065
                        , topLeftTextPosX = 0.2, topRightTextPosX = 0.92, topTextPosY = 0.9
                        , bottomLeftTextPosX = 0.2, bottomRightTextPosX = 0.92, bottomTextPosY = 0.06
                        , legendNCol = 1
                        , considerUncertainties = False, textPlotsDist = 0.05
                        , yMinOffset = 0, yMaxOffset = 0, verbose = 0
                        , ignoreHorizontalBoxOverlaps = False
                        , putTextAtTheTop = True, putTextAtTheBottom = False
                        , letAtlasLabelFloat = False, placePredefinedPanels = False
                        , atlasLabel = None, legends = None, texts = None):
        # Set all the variables to their initial values according to
        #    the user's input
        self.resetAttributesToNone()
        self.verbose = verbose
        self.ignoreHorizontalBoxOverlaps = ignoreHorizontalBoxOverlaps
        self.putTextAtTheTop = putTextAtTheTop
        self.putTextAtTheBottom = putTextAtTheBottom
        self.letAtlasLabelFloat = letAtlasLabelFloat
        self.placePredefinedPanels = placePredefinedPanels
        self.setPad(pad)
        self.setPlots(plots)
        # Set entryHeight, topLeftTextPosX, topRightTextPosX, topTextPosY,
        #    bottomLeftTextPosX, bottomRightTextPosX, bottomTextPosY, legendNCol,
        #    considerUncertainties, textPlotsDist, yMinOffset, yMaxOffset
        self.setEntryHeight(entryHeight)
        self.topLeftTextPosX = topLeftTextPosX
        self.topRightTextPosX = topRightTextPosX
        self.topTextPosY = topTextPosY
        self.bottomLeftTextPosX = bottomLeftTextPosX
        self.bottomRightTextPosX = bottomRightTextPosX
        self.bottomTextPosY = bottomTextPosY
        self.legendNCol = legendNCol
        self.considerUncertainties = considerUncertainties
        self.textPlotsDist = textPlotsDist
        self.yMinOffset = yMinOffset
        self.yMaxOffset = yMaxOffset
        # Check that all objects in plots are either TH1, TGraph,
        #    THStack, TF1 or TLine.
        self.checkInputPlots()
        # Set xMin and xMax
        self.xMin = xMin
        self.xMax = xMax
        xMax, xMin = self.getXMaxAndMin()
        if self.xMin is None:
            self.xMin = xMin
        if self.xMax is None:
            self.xMax = xMax
        # Check compatibility of xMin with logarithmic x-axis
        if self.pad.GetLogx() and self.xMin <= 0:
            print "ERROR: in resetAttributes():"
            print "    x-axis is logarithmic and xMin <= 0!"
            raise SystemExit()
        # Check that plots are compatible with logarithmic y-axis (if it was requested)
        self.checkInputPlots(self.xMin, self.xMax)
        # Set yMin and yMax
        self.yMin = yMin
        self.yMax = yMax
        # Check compatibility of yMin with logarithmic y-axis
        if self.pad.GetLogy() and self.yMin is not None and self.yMin <= 0:
            print "ERROR: in resetAttributes():"
            print "    y-axis is logarithmic and yMin <= 0!"
            raise SystemExit()
        # Set yMinDyn, yMaxDyn, tBox, bBox
        if self.yMin is not None:
            self.yMinDyn = self.yMin
        else:
            self.yMinDyn = self.getMinimum(self.xMin, self.xMax)
        if self.yMax is not None:
            self.yMaxDyn = self.yMax
        else:
            self.yMaxDyn = self.getMaximum(self.xMin, self.xMax)
        self.yMaxDyn, self.yMinDyn = self.offsetMaxAndMin()
        self.tBox = None
        self.bBox = None
        # Set frame
        self.frame = TH1D("frame", "frame", 1, self.xMin, self.xMax)
        self.frame.GetXaxis().SetNoExponent()
        self.frame.SetMinimum(self.yMinDyn)
        self.frame.SetMaximum(self.yMaxDyn)
        self.frame.SetLineColor(0)
        self.frame.Draw()
        if self.textStorage is None:
            self.textStorage = []
        self.textStorage.append(self.frame)
        self.pad.Modified()
        self.pad.Update()
        self.atlasLabel = atlasLabel
        if legends is None:
            self.legends = []
        if texts is None:
            self.texts = []
        self.nLayoutsTried = None
        self.nLayoutsWithNonSuitedPanel = None
        self.nLayoutsWithOverlapedBoxes = None
        self.outAtlasLab = None
        self.outListLeg = None
        self.outDicLeg = None
        self.outListTexts = None
        self.outDicTexts = None
        self.predefinedPanels = None
        return

    def clearStorage(self):
        self.textStorage = None
        return
    
    def addLabel(self, labelList, outDic = None):
        # Maximum one label can be added!
        # The output coordinates will be retrievable with labelCoordinates().
        self.checkListOfStr(labelList, "layout_helper.addLabel()")
        if outDic is not None and not isinstance(outDic, dict):
            print "In layout_helper.addLabel(): parameter outDic must be either None or dict!"
            print "    This type provided:", type(outDic)
            raise SystemExit()
        if self.atlasLabel is not None:
            print "self.atlasLabel set already!"
            print "Failed to add the label"
            print labelList
            raise SystemExit()
        cl = CustomList(labelList)
        cl.kind = "label"
        self.atlasLabel = cl
        self.outAtlasLab = outDic
        if self.outAtlasLab is None:
            self.outAtlasLab = {}
        return

    def addLegend(self, entries, outDic = None):
        # Add legend defined by entries (list of strings) to the internal
        #    list of legends.
        # outDic can be None, dict or str:
        #    None ... output coordinates for given text box will be retrievable with
        #             legendCoordinates(i), where i = 0, 1,... reflects the order
        #             in which text boxes were added.
        #    dict ... output coordinates will be stored in this user-provided dictionary.
        #    str  ... output coordinates will be retrievable with
        #             legendCoordinates(outDic).
        self.checkListOfStr(entries, "layout_helper.addLegend()")
        self.checkOutDic(outDic, "layout_helper.addLegend()")
        if self.legends is None:
            self.legends = []
        cl = CustomList(entries)
        cl.kind = "legend"
        cl.nCol = 1
        self.legends.append(cl)
        # self.outListLeg
        if self.outListLeg is None:
            self.outListLeg = []
        if isinstance(outDic, dict):
            self.outListLeg.append(outDic)
        else:
            self.outListLeg.append({})
        # self.outDicLeg
        if isinstance(outDic, str):
            if self.outDicLeg is None:
                self.outDicLeg = {}
            if outDic in self.outDicTexts:
                print "In layout_helper.addLegend(): key \"{0}\"".format(outDic)
                print "    exists already; you must not use this key anymore!"
                raise SystemExit()
            self.outDicLeg[outDic] = self.outListLeg[len(self.outListLeg) - 1]
        return
    
    def addText(self, entries, outDic = None):
        # Add text box defined by entries (list of strings) to the internal
        #    list of text boxes.
        # outDic can be None, dict or str:
        #    None ... output coordinates for given text box will be retrievable with
        #             textCoordinates(i), where i = 0, 1,... reflects the order
        #             in which text boxes were added.
        #    dict ... output coordinates will be stored in this user-provided dictionary.
        #    str  ... output coordinates will be retrievable with
        #             textCoordinates(outDic).
        self.checkListOfStr(entries, "layout_helper.addText()")
        self.checkOutDic(outDic, "layout_helper.addText()")
        if self.texts is None:
            self.texts = []
        cl = CustomList(entries)
        cl.kind = "text"
        self.texts.append(cl)
        # self.outListTexts
        if self.outListTexts is None:
            self.outListTexts = []
        if isinstance(outDic, dict):
            self.outListTexts.append(outDic)
        else:
            self.outListTexts.append({})
        # self.outDicTexts
        if isinstance(outDic, str):
            if self.outDicTexts is None:
                self.outDicTexts = {}
            if outDic in self.outDicTexts:
                print "In layout_helper.addText(): key \"{0}\"".format(outDic)
                print "    exists already; you must not use this key anymore!"
                raise SystemExit()
            self.outDicTexts[outDic] = self.outListTexts[len(self.outListTexts) - 1]
        return
    
    def addLegendToPredefinedPanel(self, entries, nCol, pos, outDic = None):
        # Add legend defined by entries (list of strings) to the panel
        #    at the position pos ("TL", "TR", "BL" or "BR").
        # Use this method only if you set self.placePredefinedPanels to True;
        #    otherwise, there will be no effect.
        # For outDic, see addLegend() method.
        self.checkListOfStr(entries, "layout_helper.addLegendToPredefinedPanel()")
        if not isinstance(nCol, int) or nCol < 1:
            print "In layout_helper.addLegendToPredefinedPanel(): parameter nCol must be an integer >= 1!"
            raise SystemExit()
        if pos not in ["TL", "TR", "BL", "BR"]:
            print "In layout_helper.addLegendToPredefinedPanel(): parameter pos must be"
            print "    one of the following str: \"TL\", \"TR\", \"BL\", \"BR\"!"
            print "    Provided value: pos == ", pos
            raise SystemExit()
        self.checkOutDic(outDic, "layout_helper.addLegendToPredefinedPanel()")
        if self.predefinedPanels is None:
            self.predefinedPanels = {}
        for key in ["TL", "TR", "BL", "BR"]:
            if not key in self.predefinedPanels:
                self.predefinedPanels[key] = []
        cl = CustomList(entries)
        cl.kind = "legend"
        cl.nCol = nCol
        self.predefinedPanels[pos].append(cl)
        # self.legends
        if self.legends is None:
            self.legends = []
        self.legends.append(cl)
        # self.outListLeg
        if self.outListLeg is None:
            self.outListLeg = []
        if isinstance(outDic, dict):
            self.outListLeg.append(outDic)
        else:
            self.outListLeg.append({})
        # self.outDicLeg
        if isinstance(outDic, str):
            if self.outDicLeg is None:
                self.outDicLeg = {}
            if outDic in self.outDicLeg:
                print "In layout_helper.addLegendToPredefinedPanel(): key \"{0}\"".format(outDic)
                print "    exists already; you must not use this key anymore!"
                raise SystemExit()
            self.outDicLeg[outDic] = self.outListLeg[len(self.outListLeg) - 1]
        return
        
    def addTextToPredefinedPanel(self, entries, pos, outDic = None):
        # Add text box defined by entries (list of strings) to the panel
        #    at the position pos ("TL", "TR", "BL" or "BR").
        # Use this method only if you set self.placePredefinedPanels to True;
        #    otherwise, there will be no effect.
        # For outDic, see addText() method.
        self.checkListOfStr(entries, "layout_helper.addTextToPredefinedPanel()")
        if pos not in ["TL", "TR", "BL", "BR"]:
            print "In layout_helper.addTextToPredefinedPanel(): parameter pos must be"
            print "    one of the following str: \"TL\", \"TR\", \"BL\", \"BR\"!"
            print "    Provided value: pos == ", pos
            raise SystemExit()
        self.checkOutDic(outDic, "layout_helper.addTextToPredefinedPanel()")
        if self.predefinedPanels is None:
            self.predefinedPanels = {}
        for key in ["TL", "TR", "BL", "BR"]:
            if not key in self.predefinedPanels:
                self.predefinedPanels[key] = []
        cl = CustomList(entries)
        cl.kind = "text"
        self.predefinedPanels[pos].append(cl)
        # self.texts
        if self.texts is None:
            self.texts = []
        self.texts.append(cl)
        # self.outListTexts
        if self.outListTexts is None:
            self.outListTexts = []
        if isinstance(outDic, dict):
            self.outListTexts.append(outDic)
        else:
            self.outListTexts.append({})
        # self.outDicTexts
        if isinstance(outDic, str):
            if self.outDicTexts is None:
                self.outDicTexts = {}
            if outDic in self.outDicTexts:
                print "In layout_helper.addTextToPredefinedPanel(): key \"{0}\"".format(outDic)
                print "    exists already; you must not use this key anymore!"
                raise SystemExit()
            self.outDicTexts[outDic] = self.outListTexts[len(self.outListTexts) - 1]
        return
        
    
    #############################################
    ## Methods returning the output of the class
    #############################################

    def getFrame(self):
        return self.frame
    
    def labelCoordinates(self):
        return self.outAtlasLab
    
    def legendCoordinates(self, identifier = None):
        # identifier is either None, integer or str.
        #    None ... return the whole list of dictionaries ordered according
        #             to the order in which legends were added.
        #    integer ... return dictionary of the i-th added legend (i = 0, 1...).
        #    str ... return dictionary related to the string provided in addLegend.
        if identifier is None:
            return self.outListLeg
        if isinstance(identifier, int):
            if identifier >= len(self.outListLeg):
                print "In layout_helper.legendCoordinates(): provided identifier is integer"
                print "    identifier ==", identifier, "but only", len(self.outListLeg)
                print "    legends were added; identifier must be 0, 1, ...,", len(self.outListLeg) - 1
                print "    Returning None, expect crash soon!"
                return None
            return self.outListLeg[identifier]
        if isinstance(identifier, str):
            if not identifier in self.outDicLeg:
                print "In layout_helper.legendCoordinates(): provided identifier is str"
                print "    identifier ==", identifier, "but entry with this name"
                print "    does not exist!"
                print "    Returning None, expect crash soon!"
                return None
            return self.outDicLeg[identifier]
        print "In layout_helper.legendCoordinates(): argument identifier must be None, int or str!"
        print "    type of identifier:", type(identifier)
        print "    Returning None, expect crash soon!"
        return None
    
    def textCoordinates(self, identifier = None):
        # identifier is either None, integer or str.
        #    None ... return the whole list of dictionaries ordered according
        #             to the order in which text boxes were added.
        #    integer ... return dictionary of the i-th added text box (i = 0, 1...).
        #    str ... return dictionary related to the string provided in addText.
        if identifier is None:
            return self.outListTexts
        if isinstance(identifier, int):
            if identifier >= len(self.outListTexts):
                print "In layout_helper.textCoordinates(): provided identifier is integer"
                print "    identifier ==", identifier, "but only", len(self.outListTexts)
                print "    text boxes were added; identifier must be 0, 1, ...,", len(self.outListTexts) - 1
                print "    Returning None, expect crash soon!"
                return None
            return self.outListTexts[identifier]
        if isinstance(identifier, str):
            if not identifier in self.outDicTexts:
                print "In layout_helper.textCoordinates(): provided identifier is str"
                print "    identifier ==", identifier, "but entry with this name"
                print "    does not exist!"
                print "    Returning None, expect crash soon!"
                return None
            return self.outDicTexts[identifier]
        print "In layout_helper.textCoordinates(): argument identifier must be None, int or str!"
        print "    type of identifier:", type(identifier)
        print "    Returning None, expect crash soon!"
        return None
    
    #############################################
    ## Methods for handling text in plots
    #############################################

    def placeAllTextToPad(self):
        if self.placePredefinedPanels:
            if self.yMin is not None and self.yMax is not None:
                return self.placePredefinedPanelsToPad_yAxRangeFixed()
            return self.placePredefinedPanelsToPad()
        objects = []
        if self.atlasLabel is not None and self.letAtlasLabelFloat:
            objects.append(self.atlasLabel)
        for b in self.legends:
            objects.append(b)
        for b in self.texts:
            objects.append(b)
        NObj = len(objects)
        initialYMax = self.yMaxDyn
        initialYMin = self.yMinDyn
        TLPanel = []
        TRPanel = []
        # Just set some initial value for the final yMax candidate
        #if self.atlasLabel is not None:
        #    TLPanel.append(self.atlasLabel)
        #for b in objects:
        #    TLPanel.append(b)
        #test = self.placeTopLeftPanelToPad(TLPanel)
        #if not test:
        yMaxCandidate = float("inf")
        yMinCandidate = float("-inf")
        if self.pad.GetLogy():
            yMinCandidate = self.yMinDyn / 1.e30
        ###yMaxCandidate = 1 # for the case self.yMaxDyn == 0
        ###if self.yMaxDyn > 0:
        ###    yMaxCandidate = self.yMaxDyn * 1.e30
        ###elif self.yMaxDyn < 0:
        ###    yMaxCandidate = abs(self.yMaxDyn) * 10
        ###yMinCandidate = -1.e30
        ###sign = math.copysign(1, self.yMinDyn)
        ###if sign < 0:
        ###    yMinCandidate = abs(self.yMinDyn) * 1.e30 * sign
        ###elif sign > 0 and self.pad.GetLogy():
        ###    yMinCandidate = self.yMinDyn / 1.e30
        if self.putTextAtTheTop and not self.putTextAtTheBottom:
            yMinCandidate = self.yMinDyn
        if self.putTextAtTheBottom and not self.putTextAtTheTop:
            yMaxCandidate = self.yMaxDyn
        if self.yMax is not None:
            yMaxCandidate = self.yMaxDyn
        if self.yMin is not None:
            yMinCandidate = self.yMinDyn
        # Set some control variables
        self.nLayoutsTried = 0
        self.nLayoutsWithNonSuitedPanel = 0
        self.nLayoutsWithOverlapedBoxes = 0
        # Prepare lists with all possible combinations
        patternsNObj = []
        for N in range(NObj + 1):
            if self.putTextAtTheTop and not self.putTextAtTheBottom:
                patternsNObj.append([NObj - N, N, 0, 0])
            if self.putTextAtTheBottom and not self.putTextAtTheTop:
                patternsNObj.append([0, 0, NObj - N, N])
            if self.putTextAtTheTop and self.putTextAtTheBottom:
                # N_BR = N
                for N_BL in range(NObj + 1 - N):
                    for N_TR in range(NObj + 1 - N - N_BL):
                            patternsNObj.append([NObj - N_TR - N_BL - N, N_TR, N_BL, N])
        patternsLegNCol = []
        if len(self.legends) == 0:
            patternsLegNCol.append(None)
        else:
            nc = self.legendNCol
            nl = len(self.legends)
            for i in range(pow(nc, nl)):
                num = []
                newi = i
                for il in range(nl):
                    mod = newi % pow(nc, il + 1)
                    pos = mod / pow(nc, il)
                    num.append(pos + 1)
                    newi -= mod
                patternsLegNCol.append(num)
        patternsAtlasLPos = ["L", "R"]
        if self.atlasLabel is None or self.letAtlasLabelFloat:
            patternsAtlasLPos = [None]
        # Start trying all possibilities
        for pALPos in patternsAtlasLPos:
            for pLegNCol in patternsLegNCol:
                for pNObj in patternsNObj:
                    for pObjects in itertools.permutations(objects):
                        if not self.tryLayout(initialYMax, initialYMin
                                              , pALPos, pLegNCol, pNObj, pObjects):
                            continue
                        canYRange = self.toLog(yMaxCandidate) - self.toLog(yMinCandidate)
                        currYRange = self.toLog(self.yMaxDyn) - self.toLog(self.yMinDyn)
                        if self.verbose > 1:
                            print "INFO: In placeAllTextToPad(): printout after a layout passed tryLayout():"
                            print "    yMaxCandidate", yMaxCandidate, "self.yMaxDyn", self.yMaxDyn, "yMinCandidate", yMinCandidate, "self.yMinDyn", self.yMinDyn
                        if currYRange < canYRange or (self.isClose(currYRange, canYRange, 1.e-9) and not self.someLayoutPassed()):
                            yMaxCandidate = self.yMaxDyn
                            yMinCandidate = self.yMinDyn
                            if self.atlasLabel is not None:
                                self.atlasLabel.coor = self.atlasLabel.tmpCoor.copy()
                            for obj in pObjects:
                                obj.coor = obj.tmpCoor.copy()
                            for leg in self.legends:
                                leg.nColumns = leg.nCol
        if self.verbose:
            print "In placeAllTextToPad(), summary:"
            print "    {0} layouts tried".format(self.nLayoutsTried)
            nSucc = self.nLayoutsTried - self.nLayoutsWithNonSuitedPanel
            if not self.ignoreHorizontalBoxOverlaps:
                nSucc -= self.nLayoutsWithOverlapedBoxes
            print "    {0} layouts successfull".format(nSucc)
            print "    {0} layouts with non-suited panels".format(self.nLayoutsWithNonSuitedPanel)
            print "    {0} layouts with overlapping boxes".format(self.nLayoutsWithOverlapedBoxes)
        if self.nLayoutsWithNonSuitedPanel == self.nLayoutsTried:
            if self.verbose:
                print "All tried layouts failed!"
                print "    All panels are too height!"
            return False
        if self.nLayoutsWithNonSuitedPanel + self.nLayoutsWithOverlapedBoxes == self.nLayoutsTried:
            if self.verbose:
                print "All tried layouts failed!"
                print "    All layouts yield either a too height panel or"
                print "    overlapping boxes."
            if not self.ignoreHorizontalBoxOverlaps:
                return False
            else:
                if self.verbose:
                    print "Ignoring horizontal box overlaps."
        self.yMaxDyn = yMaxCandidate
        self.frame.SetMaximum(self.yMaxDyn)
        self.yMinDyn = yMinCandidate
        self.frame.SetMinimum(self.yMinDyn)
        self.pad.Modified()
        self.pad.Update()
        # Copy the coordinates to the output dictionaries.
        if self.atlasLabel is not None:
            self.copyOutputDictionary(self.atlasLabel.coor, self.outAtlasLab)
        for i in range(len(self.legends)):
            self.copyOutputDictionary(self.legends[i].coor, self.outListLeg[i])
        for i in range(len(self.texts)):
            self.copyOutputDictionary(self.texts[i].coor, self.outListTexts[i])
        return True

    def tryLayout(self, initialYMax, initialYMin, pALPos, pLegNCol, pNObj, pObjects):
        # ATTENTION: method changes self.yMaxDyn and 
        #    maximum of the "axes" histogram self.frame!!!
        # Layout defined by pALPos, pLegNCol, pNObj, pObjects:
        #    pALPos   ... either "L" or "R"
        #    pLegNCol ... list with number of columns for each legend
        #    pNObj    ... list with number of boxes for each panel
        #    pObjects ... list with tested permutation of entries
        self.tBox = None
        self.bBox = None
        self.yMaxDyn = initialYMax
        self.frame.SetMaximum(self.yMaxDyn)
        self.yMinDyn = initialYMin
        self.frame.SetMinimum(self.yMinDyn)
        self.pad.Modified()
        self.pad.Update()
        self.nLayoutsTried += 1
        if self.verbose and self.nLayoutsTried % 10 == 0:
            print "{0} layouts tried".format(self.nLayoutsTried)
        TLPanel = []
        TRPanel = []
        BLPanel = []
        BRPanel = []
        # Position of the ATLAS labels
        if pALPos is not None:
            if self.putTextAtTheTop:
                if pALPos == "L":
                    TLPanel.append(self.atlasLabel)
                if pALPos == "R":
                    TRPanel.append(self.atlasLabel)
            if self.putTextAtTheBottom and not self.putTextAtTheTop:
                if pALPos == "L":
                    BLPanel.append(self.atlasLabel)
                if pALPos == "R":
                    BRPanel.append(self.atlasLabel)
        # Numbers of legend columns
        if pLegNCol is not None:
            for il in range(len(self.legends)):
                self.legends[il].nCol = pLegNCol[il]
        # Boxes in panels
        N_TL = pNObj[0]
        N_TR = pNObj[1]
        N_BL = pNObj[2]
        N_BR = pNObj[3]
        for i in range(0, N_TL):
            TLPanel.append(pObjects[i])
        for i in range(N_TL, N_TL + N_TR):
            TRPanel.append(pObjects[i])
        for i in range(N_TL + N_TR, N_TL + N_TR + N_BL):
            BLPanel.append(pObjects[i])
        for i in range(N_TL + N_TR + N_BL, N_TL + N_TR + N_BL + N_BR):
            BRPanel.append(pObjects[i])
        # Place panels to the pad
        if self.verbose > 1:
            print "INFO: In tryLayout(): printing panels before placing them."
            print "TLPanel", TLPanel
            print "TRPanel", TRPanel
            print "BLPanel", BLPanel
            print "BRPanel", BRPanel
        if not self.placeTopPanelToPad(TLPanel, "L"):
            self.nLayoutsWithNonSuitedPanel += 1
            return False
        if not self.placeTopPanelToPad(TRPanel, "R"):
            self.nLayoutsWithNonSuitedPanel += 1
            return False
        if not self.placeBottomPanelToPad(BLPanel, "L"):
            self.nLayoutsWithNonSuitedPanel += 1
            return False
        if not self.placeBottomPanelToPad(BRPanel, "R"):
            self.nLayoutsWithNonSuitedPanel += 1
            return False
        if self.overlap(TLPanel, TRPanel):
            self.nLayoutsWithOverlapedBoxes += 1
            if not self.ignoreHorizontalBoxOverlaps:
                return False
        if self.overlap(BLPanel, BRPanel):
            self.nLayoutsWithOverlapedBoxes += 1
            if not self.ignoreHorizontalBoxOverlaps:
                return False
        return True
        
    def placeTopPanelToPad_backup(self, panel, isLeftPanel):
        # Panel is a list of CustomLists;
        #    the panel is to be plotted at one corner of the frame
        # ATTENTION: method changes self.yMaxDyn!!!
        if len(panel) == 0:
            return True
        # Check if there is a legend in the panel
        legWidth = self.maxLegendWidthInPanel(panel)
        for ib in range(len(panel)):
            x = self.topLeftTextPosX + legWidth * 0.0333
            if not isLeftPanel:
                x = self.topRightTextPosX - self.getPanelWidth(panel) + legWidth * 0.0333
            if panel[ib].kind == "legend":
                x = self.topLeftTextPosX
                if not isLeftPanel:
                    x = self.topRightTextPosX - self.getPanelWidth(panel)
            prevY2 = self.topTextPosY
            if ib > 0:
                prevY2 = panel[ib - 1].tmpCoor["y2"]
            if not self.placeBoxToTopPanel_backup(panel[ib], x, prevY2):
                return False
        return True

    def placeBottomPanelToPad_backup(self, panel, isLeftPanel):
        # Panel is a list of CustomLists;
        #    the panel is to be plotted at one corner of the frame
        # ATTENTION: method changes self.yMinDyn!!!
        if len(panel) == 0:
            return True
        # Check if there is a legend in the panel
        legWidth = self.maxLegendWidthInPanel(panel)
        for ib in range(len(panel)):
            x = self.bottomLeftTextPosX + legWidth * 0.0333
            if not isLeftPanel:
                x = self.bottomRightTextPosX - self.getPanelWidth(panel) + legWidth * 0.0333
            if panel[ib].kind == "legend":
                x = self.bottomLeftTextPosX
                if not isLeftPanel:
                    x = self.bottomRightTextPosX - self.getPanelWidth(panel)
            prevY1 = self.bottomTextPosY
            if ib > 0:
                prevY1 = panel[ib - 1].tmpCoor["y1"]
            if not self.placeBoxToBottomPanel_backup(panel[ib], x, prevY1):
                return False
        return True

    def placeTopPanelToPad(self, panel, hPos):
        # Panel is a CustomList of CustomLists;
        #    the panel is to be plotted at one corner of the frame
        # Parameter pos must be either "L" or "R".
        if len(panel) == 0:
            return True
        # Check if there is a legend in the panel
        legWidth = self.maxLegendWidthInPanel(panel)
        for ib in range(len(panel)):
            x = self.topLeftTextPosX + legWidth * 0.0333
            if hPos == "R":
                x = self.topRightTextPosX - self.getPanelWidth(panel) + legWidth * 0.0333
            if panel[ib].kind == "legend":
                x = self.topLeftTextPosX
                if hPos == "R":
                    x = self.topRightTextPosX - self.getPanelWidth(panel)
            prevY2 = self.topTextPosY
            if ib > 0:
                prevY2 = panel[ib - 1].tmpCoor["y2"]
            if not self.placeBoxToPanel(panel[ib], x, prevY2, "T"):
                return False
        return True

    def placeBottomPanelToPad(self, panel, hPos):
        # Panel is a list of CustomLists;
        #    the panel is to be plotted at one corner of the frame
        # Parameter pos must be either "L" or "R".
        if len(panel) == 0:
            return True
        # Check if there is a legend in the panel
        legWidth = self.maxLegendWidthInPanel(panel)
        for ib in range(len(panel)):
            x = self.bottomLeftTextPosX + legWidth * 0.0333
            if hPos == "R":
                x = self.bottomRightTextPosX - self.getPanelWidth(panel) + legWidth * 0.0333
            if panel[ib].kind == "legend":
                x = self.bottomLeftTextPosX
                if hPos == "R":
                    x = self.bottomRightTextPosX - self.getPanelWidth(panel)
            prevY1 = self.bottomTextPosY
            if ib > 0:
                prevY1 = panel[ib - 1].tmpCoor["y1"]
            if not self.placeBoxToPanel(panel[ib], x, prevY1, "B"):
                return False
        return True

    def placeBoxToTopPanel_backup(self, entries, origX, origY):
        # Place text into a panel.
        # The coordinates of the text are attached to entries
        #    as an attribute tmpCoor which is a directory.
        # ATTENTION: method changes self.yMaxDyn and 
        #    maximum of the "axes" histogram self.frame!!!
        box = self.getBoxSize(origX = origX, origY = origY
                                         , align = "left", entries = entries)
        if not self.updateMaximum(box):
            return False
        entries.tmpCoor = self.outputDictionary(box, entries, "left")
        return True

    def placeBoxToBottomPanel_backup(self, entries, origX, origY):
        # Place text into a panel.
        # The coordinates of the text are attached to entries
        #    as an attribute tmpCoor which is a directory.
        # ATTENTION: method changes self.yMinDyn and 
        #    minimum of the "axes" histogram self.frame!!!
        # The boxes are inserted from bottom to top.
        #    (origX, origY) is the top left corner of the last inserted box.
        height = self.getBoxHeight(entries)
        box = self.getBoxSize(origX = origX, origY = origY + height
                              , align = "left", entries = entries)
        if not self.updateMinimum(box):
            return False
        entries.tmpCoor = self.outputDictionary(box, entries, "left")
        return True

    def placeBoxToPanel(self, entries, x, y, vPos):
        # Place text into a panel.
        # The coordinates of the text are attached to entries
        #    as an attribute tmpCoor which is a directory.
        # ATTENTION: method changes self.yMinDyn and 
        #    minimum of the "axes" histogram self.frame!!!
        # The boxes are inserted from bottom to top.
        #    (x, y) is the top left corner of the last inserted box.
        height = 0
        if vPos == "B":
            height = self.getBoxHeight(entries)
        box = self.getBoxSize(origX = x, origY = y + height
                              , align = "left", entries = entries)
        box.vPos = vPos
        if not self.updateMaxMin(box):
            return False
        entries.tmpCoor = self.outputDictionary(box, entries, "left")
        return True

    def copyOutputDictionary(self, oldDic, newDic):
        if not isinstance(newDic, dict):
            print "In copyOutputDictionary(): argument dic is not of type dict;"
            print "    provided type:", type(newDic)
            raise SystemExit()
        newDic["x1"] = oldDic["x1"]
        newDic["y1"] = oldDic["y1"]
        newDic["x2"] = oldDic["x2"]
        newDic["y2"] = oldDic["y2"]
        if "nColumns" in oldDic:
            newDic["nColumns"] = oldDic["nColumns"]
        if "TLatexPositions" in oldDic:
            newDic["TLatexPositions"] = []
            for pos in oldDic["TLatexPositions"]:
                newDic["TLatexPositions"].append(dict(pos))
        return
    
    def outputDictionary(self, box, entries, align):
        # Create the dictionary with the output-type information.
        outDic = dict(box)
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
        if entries.kind == "legend":
            outDic["nColumns"] = entries.nCol
            return outDic
        # Needed as a final output: recommendation where to place the TLatex object.
        outDic["TLatexPositions"] = []
        for i in range(len(entries)):
            x1lat = x1
            if align == "right":
                x1lat = x2 - self.getTextWidth(entries[i])
            outDic["TLatexPositions"].append({"x" : x1lat
                                              , "y" : y1 - (i + 0.73) * self.entryHeight})
        # Needed by the method overlap() for check of horizontal
        #    overlap of texts, legends and labels entries.
        outDic["entriesCoor"] = []
        for i in range(len(entries)):
            x1coor = x1
            x2coor = x1 + self.getTextWidth(entries[i])
            if align == "right":
                x1coor = x2 - self.getTextWidth(entries[i])
                x2coor = x2
            outDic["entriesCoor"].append({"x1" : x1coor
                                          , "y1" : y1 - i * self.entryHeight
                                          , "x2" : x2coor
                                          , "y2" : y1 - (i + 1) * self.entryHeight})
        return outDic
    
    def overlap(self, LPanel, RPanel):
        LRectangles = []
        for box in LPanel:
            if box.kind == "legend":
                LRectangles.append(box.tmpCoor)
            else:
                for entry in box.tmpCoor["entriesCoor"]:
                    LRectangles.append(entry)
        RRectangles = []
        for box in RPanel:
            if box.kind == "legend":
                RRectangles.append(box.tmpCoor)
            else:
                for entry in box.tmpCoor["entriesCoor"]:
                    RRectangles.append(entry)
        for lentry in LRectangles:
            for rentry in RRectangles:
                if self.rectanglesOverlap(lentry, rentry):
                    return True
        return False

    def rectanglesOverlap(self, coor1, coor2):
        # Returns True if rectangles given by corners in coor1, coor2 overlap.
        lb = coor1
        rb = coor2
        if coor2["x1"] < coor1["x1"]:
            lb = coor2
            rb = coor1
        tb = lb
        bb = rb
        if rb["y1"] > lb["y1"]:
            tb = rb
            bb = lb
        if lb["x2"] >= rb["x1"] or lb["x1"] == rb["x1"] or lb["x2"] == rb["x2"]:
            if tb["y2"] < bb["y1"] or tb["y1"] == bb["y1"] or tb["y2"] == bb["y2"]:
                return True
        return False

    def updateMaxMin(self, box):
        # ATTENTION: method changes self.yMaxDyn, self.yMinDyn, 
        #    max and min of the "axes" histogram self.frame,
        #    tBox and bBox!!!!!!!
        # Returns suggested optimal y-axis maximum and minimum for
        #    a pad with box inserted; optimal means that the box 
        #    does not overlap with any other object in the pad.
        # Terminology inside the method:
        #    pt, pb ... y-max and y-min of plots within the box x-range
        #    bt, bb ... y-min (y-max) of the top (bottom) box
        #    et, eb ... minimum required distance box-plot relative to y-axis range
        #    M, m   ... y-axis maximum and minimum
        #    D   = M - m
        #    eps = self.textPlotsDist
        #    items without (with) "0" ... after (before) the update of the y-axis range.
        #    Ft  = eps + (M0 - bt0)/D0
        #    Fb  = eps + (bb0 - m0)/D0
        # First, check whether there is at least one plot in plots
        if len(self.plots) == 0: return False
        # Second, check whether yMin or yMax are set
        if self.yMax is not None and self.yMin is not None:
            return True
        # Set starting parameters:
        M0 = self.toLog(self.yMaxDyn)
        m0 = self.toLog(self.yMinDyn)
        D0 = M0 - m0
        et, eb = self.yMaxOffset, self.yMinOffset
        pt = self.toLog(self.getMaximum(self.xMin, self.xMax))
        bt0 = self.toLog(self.yMaxDyn)
        if self.yMax is not None: ##
            et = 0 ##
            if pt > M0: ##
                pt = M0 ##
                bt0 = M0 ##
        pb = self.toLog(self.getMinimum(self.xMin, self.xMax))
        bb0 = self.toLog(self.yMinDyn)
        if self.yMin is not None: ##
            eb = 0 ##
            if pb < m0: ##
                pb = m0 ##
                bb0 = m0 ##
        if box.vPos == "T":
            tmpEt = self.textPlotsDist
            tmpPt = self.toLog(self.getYMaxInBoxNDCRange(box))
            tmpBt0 = self.toLog(self.NDCtoY(box["y2"]))
            if self.tBox is None:
                self.tBox = box
                if tmpBt0 - tmpPt - tmpEt * D0 < bt0 - pt - et * D0: ##
                    et = self.textPlotsDist
                    pt = tmpPt
                    bt0 = tmpBt0
            else:
                currEt = self.textPlotsDist
                currTBpt = self.toLog(self.getYMaxInBoxNDCRange(self.tBox))
                currTBbt0 = self.toLog(self.NDCtoY(self.tBox["y2"]))
                if tmpBt0 - tmpPt - tmpEt * D0 < currTBbt0 - currTBpt - currEt * D0:
                    self.tBox = box
                    currEt = self.textPlotsDist
                    currTBpt = self.toLog(self.getYMaxInBoxNDCRange(self.tBox))
                    currTBbt0 = self.toLog(self.NDCtoY(self.tBox["y2"]))
                if currTBbt0 - currTBpt - currEt * D0 < bt0 - pt - et * D0:
                    et = currEt
                    pt = currTBpt
                    bt0 = currTBbt0
            if self.bBox is not None:
                tmpEb = self.textPlotsDist
                tmpPb = self.toLog(self.getYMinInBoxNDCRange(self.bBox))
                tmpBb0 = self.toLog(self.NDCtoY(self.bBox["y1"]))
                if tmpPb - tmpBb0 - tmpEb * D0 < pb - bb0 - eb * D0:
                    eb = tmpEb
                    pb = tmpPb
                    bb0 = tmpBb0
        if box.vPos == "B":
            tmpEb = self.textPlotsDist
            tmpPb = self.toLog(self.getYMinInBoxNDCRange(box))
            tmpBb0 = self.toLog(self.NDCtoY(box["y1"]))
            if self.bBox is None:
                self.bBox = box
                if tmpPb - tmpBb0 - tmpEb * D0 < pb - bb0 - eb * D0:
                    eb = self.textPlotsDist
                    pb = tmpPb
                    bb0 = tmpBb0
            else:
                currEb = self.textPlotsDist
                currBBpb = self.toLog(self.getYMinInBoxNDCRange(self.bBox))
                currBBbb0 = self.toLog(self.NDCtoY(self.bBox["y1"]))
                if tmpPb - tmpBb0 - tmpEb * D0 < currBBpb - currBBbb0 - currEb * D0:
                    self.bBox = box
                    currEb = self.textPlotsDist
                    currBBpb = self.toLog(self.getYMinInBoxNDCRange(self.bBox))
                    currBBbb0 = self.toLog(self.NDCtoY(self.bBox["y1"]))
                if currBBpb - currBBbb0 - currEb * D0 < pb - bb0 - eb * D0:
                    eb = currEb
                    pb = currBBpb
                    bb0 = currBBbb0
            if self.tBox is not None:
                tmpEt = self.textPlotsDist ##
                tmpPt = self.toLog(self.getYMaxInBoxNDCRange(self.tBox)) ##
                tmpBt0 = self.toLog(self.NDCtoY(self.tBox["y2"])) ##
                if tmpBt0 - tmpPt - tmpEt * D0 < bt0 - pt - et * D0: ##
                    et = tmpEt
                    pt = tmpPt
                    bt0 = tmpBt0
        # Speed the process up: return if there is nothing to change.
        if self.putTextAtTheTop and not self.putTextAtTheBottom:
            if bt0 >= pt + et * D0:
                return True
        elif not self.putTextAtTheTop and self.putTextAtTheBottom:
            if bb0 <= pb - eb * D0:
                return True
        else:
            if bt0 >= pt + et * D0 and bb0 <= pb - eb * D0:
                return True
        # Catch cases when self.yMax (self.yMin) is set to higher (lower)
        #    value than is pt (pb) but the difference self.yMax - pt (self.yMin - pb)
        #    is not enough large to put the box there.
        if self.yMax is not None:
            if self.putTextAtTheBottom and box.vPos == "B":
                if M0 - pt - et * D0 > 0:
                    pt = M0
        if self.yMin is not None:
            if self.putTextAtTheTop and box.vPos == "T":
                if pb - m0 - eb * D0 > 0:
                    pb = m0
        Ft = (M0 - bt0) / D0 + et
        Fb = (bb0 - m0) / D0 + eb
        # In principle, Fb should be >= 0; case Fb < 0 can only happen
        #    due to computer precision in which case Fb is just slightly
        #    lower than 0. Therefore, cases Fb < 0 are treated as Fb == 0.
        if Fb <= 0:
            m = pb
            M = 1 / (1 - Ft) * (-Ft * m + pt)
        else:
            m_denom = -Ft / (1 - Ft) - (-1 + Fb) / Fb
            m_nom = -pt / (1 - Ft) + pb / Fb
            m = 1 / m_denom * m_nom
            M = 1 / Fb * (m * (-1 + Fb) + pb)
        if self.yMax is not None:
            if m > m0:
                return False
            if not self.isZero((M - M0) / (M + M0)):
                return False
        if self.yMin is not None:
            if self.isZero(m0) and not self.isZero(m):
                return False
            if not self.isZero(m0) and not self.isZero((m - m0) / (abs(m) + abs(m0))):
                return False
            if M < M0:
                return False
        if self.yMax is None and self.yMin is None:
            if (m > m0 and not self.isClose(m, m0, 1.e-9)) or (M < M0 and not self.isClose(M, M0, 1.e-9)):
                return False
        #print "bt0", bt0,"pt", pt,"et", et,"bb0", bb0,"pb", pb,"eb", eb,"D0", D0
        #print "m0", m0, "M0", M0, "m", m, "M", M
        if self.pad.GetLogy():
            M, m = pow(10, M), pow(10, m)
        if self.yMax is not None:
            M = self.yMax
        if self.yMin is not None:
            m = self.yMin
        self.yMaxDyn, self.yMinDyn = M, m
        self.frame.SetMaximum(self.yMaxDyn)
        self.frame.SetMinimum(self.yMinDyn)
        self.pad.Modified()
        self.pad.Update()
        return True

    def toLog(self, y):
        if not self.pad.GetLogy():
            return y
        return math.log(y, 10)

    def updateMaximum(self, box):
        # Update plot maximum to avoid box clipping
        if self.yMax is not None:
            self.yMaxDyn = self.yMax
            self.frame.SetMaximum(self.yMaxDyn)
            self.pad.Modified()
            self.pad.Update()
            return True
        #print "    beginning: self.yMaxDyn", self.yMaxDyn
        # Check whether there is at least one plot in plots
        if len(self.plots) == 0: return False
        # Find the maximum value of a plot in plots
        plotsY = self.getYMaxInBoxNDCRange(box)
        # Minimum y-axis value of the text box
        #print "    middle1: boxYNDC", boxYNDC, "boxXNDC1", boxXNDC1, "boxXNDC2", boxXNDC2, "plotsY", plotsY
        boxY = self.NDCtoY(box["y2"])
        #print "    middle1: boxY", boxY, "boxX1", self.NDCtoX(boxXNDC1), "boxX2", self.NDCtoX(boxXNDC2), "plotsY", plotsY
        newYMax = self.yMaxDyn
        if self.pad.GetLogy():
            newYMax = math.log(self.yMaxDyn, 10)
        if plotsY > boxY:
            if not self.pad.GetLogy():
                h1 = self.yMaxDyn - boxY
                h2 = boxY - self.yMinDyn
                y1 = self.yMaxDyn - plotsY
                y2 = plotsY - self.yMinDyn
                v  = y2 * h1 / h2 - y1
                #newYMax += v
                b0 = boxY
                yMax = self.yMaxDyn
                yMin = self.yMinDyn
                p = plotsY
                F = (yMax - b0) / (b0 - yMin)
                eps = self.textPlotsDist
                delta = 1. / (1. - eps - eps * F) * ((1. + F) * (p + yMax * eps - yMin * eps) - yMax - yMin * F)
                newYMax += delta
            else:
                h1 = math.log(self.yMaxDyn, 10) - math.log(boxY, 10)
                h2 = math.log(boxY, 10) - math.log(self.yMinDyn, 10)
                y1 = math.log(self.yMaxDyn, 10) - math.log(plotsY, 10)
                y2 = math.log(plotsY, 10) - math.log(self.yMinDyn, 10)
                v  = y2 * h1 / h2 - y1
                #newYMax += v
                b0 = math.log(boxY, 10)
                yMax = math.log(self.yMaxDyn, 10)
                yMin = math.log(self.yMinDyn, 10)
                p = math.log(plotsY, 10)
                F = (yMax - b0) / (b0 - yMin)
                eps = self.textPlotsDist
                delta = 1. / (1. - eps - eps * F) * ((1. + F) * (p + yMax * eps - yMin * eps) - yMax - yMin * F)
                newYMax += delta
            #print "    middle2: delta", delta, "newYMax", newYMax
            if delta < 0:
                return False
        #print "    end: newYMax", newYMax if not self.pad.GetLogy() else pow(10, newYMax)
        if self.pad.GetLogy():
            newYMax = pow(10, newYMax)
        self.yMaxDyn = newYMax
        self.frame.SetMaximum(self.yMaxDyn)
        self.pad.Modified()
        self.pad.Update()
        return True

    def updateMinimum(self, box):
        # Update plot minimum to avoid box clipping
        if self.yMin is not None:
            self.yMinDyn = self.yMin
            self.frame.SetMinimum(self.yMinDyn)
            self.pad.Modified()
            self.pad.Update()
            return True
        #print "    beginning: self.yMinDyn", self.yMinDyn
        # Check whether there is at least one plot in plots
        if len(self.plots) == 0: return False
        # Find the minimum value of a plot in plots
        plotsY = self.getYMinInBoxNDCRange(box)
        # Maximum y-axis value of the text box
        boxY = self.NDCtoY(box["y1"])
        newYMin = self.yMinDyn
        if self.pad.GetLogy():
            newYMin = math.log(self.yMinDyn, 10)
        if plotsY < boxY:
            if not self.pad.GetLogy():
                b0 = boxY
                yMax = self.yMaxDyn
                yMin = self.yMinDyn
                p = plotsY
            else:
                b0 = math.log(boxY, 10)
                yMax = math.log(self.yMaxDyn, 10)
                yMin = math.log(self.yMinDyn, 10)
                p = math.log(plotsY, 10)
            D0 = yMax - yMin
            eps = self.textPlotsDist
            delta = D0 * (p - eps * D0 - b0) / (eps * D0 + b0 - yMax)
            newYMin -= delta
            #print "    middle2: delta", delta, "newYMin", newYMin
            if delta < 0:
                return False
        #print "    end: newYMin", newYMin if not self.pad.GetLogy() else pow(10, newYMin)
        if self.pad.GetLogy():
            newYMin = pow(10, newYMin)
        self.yMinDyn = newYMin
        self.frame.SetMinimum(self.yMinDyn)
        self.pad.Modified()
        self.pad.Update()
        return True

    def getYMaxInBoxNDCRange(self, box):
        # Get maximum y-value of self.plots in the range of box["x1"], box["x2"].
        # The box coordinates must be in NDC!!!
        if len(self.plots) == 0:
            print "In getYMaxInBoxNDCRange(): no plot in self.plots!"
            raise SystemExit()
        xMin = self.NDCtoX(box["x1"])
        xMax = self.NDCtoX(box["x2"])
        yMax = self.getMaximum(xMin, xMax)
        if self.pad.GetLogy() and yMax <= 0:
            return self.yMinDyn
        return yMax

    def getYMinInBoxNDCRange(self, box):
        # Get minimum y-value of self.plots in the range of box["x1"], box["x2"].
        # The box coordinates must be in NDC!!!
        # If the y-scale is logarithmic, return the minimal
        #    non-zero value instead.
        if len(self.plots) == 0:
            print "In getYMinInBoxNDCRange(): no plot in self.plots!"
            raise SystemExit()
        xMin = self.NDCtoX(box["x1"])
        xMax = self.NDCtoX(box["x2"])
        yMin = self.getMinimum(xMin, xMax)
        return yMin

    def getBoxSize(self, origX, origY, align, entries, yFactor = 1.):
        # Calculate box dimensions.
        if len(entries) == 0:
            return CustomDict({"x1" : 0, "y1" : 0, "x2" : 0, "y2" : 0})
        # Check if it is legend and set nCol.
        isLegend = (entries.kind == "legend")
        nCol = 1
        if hasattr(entries, "nCol"):
            nCol = entries.nCol
        # Determine box height.
        nRow = int(math.ceil(float(len(entries)) / nCol))
        height = nRow * self.entryHeight * yFactor
        # Determine box width.
        width = 0
        widths = [ 0 for i in range(nCol) ]
        for j in range(nRow):
            for i in range(nCol):
                k = j * nCol + i
                if k < len(entries):
                    textWidth = self.getTextWidth(entries[k])
                    if textWidth > widths[i]:
                        widths[i] = textWidth
        width = sum(widths)
        # Some legend-specific adjustments
        if isLegend:
            # Scale the width to account for the boxes which form 1/4 of the legend box width
            width *= 1.333
            # Scale with number of cols just because it looks better
            width += (nCol - 1) * 0.04
            if align == 'right':
                origX += (nCol - 1) * 0.01
        # Calculate coordinates
        x1 = origX
        y1 = origY
        x2 = origX + width
        y2 = origY - height
        if align == 'right':
            x1 = origX - width
            x2 = origX
        #print "In getBoxSize()"
        #print "   origX:", origX, "origY:", origY, "width:", width
        box = {"x1" : x1, "y1" : y1, "x2" : x2, "y2" : y2}
        return CustomDict(box)
    
    ## backup of Dan's method
    #def getTextWidth(self, text):
    #    # returns text width
    #    t = TLatex(0, 0, text)
    #    ww = array('I', [0])
    #    hh = array('I', [0])
    #    t.GetBoundingBox(ww, hh)
    #    # hack for root 5.34
    #    if float(ww[0]) == 0:
    #        gROOT.ProcessLine("UInt_t w = 0; UInt_t h = 0;")
    #        gROOT.ProcessLine("TLatex* tmp = new TLatex(0,0,\"%s\");" % text)
    #        gROOT.ProcessLine("tmp->GetBoundingBox(w, h);")
    #        from ROOT import w, h
    #        ww[0] = w
    #    www = 495.624 * float(ww[0]) / (self.pad.GetAbsHNDC()*self.pad.GetWh())
    #    # Dan's hack
    #    textWidth = www / (self.pad.GetAbsWNDC()*self.pad.GetWw()) * 1.66
    #    ## My hack: the constant 0.69 obtained from a measurement of the actual text widths wrt. the pad width
    #    #textWidth = www / (self.pad.GetAbsWNDC()*self.pad.GetWw()) * 1.66 * self.textWidthSF()
    #    #print "Text: ", text, " width: ", float(ww[0]), " pad width: ", self.pad.GetAbsWNDC()*self.pad.GetWw(), " pad height: ", self.pad.GetAbsHNDC()*self.pad.GetWh(), "textWidth:", textWidth, "GetAbsWNDC", self.pad.GetAbsWNDC(), "GetAbsHNDC", self.pad.GetAbsHNDC()
    #    return textWidth
    
    def getTextWidth(self, text):
        # Return text width in NDC.
        #self.pad.Modified()
        #self.pad.Update()
        # returns text width
        t = TLatex(self.topLeftTextPosX, self.topTextPosY, text)
        t.SetNDC()
        ww = array('I', [0])
        hh = array('I', [0])
        t.GetBoundingBox(ww, hh)
        # hack for root 5.34
        if float(ww[0]) == 0:
            gROOT.ProcessLine("UInt_t w = 0; UInt_t h = 0;")
            gROOT.ProcessLine("TLatex* tmp = new TLatex(0,0,\"%s\");" % text)
            gROOT.ProcessLine("tmp->GetBoundingBox(w, h);")
            from ROOT import w, h
            ww[0] = w
        
        x1NDC = self.topLeftTextPosX
        x1 = self.NDCtoX(x1NDC)
        x1Px = self.pad.XtoPixel(math.log(x1, 10) if self.pad.GetLogx() else x1)
        # In the following formula, the factor 1.58 was tuned to the font size of 27 pixels.
        # Then, a phenomenological (measured) formula self.textWidthSF() is applied
        #    to account for different font sizes (from 15 to 26 pixels).
        # Both the factor and formula were derived for the pad cmain in the following setup:
        #        gStyle.SetPadLeftMargin(0.16)
        #        gStyle.SetPadRightMargin(0.05)
        #        gStyle.SetPadBottomMargin(0.16)
        #        gStyle.SetPadTopMargin(0.05)
        #        cmother = TCanvas("cmother", "cmother", 600, 600)
        #        cmother.cd()
        #        cmain = TPad("cmain", gPad.GetTitle(), 0, 0.358, 1, 1)
        #        cmain.SetTopMargin(0.057)
        #        cmain.SetBottomMargin(0.03)
        #        cmain.Draw()
        #        cmother.cd()
        #        cratio = TPad("cratio", gPad.GetTitle(), 0, 0, 1, 0.358)
        #        cratio.SetBottomMargin(0.33)
        #        cratio.Draw()
        # The constant 4.56901604741e-06 is equal to
        #    1. / (self.pad.GetAbsHNDC()*self.pad.GetWh()) / (self.pad.GetAbsWNDC()*self.pad.GetWw())
        #    in the pad cmain from above.
        #    Therefore, 4.56901604741e-06 / (self.pad.GetAbsHNDC()*self.pad.GetWh()) / (self.pad.GetAbsWNDC()*self.pad.GetWw())
        #        is equal to 1 in cmain but is different from 1 in pads of different dimensions.
        x2Px = int(x1Px + ww[0] * 1.58 * self.textWidthSF() * self.universalTextScaleConstant())
        x2 = self.pad.PixeltoX(x2Px)
        if self.pad.GetLogx():
            x2 = pow(10, x2)
        x2NDC = self.XtoNDC(x2)
        textWidth = x2NDC - x1NDC
        #print "in getTextWidth()"
        #Dan = 495.624 * float(ww[0]) / (self.pad.GetAbsHNDC()*self.pad.GetWh()) / (self.pad.GetAbsWNDC()*self.pad.GetWw()) * 1.66
        #print "    Dan:", Dan, "me:", textWidth
        return x2NDC - x1NDC

    def getTextWidth_Olivier(self, text):
        t = TLatex(self.topLeftTextPosX, self.topTextPosY, text)
        t.SetNDC()
        w = array('I',[0])
        h = array('I',[0])
        f = t.GetTextFont()
        if f % 10 <= 2:
            t.GetTextExtent(w, h, t.GetTitle())
        else:
            w = array('I',[0])
            t2 = t
            t2.SetTextFont(f - 1)
            pad = self.pad #gROOT.GetSelectedPad()
            #if pad is None: return w
            dy = pad.AbsPixeltoY(0) - pad.AbsPixeltoY(int(t.GetTextSize()))
            tsize = dy / (pad.GetY2() - pad.GetY1())
            t2.SetTextSize(tsize)
            t2.GetTextExtent(w, h, t2.GetTitle())
        return w[0]

    def getTextWidth_backup2(self, text):
        # Return text width in NDC.
        #self.pad.Modified()
        #self.pad.Update()
        # returns text width
        t = TLatex(self.topLeftTextPosX, self.topTextPosY, text)
        t.SetNDC()
        #ww = array('I', [0])
        #hh = array('I', [0])
        gROOT.ProcessLine("UInt_t w = 0; UInt_t h = 0;")
        gROOT.ProcessLine("TLatex* tmp = new TLatex(0,0,\"{0}\");".format(text))
        gROOT.ProcessLine("tmp->GetTextExtent(w, h, \"{0}\");".format(text))
        from ROOT import w, h
        #ww[0] = w
        #print "in getTextWidth()"
        #print "    orig", self.getTextWidth_backup(text), w
        return w

    def getTextWidth_backup3(self, text):
        # Return text width in NDC.
        #self.pad.Modified()
        #self.pad.Update()
        # returns text width
        t = TLatex(self.topLeftTextPosX, self.topTextPosY, text)
        t.SetNDC()
        w = t.GetXsize()
        print "in getTextWidth()"
        print "    orig", self.getTextWidth_backup1(text), w
        print "    calib const", self.universalTextScaleConstant()
        return w

    def getMultiTextWidth(self, lines):
        # returns width of the multiline text
        width = 0
        for text in lines:
            textWidth = self.getTextWidth(text)
            if textWidth > width:
                width = textWidth
        return width
    
    def textWidthSF(self, fsp = None):
        if fsp is None:
            fsp = gStyle.GetTextSize() # the text size must be set in pixels!!!
        if fsp == 27: return 1.
        if fsp > 23 and fsp < 27:
            return self.interpolateSF(fsp, 23, 27)
        if fsp == 23: return 1.05
        if fsp > 19 and fsp < 23:
            return self.interpolateSF(fsp, 19, 23)
        if fsp == 19: return 1.10
        if fsp > 15 and fsp < 19:
            return self.interpolateSF(fsp, 15, 19)
        if fsp == 15: return 0.99
        return None
    
    def universalTextScaleConstant(self):
        return 1. / 4.56901604741e-06 / (self.pad.GetAbsHNDC()*self.pad.GetWh()) / (self.pad.GetAbsWNDC()*self.pad.GetWw())

    def interpolateSF(self, fsp, s1 = None, s2 = None):
        if s1 is not None and s2 is not None:
            DeltaS = s2 - s1
            DeltaY = self.textWidthSF(s2) - self.textWidthSF(s1)
            return self.textWidthSF(s1) + (fsp - s1) * DeltaY / DeltaS
    
    def getPanelWidth(self, panel):
        # Return width of the widest box in the panel.
        width = 0
        for b in panel:
            if b.kind == "legend":
                tmp = self.getLegendWidth(b)
            else:
                tmp = self.getMultiTextWidth(b)
            if tmp > width:
                width = tmp
        return width

    def getLegendWidth(self, entries):
        # Return width of a legend.
        # Entries are text entries in the legend;
        #     it is a list of strings.
        if entries.kind != "legend":
            print "In layout_helper.getLegendWidth(): attribute kind of the provided list is not a legend!"
            raise SystemExit()
        box = self.getBoxSize(origX = self.topLeftTextPosX
                              , origY = self.topTextPosY
                              , align = 'left', entries = entries)
        return box["x2"] - box["x1"]

    def maxLegendWidthInPanel(self, panel):
        # Note: there might be several legends in a panel.
        # Return the maximum width of a legend in panel.
        legWidth = 0
        for b in panel:
            if b.kind == "legend":
                tmp = self.getLegendWidth(b) / b.nCol
                if tmp > legWidth:
                    legWidth = tmp
        return legWidth
    
    def getBoxHeight(self, entries):
        # Return height of a box.
        # Entries are text entries in the box;
        #     it is a list of strings.
        box = self.getBoxSize(origX = self.topLeftTextPosX
                              , origY = self.topTextPosY
                              , align = 'left', entries = entries)
        return box["y1"] - box["y2"]

    def getMaximum(self, xMin = None, xMax = None):
        # Get maximum of a plot in self.plots.
        # Regarding output, see description of getObjectMaxAndMin().
        # If xMin is just an edge of a histogram bin or graph point,
        #    use xMin + abs(xMin) * 1.e-9.
        # If xMax is just an edge of a histogram bin or graph point,
        #    use xMax - abs(xMax) * 1.e-9.
        # If all objects in self.plots have x-range outside (xMin, xMax),
        #    return self.yMinDyn.
        if len(self.plots) == 0:
            print "In layout_helper.getMaximum(): no plot in self.plots!"
            raise SystemExit()
        if xMin is None:
            xMin = self.xMin
        if xMax is None:
            xMax = self.xMax
        yMax, yMin = self.getObjectMaxAndMin(self.plots[0], xMin, xMax)
        ###############
        #plot0 = self.toTH1(self.plots[0])
        #if self.considerUncertainties:
        #    plot0 = self.addUncertainty(self.plots[0], 1.)
        #yMax, yMin = self.getMaxAndMin(plot0, xMin, xMax)
        ###############
        for ip in range(1, len(self.plots)):
            tmpYMax, tmpYMin = self.getObjectMaxAndMin(self.plots[ip], xMin, xMax)
            if yMax is None or tmpYMax > yMax:
                yMax = tmpYMax
            ###############
            #plot = self.toTH1(self.plots[ip])
            #if self.considerUncertainties:
            #    plot = self.addUncertainty(self.plots[ip], 1.)
            #tmpYMax, tmpYMin = self.getMaxAndMin(plot, xMin, xMax)
            #if tmpYMax > yMax:
            #    yMax = tmpYMax
            ###############
        return yMax
    
    def getMinimum(self, xMin = None, xMax = None):
        # Get minimum of a plot in self.plots if y-axis scale is linear.
        # Regarding output, see description of getObjectMaxAndMin().
        # If xMin is just an edge of a histogram bin or graph point,
        #    use xMin + abs(xMin) * 1.e-9.
        # If xMax is just an edge of a histogram bin or graph point,
        #    use xMax - abs(xMax) * 1.e-9.
        # If all objects in self.plots have x-range outside (xMin, xMax),
        #    return self.yMaxDyn.
        if len(self.plots) == 0:
            print "In layout_helper.getMinimum(): no plot in self.plots!"
            raise SystemExit()
        if xMin is None:
            xMin = self.xMin
        if xMax is None:
            xMax = self.xMax
        yMax, yMin = self.getObjectMaxAndMin(self.plots[0], xMin, xMax)
        ###############
        #plot0 = self.toTH1(self.plots[0])
        #if self.considerUncertainties:
        #    plot0 = self.addUncertainty(self.plots[0], -1.)
        #yMax, yMin = self.getMaxAndMin(plot0, xMin, xMax)
        #if self.pad.GetLogy():
        #    yMin = self.getNonZeroMin(plot0, xMin, xMax)
        ###############
        for ip in range(1, len(self.plots)):
            tmpYMax, tmpYMin = self.getObjectMaxAndMin(self.plots[ip], xMin, xMax)
            if tmpYMin is None:
                continue
            if yMin is None or tmpYMin < yMin:
                yMin = tmpYMin
            ###############
            #plot = self.toTH1(self.plots[ip])
            #if self.considerUncertainties:
            #    plot = self.addUncertainty(self.plots[ip], -1.)
            #tmpYMax, tmpYMin = self.getMaxAndMin(plot, xMin, xMax)
            #if self.pad.GetLogy():
            #    tmpYMin = self.getNonZeroMin(plot, xMin, xMax)
            #if tmpYMin < yMin:
            #    yMin = tmpYMin
            ###############
        return yMin

    def getObjectMaxAndMin(self, obj, xMin, xMax):
        # Return the max and min of object obj within the range (xMin, xMax);
        #    the object must be TH1, TGraph, THStack, TF1 or TLine;
        #    otherwise, return (self.yMinDyn, self.yMaxDyn);
        #    btw. (self.yMinDyn, self.yMaxDyn) means that the object is ignored.
        # Return (self.yMinDyn, self.yMaxDyn) if the object x-range
        #    is outside (xMin, xMax).
        # Return (yMax, self.yMaxDyn) if self.pad.GetLogy() and the object
        #    is TH1, TGraph or THStack and has bins with negative or zero content.
        histo = self.toTH1(obj)
        # For TH1, TGraph and THStack:
        if histo is not None:
            # yMax first
            h = histo.Clone()
            if self.considerUncertainties:
                h = self.addUncertainty(h, 1.)
            yMax, dummy = self.getMaxAndMin(h, xMin, xMax)
            # yMin second
            h = histo.Clone()
            if self.considerUncertainties:
                h = self.addUncertainty(h, -1.)
            dummy, yMin = self.getMaxAndMin(h, xMin, xMax)
            if self.pad.GetLogy():
                yMin = self.getNonZeroMin(h, xMin, xMax)
            if yMin is None:
                return yMax, self.yMaxDyn
            return yMax, yMin
        # For TF1:
        if isinstance(obj, TF1):
            x1 = obj.GetXmin()
            x2 = obj.GetXmax()
            if xMax <= x1 or xMin >= x2:
                return self.yMinDyn, self.yMaxDyn
            if xMax > x2:
                xMax = x2
            if xMin < x1:
                xMin = x1
            return obj.GetMaximum(xMin, xMax), obj.GetMinimum(xMin, xMax)
        # For TLine:
        if isinstance(obj, TLine):
            x1 = obj.GetX1()
            y1 = obj.GetY1()
            x2 = obj.GetX2()
            y2 = obj.GetY2()
            if x1 > x2:
                x1 = obj.GetX2()
                y1 = obj.GetY2()
                x2 = obj.GetX1()
                y2 = obj.GetY1()
            if xMax <= x1 or xMin >= x2:
                return self.yMinDyn, self.yMaxDyn
            if self.isZero(x2 - x1):
                if y2 > y1:
                    return y2, y1
                return y1, y2
            if xMax > x2:
                xMax = x2
            if xMin < x1:
                xMin = x1
            yMax = y1 + (y2 - y1) / (x2 - x1) * (xMax - x1)
            yMin = y1 + (y2 - y1) / (x2 - x1) * (xMin - x1)
            if self.pad.GetLogy():
                slope = (self.toLog(y2) - self.toLog(y1)) / (x2 - x1)
                yMax = pow(10, self.toLog(y1) + slope * (xMax - x1))
                yMin = pow(10, self.toLog(y1) + slope * (xMin - x1))
            if yMin > yMax:
                return yMin, yMax
            return yMax, yMin
        return self.yMinDyn, self.yMaxDyn

    def getXMaxAndMin(self):
        xMax, xMin = None, None
        for p in self.plots:
            tmpXMax, tmpXMin = None, None
            plot = self.toTH1(p)
            if plot is not None:
                tmpXMax = plot.GetBinLowEdge(plot.GetNbinsX() + 1)
                tmpXMin = plot.GetBinLowEdge(1)
            elif isinstance(p, TF1):
                tmpXMax, tmpXMin = p.GetXmax(), p.GetXmin()
            elif isinstance(p, TLine):
                x1, x2 = p.GetX1(), p.GetX2()
                if x2 > x1:
                    tmpXMax, tmpXMin = x2, x1
                else:
                    tmpXMax, tmpXMin = x1, x2
            else:
                print "ERROR: object type in plots({0})".format(`type(p)`)
                print "    is not supported!"
                raise SystemExit()
            if xMax is None and xMin is None:
                xMax, xMin = tmpXMax, tmpXMin
            else:
                if tmpXMax > xMax:
                    xMax = tmpXMax
                if tmpXMin < xMin:
                    xMin = tmpXMin
        return xMax, xMin

    def offsetMaxAndMin(self):
        # Calculate new max (min) that is higher (lower) by
        #    self.yMaxOffset (self.yMinOffset).
        if self.yMax is not None and self.yMin is not None:
            return self.yMax, self.yMin
        if self.yMax is not None:
            return self.yMax, self.offsetMin()
        if self.yMin is not None:
            return self.offsetMax(), self.yMin
        if self.yMaxOffset is None or self.isZero(self.yMaxOffset):
            return self.yMaxDyn, self.offsetMin()
        if self.yMinOffset is None or self.isZero(self.yMinOffset):
            return self.offsetMax(), self.yMinDyn
        em = self.yMinOffset
        eM = self.yMaxOffset
        if em + eM >= 1:
            print "ERROR: self.yMinOffset + self.yMaxOffset >= 1!"
            raise SystemExit()
        pt = self.toLog(self.yMaxDyn)
        pb = self.toLog(self.yMinDyn)
        m = 1 / (1 - eM - em) * (pb * (1 - eM) - em * pt)
        M = pt + eM / em * (pb - m)
        if self.pad.GetLogy():
            return pow(10, M), pow(10, m)
        return M, m
    
    def offsetMin(self):
        # Calculate new minimum that is lower by self.yMinOffset;
        #    self.yMinOffset is in units relative to the y-axis range.
        if self.yMin is not None: return self.yMin
        if self.yMinOffset is None: return self.yMinDyn
        # For linear y-axis scale
        #height = self.yMaxDyn - self.yMinDyn
        #newMin = self.yMinDyn - self.yMinOffset * height
        eps = self.yMinOffset
        newMin = 1 / (1 - eps) * (self.yMinDyn - eps * self.yMaxDyn)
        # For logarithmic y-axis scale
        if self.pad.GetLogy():
            minimum = math.log(self.yMinDyn, 10)
            maximum = math.log(self.yMaxDyn, 10)
            #height = maximum - minimum
            #newMin = minimum - self.yMinOffset * height
            newMin = 1 / (1 - eps) * (minimum - eps * maximum)
            newMin = pow(10, newMin)
        return newMin
        
    def offsetMax(self):
        # Calculate new maximum that is higher by self.yMaxOffset;
        #    self.yMaxOffset is in units relative to the y-axis range.
        if self.yMax is not None: return self.yMax
        if self.yMaxOffset is None: return self.yMaxDyn
        # For linear y-axis scale
        #height = self.yMaxDyn - self.yMinDyn
        #newMax = self.yMaxDyn + self.yMaxOffset * height
        eps = self.yMaxOffset
        newMax = 1 / (1 - eps) * (self.yMaxDyn - eps * self.yMinDyn)
        # For logarithmic y-axis scale
        if self.pad.GetLogy():
            minimum = math.log(self.yMinDyn, 10)
            maximum = math.log(self.yMaxDyn, 10)
            #height = maximum - minimum
            #newMax = maximum + self.yMaxOffset * height
            newMax = 1 / (1 - eps) * (maximum - eps * minimum)
            newMax = pow(10, newMax)
        return newMax

    def placePredefinedPanelsToPad(self):
        # User predefined content of panels and this method places them to the pad.
        # Maximum and minimum of the y-axis are adjusted if self.yMin is None and self.yMax is None.
        # Minimum of the y-axis is adjusted if self.yMin is None and self.yMax is not None.
        # Maximum of the y-axis is adjusted if self.yMin is not None and self.yMax is None.
        if self.predefinedPanels is None:
            print "No text box or legend was provided!"
            print "If you want to decide your text layout yourself, use"
            print "    methods add[Legend, Text]ToPanel() together with"
            print "    the switch self.placePredefinedPanels == True."
            print "Otherwise, set self.placePredefinedPanels to False!"
            return False
        # Enable both options
        self.putTextAtTheTop = True
        self.putTextAtTheBottom = True
        # Place panels to the pad
        if self.verbose > 1:
            print "INFO: In tryLayout(): printing panels before placing them."
            print "TLPanel", self.predefinedPanels["TL"]
            print "TRPanel", self.predefinedPanels["TR"]
            print "BLPanel", self.predefinedPanels["BL"]
            print "BRPanel", self.predefinedPanels["BR"]
        self.nLayoutsTried = 1
        self.nLayoutsWithNonSuitedPanel = 0
        self.nLayoutsWithOverlapedBoxes = 0
        if not self.placeTopPanelToPad(self.predefinedPanels["TL"], "L"):
            self.nLayoutsWithNonSuitedPanel += 1
            print "ERROR: maybe yMax settings forces text and objects to overlap."
            return False
        if not self.placeTopPanelToPad(self.predefinedPanels["TR"], "R"):
            self.nLayoutsWithNonSuitedPanel += 1
            print "ERROR: maybe yMax settings forces text and objects to overlap."
            return False
        if not self.placeBottomPanelToPad(self.predefinedPanels["BL"], "L"):
            self.nLayoutsWithNonSuitedPanel += 1
            print "ERROR: maybe yMax settings forces text and objects to overlap."
            return False
        if not self.placeBottomPanelToPad(self.predefinedPanels["BR"], "R"):
            self.nLayoutsWithNonSuitedPanel += 1
            print "ERROR: maybe yMax settings forces text and objects to overlap."
            return False
        if self.overlap(self.predefinedPanels["TL"], self.predefinedPanels["TR"]):
            self.nLayoutsWithOverlapedBoxes += 1
            if not self.ignoreHorizontalBoxOverlaps:
                return False
        if self.overlap(self.predefinedPanels["BL"], self.predefinedPanels["BR"]):
            self.nLayoutsWithOverlapedBoxes += 1
            if not self.ignoreHorizontalBoxOverlaps:
                return False
        if self.verbose > 1:
            print "INFO: In placePredefinedPanelsToPad(): printout after having placed panels"
            print "    self.yMaxDyn", self.yMaxDyn, "self.yMinDyn", self.yMinDyn
        if self.verbose:
            print "In placeAllTextToPad(), summary:"
            print "    {0} layouts tried".format(self.nLayoutsTried)
            nSucc = self.nLayoutsTried - self.nLayoutsWithNonSuitedPanel
            if not self.ignoreHorizontalBoxOverlaps:
                nSucc -= self.nLayoutsWithOverlapedBoxes
            print "    {0} layouts successfull".format(nSucc)
            print "    {0} layouts with non-suited panels".format(self.nLayoutsWithNonSuitedPanel)
            print "    {0} layouts with overlapping boxes".format(self.nLayoutsWithOverlapedBoxes)
        if self.nLayoutsWithNonSuitedPanel == self.nLayoutsTried:
            if self.verbose:
                print "All tried layouts failed!"
                print "    All panels are too height!"
            return False
        if self.nLayoutsWithNonSuitedPanel + self.nLayoutsWithOverlapedBoxes == self.nLayoutsTried:
            if self.verbose:
                print "All tried layouts failed!"
                print "    All layouts yield either a too height panel or"
                print "    overlapping boxes."
            if not self.ignoreHorizontalBoxOverlaps:
                return False
            else:
                if self.verbose:
                    print "Ignoring horizontal box overlaps."
        self.frame.SetMaximum(self.yMaxDyn)
        self.frame.SetMinimum(self.yMinDyn)
        self.pad.Modified()
        self.pad.Update()
        # Copy the coordinates to the output dictionaries.
        for i in range(len(self.legends)):
            self.copyOutputDictionary(self.legends[i].tmpCoor, self.outListLeg[i])
        for i in range(len(self.texts)):
            self.copyOutputDictionary(self.texts[i].tmpCoor, self.outListTexts[i])
        return True



    def placePredefinedPanelsToPad_yAxRangeFixed(self):
        # User predefined content of panels and this method places them to the pad.
        # This version is used only if self.yMin is not None and self.yMax is not None.
        if self.predefinedPanels is None:
            print "No text box or legend was provided!"
            print "If you want to decide your text layout yourself, use"
            print "    methods add[Legend, Text]ToPanel() together with"
            print "    the switch self.placePredefinedPanels == True."
            print "Otherwise, set self.placePredefinedPanels to False!"
            return False
        for key in self.predefinedPanels:
            panel = self.predefinedPanels[key]
            if len(panel) == 0:
                continue
            # Check if there is a legend in the panel
            legWidth = self.maxLegendWidthInPanel(panel)
            LPosX = self.topLeftTextPosX
            if "B" in key:
                LPosX = self.bottomLeftTextPosX
            RPosX = self.topRightTextPosX
            if "B" in key:
                RPosX = self.bottomRightTextPosX
            for ib in range(len(panel)):
                x = LPosX + legWidth * 0.0333
                if "R" in key:
                    x = RPosX - self.getPanelWidth(panel) + legWidth * 0.0333
                if panel[ib].kind == "legend":
                    x = LPosX
                    if "R" in key:
                        x = RPosX - self.getPanelWidth(panel)
                prevY = self.topTextPosY
                if "B" in key:
                    prevY = self.bottomTextPosY
                if ib > 0:
                    if "T" in key:
                        prevY = panel[ib - 1].coor["y2"]
                    if "B" in key:
                        prevY = panel[ib - 1].coor["y1"]
                y = prevY
                if "B" in key:
                    y = prevY + self.getBoxHeight(panel[ib])
                box = self.getBoxSize(origX = x, origY = y
                                      , align = "left", entries = panel[ib])
                panel[ib].coor = self.outputDictionary(box, panel[ib], "left")
        # Copy the coordinates to the output dictionaries.
        for i in range(len(self.legends)):
            self.copyOutputDictionary(self.legends[i].coor, self.outListLeg[i])
        for i in range(len(self.texts)):
            self.copyOutputDictionary(self.texts[i].coor, self.outListTexts[i])
        return True
    
    
    #############################################
    ## Object conversion methods
    #############################################
    
    def histoListToTHStack(self, hList):
        s = THStack("s", "")
        for dicto in hList:
            s.Add(dicto["Histogram"].Clone())
        return s
    
    def toTH1(self, plot):
        if isinstance(plot, THStack):
            # Sum the THStack to one histo
            plot = self.sumTHStack(plot)
        elif isinstance(plot, TGraph):
            # Convert graph to histos and use the nominal histo
            plot = self.graphToHistos(plot)[0]
        elif isinstance(plot, TH1):
            plot = plot.Clone()
        else:
            return None
        return plot
    
    def addUncertainty(self, plot, Nsigma):
        # Add an uncertainty to the nominal value of a TH1, THStack or TGraph;
        #    does not modify plot!
        #    Schematically: plot is cloned, the uncertainty is added to the
        #    clone and the clone is returned.
        # Nsigma is a float of type "<sign><Nsigma>"; e.g. schematically:
        #    Nsigma == 2 means: add 2 * plot.GetUpError(bin) to plot.GetBinContent(bin)
        #    Nsigma == -1.5 means: subtract 1.5 * plot.GetDownError(bin) from plot.GetBinContent(bin)
        nom = None
        unc = None
        if isinstance(plot, THStack):
            # Sum the THStack to one histo
            nom = self.sumTHStack(plot)
            unc = nom.Clone()
            for ib in range(1, unc.GetNbinsX() + 1):
                unc.SetBinContent(ib, unc.GetBinError(ib))
        elif isinstance(plot, TGraph):
            # Convert graph to histos [nom, up, down]
            hList = self.graphToHistos(plot)
            nom = hList[0]
            # The commented part below only works if up uncertainties go in the up direction
            #    and down uncertainties go in the down direction.
            #if Nsigma >= 0:
            #    unc = hList[1]
            #    unc.Add(nom, -1.)
            #else:
            #    unc = hList[2]
            #    unc.Add(nom, -1.)
            #    unc.Scale(-1.)
            # Generic treatment without assumptions on the up and down uncertainties
            up, down = hList[1], hList[2]
            for ib in range(1, nom.GetNbinsX() + 1):
                b_nom = nom.GetBinContent(ib)
                b_up = up.GetBinContent(ib) - b_nom
                b_down = down.GetBinContent(ib) - b_nom
                if b_up >= 0 and b_down >= 0:
                    if b_down > b_up: b_up = b_down
                    b_down = 0
                elif b_up <= 0 and b_down <= 0:
                    if b_up < b_down: b_down = b_up
                    b_up = 0
                elif b_up <= 0 and b_down >= 0:
                    b_up, b_down = b_down, b_up
                up.SetBinContent(ib, abs(b_up))
                down.SetBinContent(ib, abs(b_down))
            if Nsigma >= 0:
                unc = up
            else:
                unc = down
        elif isinstance(plot, TH1):
            nom = plot.Clone()
            unc = nom.Clone()
            for ib in range(1, unc.GetNbinsX() + 1):
                unc.SetBinContent(ib, unc.GetBinError(ib))
        else:
            return None
        nom.Add(unc, Nsigma)
        return nom
        
    
    
    #############################################
    ## miscanellous methods
    #############################################
    
    def checkListOfStr(self, l, methodName):
        message = "In {0}: method parameter must be a list of str!".format(methodName)
        if not isinstance(l, list):
            print message
            print "    Type provided:", type(l)
            raise SystemExit()
        for s in l:
            if not isinstance(s, str):
                print message
                raise SystemExit()
        return

    def checkOutDic(self, outDic, methodName):
        if outDic is not None:
            if not isinstance(outDic, dict) and not isinstance(outDic, str):
                print "In {0}: parameter outDic must be either None, dict or str!".format(methodName)
                print "    This type provided:", type(outDic)
                raise SystemExit()
        return
    
    def checkInputPlots(self, xMin = None, xMax = None):
        for p in self.plots:
            plot = None
            yMin = None
            plot = self.toTH1(p)
            if plot is None:
                if not isinstance(p, TF1):
                    if not isinstance(p, TLine):
                        print "ERROR: unknown plot type:", `type(p)`
                        raise SystemExit()
            if xMin is None and xMax is None:
                continue
            if plot is not None:
		print self, xMin, xMax
                yMax, yMin = self.getMaxAndMin(plot, xMin, xMax)
                if self.pad.GetLogy() and yMin <= 0:
                    if self.verbose:
                        print "WARNING: object", p.GetName(), "has minimum <= 0;"
                        print "    this is not a problem if you don't want to display"
                        print "    these non-positive values."
                continue
            if isinstance(p, TF1):
                if self.pad.GetLogy():
                    x1 = p.GetXmin()
                    x2 = p.GetXmax()
                    if xMax <= x1 or xMin >= x2:
                        continue
                    if xMax > x2:
                        xMax = x2
                    if xMin < x1:
                        xMin = x1
                    if p.GetMinimum(xMin, xMax) <= 0:
                        print "ERROR: function", p.GetName(), "has minimum <= 0;"
                        print "    this is incompatible with logarithmic y-axis!"
                        print "    function min is:", p.GetMinimum(x1, x2)
                        raise SystemExit()
            if isinstance(p, TLine):
                if self.pad.GetLogy():
                    if p.GetY1() <= 0 or p.GetY2 <= 0:
                        print "ERROR: provided TLine has minimum <= 0;"
                        print "    this is incompatible with logarithmic y-axis!"
                        raise SystemExit()
        return
    
    def someLayoutPassed(self):
        passed = False
        if self.atlasLabel is not None:
            if hasattr(self.atlasLabel, "coor"):
                passed = True
        for leg in self.legends:
            if hasattr(leg, "coor"):
                passed = True
        for t in self.texts:
            if hasattr(t, "coor"):
                passed = True
        return passed

    
    #############################################
    ## converts NDC to user
    #############################################
    
    def NDCtoX(self, ndcx):
        self.pad.Update()
        ax = (ndcx - self.pad.GetLeftMargin()) / self.GetRatioWidthNDCAxis() + self.GetUxmin()
        return self.AxisToX(ax)
    
    def NDCtoY(self, ndcy):
        ay = (ndcy - self.pad.GetBottomMargin()) / self.GetRatioHeightNDCAxis() + self.GetUymin()
        return self.AxisToY(ay)
    
    def GetRatioWidthNDCAxis(self):
        return self.GetFrameWidthNDC() / self.GetFrameWidthAxis()
    
    def GetUxmin(self):
        self.pad.Update()
        return self.pad.GetUxmin()
    
    def GetUxmax(self):
        self.pad.Update()
        return self.pad.GetUxmax()
    
    def GetFrameWidthNDC(self):
        return 1.0 - self.pad.GetLeftMargin() - self.pad.GetRightMargin()
    
    def GetFrameWidthAxis(self):
        return self.GetUxmax() - self.GetUxmin()
    
    def AxisToX(self, ax):
        return self.AxisToUser(ax, self.pad.GetLogx())
    
    def AxisToY(self, ay):
        return self.AxisToUser(ay, self.pad.GetLogy())
    
    def AxisToUser(self, x, logx):
        if logx:
            return pow(10, x)
        else:
            return x
        return None

    def XtoAxis(self, x):
        if not self.pad.GetLogx():
            return x
        return math.log(x, 10)
        
    def XtoNDC(self, x):
        self.pad.Update()
        dx = self.XtoAxis(x) - self.GetUxmin()
        dndc = dx * self.GetRatioWidthNDCAxis()
        ndcx = self.pad.GetLeftMargin() + dndc
        return ndcx
    
    def GetRatioHeightNDCAxis(self):
        return self.GetFrameHeightNDC() / self.GetFrameHeightAxis()
    
    def GetFrameHeightNDC(self):
        return 1.0 - self.pad.GetTopMargin() - self.pad.GetBottomMargin()
    
    def GetFrameHeightAxis(self):
        return self.GetUymax() - self.GetUymin()
    
    def GetUymax(self):
        self.pad.Update()
        return self.pad.GetUymax()
    
    def GetUymin(self):
        self.pad.Update()
        return self.pad.GetUymin()
    
    


