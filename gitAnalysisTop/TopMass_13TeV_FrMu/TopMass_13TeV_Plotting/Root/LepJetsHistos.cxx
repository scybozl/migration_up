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

void HistoCreator::FillLepJetsHistos(EventExtras* iEntryExtrasInfo)
{
  
  float histoweight = iEntryExtrasInfo->GetEntryWeight();
  TLorentzVector goodLepton = iEntryExtrasInfo->GetGoodLepton();
  
  double met = fFlatTree -> met_met/1000.0;
  double dPhi = goodLepton.Phi() - fFlatTree -> met_phi;
  if (dPhi > 3.142) dPhi = 6.28 - dPhi;
  if (dPhi < - 3.142) dPhi = -6.28 - dPhi;
  double dPhiAbs = fabs(dPhi);
  double mtw = sqrt(2*goodLepton.Pt()*met*(1-cos(dPhi)));
  
  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){
    
    if(fVariables[iVar] == "mtw") {
      fHistoVector[iVar].Fill(mtw, histoweight);
      fTreeVariables[iVar] = mtw;
    }
    else if(fVariables[iVar] == "mtw_extended") {
      fHistoVector[iVar].Fill(mtw, histoweight);
      fTreeVariables[iVar] = mtw;
    } 
    else if(fVariables[iVar] == "met_plus_mtw") {
      fHistoVector[iVar].Fill(met+mtw, histoweight);
      fTreeVariables[iVar] = met+mtw;
    }
    else if(fVariables[iVar] == "dphi_lep_met"){
      fHistoVector[iVar].Fill(dPhi, histoweight);
      fTreeVariables[iVar] = dPhi;
    }
    else if(fVariables[iVar] == "dphi_lep_met_abs"){
      fHistoVector[iVar].Fill(dPhiAbs, histoweight);
      fTreeVariables[iVar] = dPhiAbs;
    }
    
  }
}


