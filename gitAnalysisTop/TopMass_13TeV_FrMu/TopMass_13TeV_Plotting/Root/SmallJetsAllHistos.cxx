#include "TopMass_13TeV_Plotting/HistoCreator.h"
#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TopMass_13TeV_Plotting/EventExtras.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>
#ifdef __MAKECINT__
#pragma link C++ class std::vector<std::vector<int> >* +;
#endif

void HistoCreator::FillSmallJetsAllHistos(EventExtras* iEntryExtrasInfo,std::shared_ptr<ConfigClass> Config)
{
  
  float histoweight = iEntryExtrasInfo->GetEntryWeight();
  int nJetCount = iEntryExtrasInfo->GetNJetsAll();

  gConfig = Config;
  fSampleType = gConfig->GetSampleType();
  
  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){

    if(fVariables[iVar] == "jet_pt"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(iJet)/1000.0, histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(iJet)/1000.0;
      }
    }
    else if(fVariables[iVar] == "jet_eta"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	fHistoVector[iVar].Fill(fFlatTree -> jet_eta  -> at(iJet), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_eta  -> at(iJet);
      }
    }
    else if(fVariables[iVar] == "jet_phi"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	fHistoVector[iVar].Fill(fFlatTree -> jet_phi  -> at(iJet), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_phi  -> at(iJet);
      }
    }
    else if(fVariables[iVar] == "jet_jvt"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	fHistoVector[iVar].Fill(fFlatTree -> jet_jvt  -> at(iJet), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_jvt  -> at(iJet);
      }
    }
    else if(fVariables[iVar] == "jet_mv2c10"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	fHistoVector[iVar].Fill(fFlatTree -> jet_mv2c10  -> at(iJet), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_mv2c10  -> at(iJet);
      }
    }
    else if(fVariables[iVar] == "jet_truthflav"){
      for(int iJet = 0; iJet < nJetCount; ++iJet){
	if(fSampleType=="MC"){
	  fHistoVector[iVar].Fill(fFlatTree -> jet_truthflav  -> at(iJet), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> jet_truthflav  -> at(iJet);
	}
	else{
	  fHistoVector[iVar].Fill(-1, histoweight);
	  fTreeVariables[iVar] = -1;
	}
      }
    }

    if(nJetCount > 0){
      if(fVariables[iVar] == "jet0_pt"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(0)/1000.0, histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(0)/1000.0;
      }
      else if(fVariables[iVar] == "jet0_eta"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_eta -> at(0), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_eta -> at(0);
      }
      else if(fVariables[iVar] == "jet0_phi"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_phi -> at(0), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_phi -> at(0);
      }
    }
    if(nJetCount > 1){
      if(fVariables[iVar] == "jet1_pt"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(1)/1000.0, histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(1)/1000.0;
      }
      else if(fVariables[iVar] == "jet1_eta"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_eta -> at(1), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_eta -> at(1);
      }
      else if(fVariables[iVar] == "jet1_phi"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_phi -> at(1), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_phi -> at(1);
      }
    }
    if(nJetCount > 2){
      if(fVariables[iVar] == "jet2_pt"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(2)/1000.0, histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(2)/1000.0;
      }
      else if(fVariables[iVar] == "jet2_eta"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_eta -> at(2), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_eta -> at(2);
      }
      else if(fVariables[iVar] == "jet2_phi"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_phi -> at(2), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_phi -> at(2);
      }
    }
    if(nJetCount > 3){
      if(fVariables[iVar] == "jet3_pt"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(3)/1000.0, histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(3)/1000.0;
      }
      else if(fVariables[iVar] == "jet3_eta"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_eta -> at(3), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_eta -> at(3);
      }
      else if(fVariables[iVar] == "jet3_phi"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_phi -> at(3), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_phi -> at(3);
      }
    }
    if(nJetCount > 4){
      if(fVariables[iVar] == "jet4_pt"){
        fHistoVector[iVar].Fill(fFlatTree -> jet_pt  -> at(4)/1000.0, histoweight);
        fTreeVariables[iVar] = fFlatTree -> jet_pt  -> at(4)/1000.0;
      }
      else if(fVariables[iVar] == "jet4_eta"){
        fHistoVector[iVar].Fill(fFlatTree -> jet_eta -> at(4), histoweight);
        fTreeVariables[iVar] = fFlatTree -> jet_eta -> at(4);
      }
      else if(fVariables[iVar] == "jet4_phi"){
        fHistoVector[iVar].Fill(fFlatTree -> jet_phi -> at(4), histoweight);
        fTreeVariables[iVar] = fFlatTree -> jet_phi -> at(4);
      }
    }



  }
  
}


