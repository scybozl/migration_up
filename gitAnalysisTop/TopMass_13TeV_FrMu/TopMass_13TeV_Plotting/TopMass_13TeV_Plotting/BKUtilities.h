#ifndef BKUTILITIES_H_
#define BKUTILITIES_H_

#include "TChain.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TH2F.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>

double deltaPhi(float, float);

std::vector<std::string> GetFileList(std::string);

TChain* ChainFiles(std::string, std::string);

std::pair<float, int> CalculateTotalEventNumberTree(TChain*);

std::pair<float, int> CalculateTotalEventNumberHisto(std::vector<std::string>, TChain *, std::string);

TH2D MakeNtupleCutflow(std::vector<std::string>, std::string);

#endif
