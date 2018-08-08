#include "TopMass_13TeV_Plotting/HistoUtilities.h"
#include "TopMass_13TeV_Plotting/Enums.h"

#include "TChain.h"
#include "TStyle.h"
#include "TFile.h"
#include "TTree.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TH1D.h"
#include "TH2D.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <set>
#include <iomanip>
#include <vector>
#include <string>
#ifdef __MAKECINT__
#pragma link C++ class std::vector<std::vector<int> >* +;
#endif

void PlotCutflow(std::string input_file, std::string output_file)
{

  TFile  *infile = new TFile(input_file.c_str(),  "READ");

  TH2D histo     = *(TH2D*) infile -> Get("cutflow");
  
  TCanvas *c0    = new TCanvas("c0", "Cutflow numbers for different regions", 700, 700);

  histo.GetXaxis()->SetBinLabel(1, "0 B incl.");
  histo.GetXaxis()->SetBinLabel(2, "2 B excl.");
  histo.GetXaxis()->SetBinLabel(3, "3 B excl.");
  histo.GetXaxis()->SetBinLabel(4, "4 B incl.");
  histo.GetYaxis()->SetBinLabel(1, "4 J excl.");
  histo.GetYaxis()->SetBinLabel(2, "5 J excl.");
  histo.GetYaxis()->SetBinLabel(3, "6 J incl.");

  histo.LabelsOption("u");

  histo.GetXaxis()->SetLabelSize(0.06);
  histo.GetXaxis()->SetLabelOffset(0.008);
  histo.GetXaxis()->SetTitleOffset(1.5);
  //  histo.GetXaxis()->SetTitle("Cutflow numbers for different regions");
  histo.GetYaxis()->SetTitleSize(0.055);
  histo.GetYaxis()->SetTitleOffset(0.85);
  gStyle->SetOptStat(0);

  histo.Draw("COLZ");
  histo.Draw("text:same");

  std::cout << output_file.c_str()  << "\t" << histo.Integral() << std::endl;

  c0 -> Print(output_file.c_str());

  infile -> Close();

  //delete c0;
  delete infile;

}

TH1D AddOverflow(TH1D fHisto)
{

  TH1D HelpHisto = fHisto;

  int nbins = HelpHisto.GetNbinsX();

  float underflow_bin = HelpHisto.GetBinContent(0);
  float first_bin     = HelpHisto.GetBinContent(1);

  float last_bin      = HelpHisto.GetBinContent(nbins);
  float overflow_bin  = HelpHisto.GetBinContent(nbins+1);

  float underflow_bin_unc = HelpHisto.GetBinError(0);
  float first_bin_unc     = HelpHisto.GetBinError(1);

  float last_bin_unc      = HelpHisto.GetBinError(nbins);
  float overflow_bin_unc  = HelpHisto.GetBinError(nbins+1);

  float total_unc_under   = sqrt(underflow_bin_unc*underflow_bin_unc + first_bin_unc*first_bin_unc);
  float total_unc_over    = sqrt(overflow_bin_unc*overflow_bin_unc   + last_bin_unc*last_bin_unc);

  HelpHisto.SetBinContent(1,     underflow_bin+first_bin);
  HelpHisto.SetBinContent(nbins, overflow_bin+last_bin);

  HelpHisto.SetBinContent(0,       0.0);
  HelpHisto.SetBinContent(nbins+1, 0.0);

  HelpHisto.SetBinError(1,     total_unc_under);
  HelpHisto.SetBinError(nbins, total_unc_over);

  HelpHisto.SetBinError(0,       0.0);
  HelpHisto.SetBinError(nbins+1, 0.0);

  return HelpHisto;

}

bool passBin(int nVal,  BINS Bin)
{

  bool pass = false;

  if(nVal == 0 && (Bin == v0excl || Bin == v0incl))
    return true;

  if(nVal == 1 && (Bin == v1excl || Bin == v1incl || Bin == v0incl))
    return true;

  if(nVal == 2 && (Bin == v2excl || Bin == v2incl || Bin == v1incl || Bin == v0incl))
    return true;

  if(nVal == 3 && (Bin == v3excl || Bin == v3incl || Bin == v2incl || Bin == v1incl || Bin == v0incl))
    return true;

  if(nVal == 4 && (Bin == v4excl || Bin == v4incl || Bin == v3incl || Bin == v2incl || Bin == v1incl || Bin == v0incl))
    return true;

  if(nVal == 5 && (Bin == v5excl || Bin == v5incl || Bin == v4incl || Bin == v3incl || Bin == v2incl || Bin == v1incl || Bin == v0incl))
    return true;

  if(nVal >= 6 && (Bin == v6incl || Bin == v5incl || Bin == v4incl || Bin == v3incl || Bin == v2incl || Bin == v1incl || Bin == v0incl))
    return true;

  if(Bin == vnone)
    return false;

  return pass;

}


bool passJetAndBTagBin(int nJet, int nTag, BINS JetBin, BINS BTagBin)
{
  
  bool passJet      = passBin(nJet, JetBin);
  bool passTag      = passBin(nTag, BTagBin);

  if(passTag && passJet)
    return true;
  
  return false;

}

float GetHistoUncertainty(TH1D histo, float scale)
{
  
  histo.Sumw2();
  histo.Scale(scale);

  int nbins  = histo.GetNbinsX();
  float unc2 = 0.0;

  for(int i = 1; i <= nbins; ++i){

    unc2 += histo.GetBinError(i)*histo.GetBinError(i);

  }

  float unc = sqrt(unc2);

  return unc;

}
