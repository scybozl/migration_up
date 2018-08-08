#ifndef HISTOUTILITIES_H_
#define HISTOUTILITIES_H_

#include "TopMass_13TeV_Plotting/Enums.h" 

#include "TChain.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TH2D.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>

TH1D AddOverflow(TH1D);
void PlotCutflow(std::string, std::string);
bool passBin(int, int, BINS, BINS);
bool passJetAndBTagBin(int, int, BINS, BINS);
float GetHistoUncertainty(TH1D, float);

#endif
