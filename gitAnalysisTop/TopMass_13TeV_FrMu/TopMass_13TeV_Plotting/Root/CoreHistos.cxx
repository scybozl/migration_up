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
using namespace std;

void HistoCreator::FillCoreHistos(EventExtras* iEntryExtrasInfo)
{
  
  float histoweight = iEntryExtrasInfo->GetEntryWeight();
  TLorentzVector goodLepton = iEntryExtrasInfo->GetGoodLepton();
  string fAnalysisType = iEntryExtrasInfo->GetfAnalysisType();

  int mu_n = fFlatTree -> mu_pt -> size();
  int el_n = fFlatTree -> el_pt -> size();
 
  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){

    if (fVariables[iVar] == "nEvents"){
      fHistoVector[iVar].Fill(1, histoweight);
      fTreeVariables[iVar] = histoweight;
    } 
    else if(fVariables[iVar] == "nBTags"){    
      fHistoVector[iVar].Fill(iEntryExtrasInfo->GetNBTagsAll(), histoweight);
      fTreeVariables[iVar] = iEntryExtrasInfo->GetNBTagsAll();
    }
    else if(fVariables[iVar] == "jet_n"){
      fHistoVector[iVar].Fill(iEntryExtrasInfo->GetNJetsAll(), histoweight);
      fTreeVariables[iVar] = iEntryExtrasInfo->GetNJetsAll();
    }
    else if(fVariables[iVar] == "met_met"){
      fHistoVector[iVar].Fill(fFlatTree -> met_met/1000.0, histoweight);
      fTreeVariables[iVar] = fFlatTree -> met_met/1000.0;
    }
    else if(fVariables[iVar] == "met_phi"){
      fHistoVector[iVar].Fill(fFlatTree -> met_phi, histoweight);
      fTreeVariables[iVar] = fFlatTree -> met_phi;
    }
    else if(fVariables[iVar] == "mu_n"){

      float lepPtCut = iEntryExtrasInfo -> GetLeptonPtCut();

      int counter = 0;

      for(int iMu = 0; iMu < mu_n; ++iMu){
	
	if(fFlatTree -> mu_pt -> at(iMu)/1000.0 > lepPtCut)
	  counter++;
      }

      fHistoVector[iVar].Fill(counter, histoweight);
      fTreeVariables[iVar] = counter;
    }
    else if(fVariables[iVar] == "el_n"){

      float lepPtCut = iEntryExtrasInfo -> GetLeptonPtCut();

      int counter = 0;

      for(int iEl = 0; iEl < el_n; ++iEl){
	if(fFlatTree -> el_pt -> at(iEl)/1000.0 > lepPtCut)
	  counter++;
      }

      fHistoVector[iVar].Fill(counter, histoweight);
      fTreeVariables[iVar] = counter;
    }

    float lepPtCut = iEntryExtrasInfo -> GetLeptonPtCut();

    for(int iMu = 0; iMu < mu_n; ++iMu){
      if(fVariables[iVar] == "mu_pt"){
	if(fFlatTree -> mu_pt -> at(iMu)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> mu_pt -> at(iMu)/1000.0, histoweight);
	  fTreeVariables[iVar] = fFlatTree -> mu_pt -> at(iMu)/1000.0;
	}
      }
      else if(fVariables[iVar] == "mu_eta"){
	if(fFlatTree -> mu_pt -> at(iMu)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> mu_eta -> at(iMu), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> mu_eta -> at(iMu);
	}
      }
      else if(fVariables[iVar] == "mu_phi"){
	if(fFlatTree -> mu_pt -> at(iMu)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> mu_phi -> at(iMu), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> mu_phi -> at(iMu);
	}
      }
      else if(fVariables[iVar] == "mu_charge"){
	if(fFlatTree -> mu_pt -> at(iMu)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> mu_charge -> at(iMu), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> mu_charge -> at(iMu);
	}
      }
    }
    for(int iEl = 0; iEl < el_n; ++iEl){
      if(fVariables[iVar] == "el_pt"){
	if(fFlatTree -> el_pt -> at(iEl)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> el_pt -> at(iEl)/1000.0, histoweight);
	  fTreeVariables[iVar] = fFlatTree -> el_pt -> at(iEl)/1000.0;
	}
      }
      else if(fVariables[iVar] == "el_eta"){
	if(fFlatTree -> el_pt -> at(iEl)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> el_eta -> at(iEl), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> el_eta -> at(iEl);
	}
      }
      else if(fVariables[iVar] == "el_phi"){
	if(fFlatTree -> el_pt -> at(iEl)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> el_phi -> at(iEl), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> el_phi -> at(iEl);
	}
      }
      else if(fVariables[iVar] == "el_charge"){
	if(fFlatTree -> el_pt -> at(iEl)/1000.0 > lepPtCut){
	  fHistoVector[iVar].Fill(fFlatTree -> el_charge -> at(iEl), histoweight);
	  fTreeVariables[iVar] = fFlatTree -> el_charge -> at(iEl);
	}
      }
    }
        
  }
}


