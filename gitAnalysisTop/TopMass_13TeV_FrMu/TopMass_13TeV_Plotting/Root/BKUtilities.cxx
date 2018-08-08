#include "TopMass_13TeV_Plotting/BKUtilities.h"
#include "TopMass_13TeV_Plotting/StatusLogbook.h"

#include "TChain.h"

#include "TFile.h"
#include "TTree.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TH1D.h"
#include "TMath.h"

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

#include <glob.h>

double deltaPhi(float phi1, float phi2){double dphi = TMath::Abs(phi1-phi2); return (dphi > TMath::Pi()) ? dphi-TMath::TwoPi() : dphi;}

std::vector<std::string> GetFileList(std::string SampleList)
{

  std::vector<std::string> list;

  std::ifstream fFile;

  fFile.open(SampleList.c_str(), std::ios::in);

  std::string line;

  while(!fFile.eof()){

    getline(fFile, line);

    if (line.find(".root") != std::string::npos)
      list.push_back(line);

  }

  return list;

}



TChain* ChainFiles(std::string chain_name, std::string InputFolder)
{

  TChain *fChain = new TChain(chain_name.c_str());

  glob_t glob_result;
  glob((InputFolder+"/*root*").c_str(), GLOB_TILDE, NULL, &glob_result);

  for(unsigned int i = 0; i < glob_result.gl_pathc; ++i){

    fChain   -> Add(glob_result.gl_pathv[i]);

  }

  return fChain;

}

TH2D MakeNtupleCutflow(std::vector<std::string> listFiles, std::string Channel)
{

  int nFiles  = listFiles.size();

  TH1D* temp_1D_noWeights =0;
  TH1D* temp_1D_mcWeights =0;
  TH1D* temp_1D_allWeights =0;
  std::string cfname = "NtupleCutflow"+Channel;
  if(Channel == "ejets_2015" || Channel == "boosted_ejets_2015" || Channel == "ejets_2016" || Channel == "boosted_ejets_2016") cfname = "NtupleCutflow_ejets";
  if(Channel == "mujets_2015" || Channel == "boosted_mujets_2015" || Channel == "mujets_2016" || Channel == "boosted_mujets_2016") cfname = "NtupleCutflow_mujets";

  for(int iFile = 0; iFile < nFiles; ++iFile){
    TFile *fFile  = TFile::Open(listFiles[iFile].c_str());
        
    TH1D  *noWeightsHist  = (TH1D*) fFile -> Get((Channel+"/cutflow").c_str());
    TH1D  *mcWeightsHist  = (TH1D*) fFile -> Get((Channel+"/cutflow_mc").c_str());
    TH1D  *allWeightsHist  = (TH1D*) fFile -> Get((Channel+"/cutflow_mc_pu_zvtx").c_str());

    if(iFile == 0) temp_1D_noWeights = (TH1D*)noWeightsHist->Clone();
    else temp_1D_noWeights->Add(noWeightsHist);
    if(iFile == 0) temp_1D_mcWeights = (TH1D*)mcWeightsHist->Clone();
    else temp_1D_mcWeights->Add(mcWeightsHist);
    if(iFile == 0) temp_1D_allWeights = (TH1D*)allWeightsHist->Clone();
    else temp_1D_allWeights->Add(allWeightsHist);

  }

  TH2D temp_2D = TH2D(cfname.c_str(), cfname.c_str(), temp_1D_noWeights->GetNbinsX(), 0.5, temp_1D_noWeights->GetNbinsX()+0.5, 3, 0.5, 3.5);

  for(int ibin = 0; ibin<temp_1D_noWeights->GetNbinsX(); ibin++){

    temp_2D.SetBinContent(ibin+1,1,temp_1D_noWeights->GetBinContent(ibin+1));
    temp_2D.SetBinContent(ibin+1,2,temp_1D_mcWeights->GetBinContent(ibin+1));
    temp_2D.SetBinContent(ibin+1,3,temp_1D_allWeights->GetBinContent(ibin+1));
    temp_2D.GetXaxis()->SetBinLabel(ibin+1,temp_1D_noWeights->GetXaxis()->GetBinLabel(ibin+1));

  }

   
  return temp_2D ;
}

std::pair<float, int> CalculateTotalEventNumberHisto(std::vector<std::string> listFiles, TChain *BKTree, std::string Channel)
{

  std::pair<float, int> info;

  info.first  = 0;
  info.second = 0;

  int   dsid;
  BKTree -> SetBranchAddress("dsid", &dsid);
  BKTree -> GetEntry(0);
  info.second = dsid;

  int nFiles  = listFiles.size();

  for(int iFile = 0; iFile < nFiles; ++iFile){

    // open input file                                                                                                                                                                                        
    TFile *fFile  = TFile::Open(listFiles[iFile].c_str());

    if(Channel=="emujets_2015" or Channel == "emujets_2016" or Channel == "emujets_comb") Channel = "ejets_2016";
    if(Channel=="ll_2015" or Channel == "ll_2016" or Channel == "ll_comb") Channel = "ejets_2016";

    TH1D  *fHist  = (TH1D*) fFile -> Get((Channel+"/cutflow_mc_pu_zvtx").c_str());
    float NEvents = fHist -> GetBinContent(1);

    info.first   += NEvents;

  }

  return info;

}

std::pair<float, int> CalculateTotalEventNumberTree(TChain *BKTree)
{

  std::pair<float, int> info;

  info.first  = 0;
  info.second = 0;

  int nevents = BKTree -> GetEntries();

  int   dsid;
  float TotalEW;

  BKTree -> SetBranchAddress("dsid",                &dsid);
  BKTree -> SetBranchAddress("totalEventsWeighted", &TotalEW);

  for(int ientry = 0; ientry < nevents; ++ientry){

    BKTree -> GetEntry(ientry);

    info.first  += TotalEW;
    info.second  = dsid;

  }

  return info;

}
