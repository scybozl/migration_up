#include "TopMass_13TeV_Plotting/HistoCreator.h"
#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TopMass_13TeV_Plotting/EventExtras.h"
#include "TLorentzVector.h"
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

void HistoCreator::FillDileptonHistos(EventExtras* iEntryExtrasInfo,std::shared_ptr<ConfigClass> Config)
{
  
  fSampleType = Config->GetSampleType();
  float btagdisc    = Config -> GetBTaggingCut();

  float histoweight = iEntryExtrasInfo->GetEntryWeight();
  vector<TLorentzVector> goodLeptons = iEntryExtrasInfo->GetGoodLeptons();
  int nJetCount = fFlatTree -> jet_pt  -> size();
  vector<TLorentzVector> goodJets;
  vector<TLorentzVector> goodBTags;
  vector<TLorentzVector> goodNBTags;
  goodJets.clear();
  goodBTags.clear();
  goodNBTags.clear();
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    TLorentzVector smallJet;
    smallJet.SetPtEtaPhiE(fFlatTree -> jet_pt -> at(iJet)/1000.0, fFlatTree -> jet_eta -> at(iJet), fFlatTree -> jet_phi -> at(iJet), fFlatTree -> jet_e -> at(iJet)/1000.0);
    goodJets.push_back(smallJet);
  }
  for(int iJet = 0; iJet < nJetCount; ++iJet)
    if(fFlatTree -> jet_mv2c10 -> at(iJet) > btagdisc)
      goodBTags.push_back(goodJets[iJet]);
    else
      goodNBTags.push_back(goodJets[iJet]);
  
  //Sort leptons by pT
  TLorentzVector L1;
  TLorentzVector L2;
  if(goodLeptons.at(0).Pt() >= goodLeptons.at(1).Pt()){
    L1 = goodLeptons.at(0);
    L2 = goodLeptons.at(1);
  }
  else{
    L1 = goodLeptons.at(1);
    L2 = goodLeptons.at(0);
  }

  //Find leading MV2 b-tagged jets
  TLorentzVector b1;
  TLorentzVector b2;
  int b1_index = -1;
  int b2_index = -1;
  float b1_mv2 = -1000.;
  float b2_mv2 = -1000.;
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    float current_mv2 = fFlatTree -> jet_mv2c10 -> at(iJet);
    if(current_mv2 > b1_mv2){
      b1_mv2 = current_mv2;
      b1_index = iJet;
    }
  }
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    if(iJet == b1_index) continue;
    float current_mv2 = fFlatTree -> jet_mv2c10 -> at(iJet);
    if(current_mv2 > b2_mv2){
      b2_mv2 = current_mv2;
      b2_index = iJet;
    }
  }
  if(b1_index != -1 && b2_index != -1){
    b1.SetPtEtaPhiE(fFlatTree -> jet_pt -> at(b1_index)/1000.0, 
		    fFlatTree -> jet_eta -> at(b1_index), 
		    fFlatTree -> jet_phi -> at(b1_index), 
		    fFlatTree -> jet_e -> at(b1_index)/1000.0);
    b2.SetPtEtaPhiE(fFlatTree -> jet_pt -> at(b2_index)/1000.0, 
		    fFlatTree -> jet_eta -> at(b2_index), 
		    fFlatTree -> jet_phi -> at(b2_index), 
		    fFlatTree -> jet_e -> at(b2_index)/1000.0);
  }
  /*
  //Leading pT b-tagged jets
  if(goodBTags.size() >= 2){
  b1 = goodBTags.at(0);
  b2 = goodBTags.at(1);
  }
  else {
  b1 = goodBTags.at(0);
  b2 = goodNBTags.at(0);
  }
  */

  //Pairing decision
  TLorentzVector L1b1 = L1 + b1;
  TLorentzVector L2b2 = L2 + b2;
  TLorentzVector L1b2 = L1 + b2;
  TLorentzVector L2b1 = L2 + b1;
  double avgMass1 = (L1b1.M() + L2b2.M())/2 ;
  double avgMass2 = (L1b2.M() + L2b1.M())/2 ;

  TLorentzVector LBpair1;
  TLorentzVector LBpair2;
  TLorentzVector LBpair1_reject;
  TLorentzVector LBpair2_reject;
  double LBpair_avgMass;
  double LBpair1_dR;
  double LBpair2_dR;

  if( avgMass1 <= avgMass2 ){
    LBpair1 = L1b1;
    LBpair2 = L2b2;
    LBpair1_reject = L1b2;
    LBpair2_reject = L2b1;
    LBpair_avgMass = avgMass1;
    LBpair1_dR = b1.DeltaR(L1);
    LBpair2_dR = b2.DeltaR(L2);
  }
  else{
    LBpair1 = L1b2;
    LBpair2 = L2b1;
    LBpair1_reject = L1b1;
    LBpair2_reject = L2b2;
    LBpair_avgMass = avgMass2;
    LBpair1_dR = b2.DeltaR(L1);
    LBpair2_dR = b1.DeltaR(L2);
  }

  //Alternate Pairing decision min(max)
  TLorentzVector LBpair1_maxMass;
  TLorentzVector LBpair1_minMass;
  TLorentzVector LBpair2_maxMass;
  TLorentzVector LBpair2_minMass;
  if(L1b1.M() > L2b2.M()){
    LBpair1_maxMass = L1b1;
    LBpair1_minMass = L2b2;
  }
  else{
    LBpair1_maxMass = L2b2;
    LBpair1_minMass = L1b1;
  }
  if(L1b2.M() > L2b1.M()){
    LBpair2_maxMass = L1b2;
    LBpair2_minMass = L2b1;
  }
  else{
    LBpair2_maxMass = L2b1;
    LBpair2_minMass = L1b2;
  }


  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){

    if(fVariables[iVar] == "mlb" || 
       fVariables[iVar] == "mlb_logscale"){
      fHistoVector[iVar].Fill(LBpair_avgMass, histoweight);
      fTreeVariables[iVar] = LBpair_avgMass;
    }
    else if(fVariables[iVar] == "mlb_minavg"){
      fHistoVector[iVar].Fill(LBpair_avgMass, histoweight);
      fTreeVariables[iVar] = LBpair_avgMass;
    }
    else if(fVariables[iVar] == "mlb_minavgboth"){
      fHistoVector[iVar].Fill(LBpair1.M(), histoweight);
      fTreeVariables[iVar] = LBpair1.M();
      fHistoVector[iVar].Fill(LBpair2.M(), histoweight);
      fTreeVariables[iVar] = LBpair2.M();
    }
    else if(fVariables[iVar] == "mlb_minavglow"){
      if(LBpair1.M() < LBpair2.M()){
	fHistoVector[iVar].Fill(LBpair1.M(), histoweight);
	fTreeVariables[iVar] = LBpair1.M();
      }
      else{
	fHistoVector[iVar].Fill(LBpair2.M(), histoweight);
	fTreeVariables[iVar] = LBpair2.M();
      }
    }
    else if(fVariables[iVar] == "mlb_minavghigh"){
      if(LBpair1.M() > LBpair2.M()){
	fHistoVector[iVar].Fill(LBpair1.M(), histoweight);
	fTreeVariables[iVar] = LBpair1.M();
      }
      else{
	fHistoVector[iVar].Fill(LBpair2.M(), histoweight);
	fTreeVariables[iVar] = LBpair2.M();
      }
    }
    else if(fVariables[iVar] == "mlb_minmax"){
      if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	fHistoVector[iVar].Fill(LBpair1_maxMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair1_maxMass.M();
      }
      else{
	fHistoVector[iVar].Fill(LBpair2_maxMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair2_maxMass.M();
      }
    }
    else if(fVariables[iVar] == "mlb_minmaxboth"){
      if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	fHistoVector[iVar].Fill(LBpair1_maxMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair1_maxMass.M();
	fHistoVector[iVar].Fill(LBpair1_minMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair1_minMass.M();
      }
      else{
	fHistoVector[iVar].Fill(LBpair2_maxMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair2_maxMass.M();
	fHistoVector[iVar].Fill(LBpair2_minMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair2_minMass.M();
      }
    }
    else if(fVariables[iVar] == "mlb_minmaxlow"){
      if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	fHistoVector[iVar].Fill(LBpair1_minMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair1_minMass.M();
      }
      else{
	fHistoVector[iVar].Fill(LBpair2_minMass.M(), histoweight);
	fTreeVariables[iVar] = LBpair2_minMass.M();
      }
    }
    else if(fVariables[iVar] == "mlb_minmaxavg"){
      if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	double m_avg = (LBpair1_maxMass.M() + LBpair1_minMass.M())/2;
	fHistoVector[iVar].Fill(m_avg, histoweight);
	fTreeVariables[iVar] = m_avg;
      }
      else{
	double m_avg = (LBpair2_maxMass.M() + LBpair2_minMass.M())/2;
	fHistoVector[iVar].Fill(m_avg, histoweight);
	fTreeVariables[iVar] = m_avg;
      }
    }
    else if(fVariables[iVar] == "pTlb"){
      double LBpair_avgPt = (LBpair1.Pt() + LBpair2.Pt())/2;
      fHistoVector[iVar].Fill(LBpair_avgPt, histoweight);
      fTreeVariables[iVar] = LBpair_avgPt;
    }
    else if(fVariables[iVar] == "dRlb"){
      fHistoVector[iVar].Fill(LBpair1_dR, histoweight);
      fTreeVariables[iVar] = LBpair1_dR;
      fHistoVector[iVar].Fill(LBpair2_dR, histoweight);
      fTreeVariables[iVar] = LBpair2_dR;
    }
    else if(fVariables[iVar] == "mll"){
      double mll = (L1 + L2).M();
      fHistoVector[iVar].Fill(mll, histoweight);
      fTreeVariables[iVar] = mll;
    }
    else if(fVariables[iVar] == "pTll"){
      double pTll = (L1 + L2).Pt();
      fHistoVector[iVar].Fill(pTll, histoweight);
      fTreeVariables[iVar] = pTll;
    }
    else if(fVariables[iVar] == "dRll"){
      double dRll = L1.DeltaR(L2);
      fHistoVector[iVar].Fill(dRll, histoweight);
      fTreeVariables[iVar] = dRll;
    }
    else if(fVariables[iVar] == "mbb"){
      double mbb = (b1 + b2).M();
      fHistoVector[iVar].Fill(mbb, histoweight);
      fTreeVariables[iVar] = mbb;
    }
    else if(fVariables[iVar] == "pTbb"){
      double pTbb = (b1 + b2).Pt();
      fHistoVector[iVar].Fill(pTbb, histoweight);
      fTreeVariables[iVar] = pTbb;
    }
    else if(fVariables[iVar] == "dRbb"){
      double dRbb = b1.DeltaR(b2);
      fHistoVector[iVar].Fill(dRbb, histoweight);
      fTreeVariables[iVar] = dRbb;
    }
    else if(fVariables[iVar] == "Rbq"){
      double Rbq = -1;
      if(goodNBTags.size() > 0){
	double sumPt_b = 0;
	double sumPt_nb = 0;
	for(int i = 0; i < (int)goodBTags.size(); ++i)
	  sumPt_b += goodBTags.at(i).Pt();
	for(int i = 0; i < (int)goodNBTags.size(); ++i)
	  sumPt_nb += goodNBTags.at(i).Pt();

	Rbq = (sumPt_b/goodBTags.size())/(sumPt_nb/goodNBTags.size());
      }
      fHistoVector[iVar].Fill(Rbq, histoweight);
      fTreeVariables[iVar] = Rbq;
    }
    else if(fVariables[iVar] == "Rbq_1B1L_closestPt"){
      double Rbq = -1;
      if(goodNBTags.size() > 0 && goodBTags.size() == 1){
	double bjetPt = goodBTags.at(0).Pt();
	double closestPt = -1000;
	double bestDiff = fabs(bjetPt - closestPt);
	for(int i = 0; i < (int)goodNBTags.size(); ++i){
	  double currentDiff = fabs(bjetPt - goodNBTags.at(i).Pt());
	  if(currentDiff < bestDiff){
	    closestPt = goodNBTags.at(i).Pt();
	    bestDiff = currentDiff;
	  }
	}
	Rbq = bjetPt/closestPt;
      }
      fHistoVector[iVar].Fill(Rbq, histoweight);
      fTreeVariables[iVar] = Rbq;
    }
    else if(fVariables[iVar] == "Rbq_1B1L_closestPt_alt"){
      double Rbq = -1;
      if(goodNBTags.size() > 1 && goodBTags.size() == 1){
	double bjetPt = goodBTags.at(0).Pt();
	double closestPt = -1000;
	double bestDiff = fabs(bjetPt - closestPt);
	for(int iJet = 0; iJet < nJetCount; ++iJet){
	  if(iJet == b1_index || iJet == b2_index) continue;
	  double currentDiff = fabs(bjetPt - goodJets.at(iJet).Pt());
	  if(currentDiff < bestDiff){
	    closestPt = goodJets.at(iJet).Pt();
	    bestDiff = currentDiff;
	  }
	}
	Rbq = bjetPt/closestPt;
      }
      fHistoVector[iVar].Fill(Rbq, histoweight);
      fTreeVariables[iVar] = Rbq;
    }
    else if(fVariables[iVar] == "Rbq_1B1L_smallestMV2c10"){
      double Rbq = -1;
      if(goodNBTags.size() > 0 && goodBTags.size() == 1){
	double bjetPt = goodBTags.at(0).Pt();
	float smallest_mv2 = 9999999.;
	int smallest_mv2_index = -1;
	for(int iJet = 0; iJet < nJetCount; ++iJet){
	  float current_mv2 = fFlatTree -> jet_mv2c10 -> at(iJet);
	  if(current_mv2 < smallest_mv2){
	    smallest_mv2 = current_mv2;
	    smallest_mv2_index = iJet;
	  }
	}
	Rbq = bjetPt/(fFlatTree -> jet_pt -> at(smallest_mv2_index)/1000.0);
      }
      fHistoVector[iVar].Fill(Rbq, histoweight);
      fTreeVariables[iVar] = Rbq;
    }
    else if(fVariables[iVar] == "Rbq_1B1L_smallestMV2c10_alt"){
      double Rbq = -1;
      if(goodNBTags.size() > 1 && goodBTags.size() == 1){
	double bjetPt = goodBTags.at(0).Pt();
	float smallest_mv2 = 9999999.;
	int smallest_mv2_index = -1;
	for(int iJet = 0; iJet < nJetCount; ++iJet){
	  if(iJet == b1_index || iJet == b2_index) continue;
	  float current_mv2 = fFlatTree -> jet_mv2c10 -> at(iJet);
	  if(current_mv2 < smallest_mv2){
	    smallest_mv2 = current_mv2;
	    smallest_mv2_index = iJet;
	  }
	}
	Rbq = bjetPt/goodJets.at(smallest_mv2_index).Pt();
      }
      fHistoVector[iVar].Fill(Rbq, histoweight);
      fTreeVariables[iVar] = Rbq;
    }
    else if(fVariables[iVar] == "bjet1_pT"){
      fHistoVector[iVar].Fill(b1.Pt(), histoweight);
      fTreeVariables[iVar] = b1.Pt();
    }
    else if(fVariables[iVar] == "bjet1_eta"){
      fHistoVector[iVar].Fill(b1.Eta(), histoweight);
      fTreeVariables[iVar] = b1.Eta();
    }
    else if(fVariables[iVar] == "bjet1_phi"){
      fHistoVector[iVar].Fill(b1.Phi(), histoweight);
      fTreeVariables[iVar] = b1.Phi();
    }
    else if(fVariables[iVar] == "bjet1_mv2c10"){
      fHistoVector[iVar].Fill(b1_mv2, histoweight);
      fTreeVariables[iVar] = b1_mv2;
    }
    else if(fVariables[iVar] == "bjet1_truthflav"){
      if(fSampleType=="MC"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_truthflav -> at(b1_index), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_truthflav -> at(b1_index);
      }
      else{
	fHistoVector[iVar].Fill(-1, histoweight);
	fTreeVariables[iVar] = -1;
      }
    }
    else if(fVariables[iVar] == "bjet2_pT"){
      fHistoVector[iVar].Fill(b2.Pt(), histoweight);
      fTreeVariables[iVar] = b2.Pt();
    }
    else if(fVariables[iVar] == "bjet2_eta"){
      fHistoVector[iVar].Fill(b2.Eta(), histoweight);
      fTreeVariables[iVar] = b2.Eta();
    }
    else if(fVariables[iVar] == "bjet2_phi"){
      fHistoVector[iVar].Fill(b2.Phi(), histoweight);
      fTreeVariables[iVar] = b2.Phi();
    }
    else if(fVariables[iVar] == "bjet2_mv2c10"){
      fHistoVector[iVar].Fill(b2_mv2, histoweight);
      fTreeVariables[iVar] = b2_mv2;
    }
    else if(fVariables[iVar] == "bjet2_truthflav"){
      if(fSampleType=="MC"){
	fHistoVector[iVar].Fill(fFlatTree -> jet_truthflav -> at(b2_index), histoweight);
	fTreeVariables[iVar] = fFlatTree -> jet_truthflav -> at(b2_index);
      }
      else{
	fHistoVector[iVar].Fill(-1, histoweight);
	fTreeVariables[iVar] = -1;
      }
    }
    else if(fVariables[iVar] == "lep1_pT"){
      fHistoVector[iVar].Fill(L1.Pt(), histoweight);
      fTreeVariables[iVar] = L1.Pt();
    }
    else if(fVariables[iVar] == "lep1_eta"){
      fHistoVector[iVar].Fill(L1.Eta(), histoweight);
      fTreeVariables[iVar] = L1.Eta();
    }
    else if(fVariables[iVar] == "lep1_phi"){
      fHistoVector[iVar].Fill(L1.Phi(), histoweight);
      fTreeVariables[iVar] = L1.Phi();
    }
    else if(fVariables[iVar] == "lep2_pT"){
      fHistoVector[iVar].Fill(L2.Pt(), histoweight);
      fTreeVariables[iVar] = L2.Pt();
    }
    else if(fVariables[iVar] == "lep2_eta"){
      fHistoVector[iVar].Fill(L2.Eta(), histoweight);
      fTreeVariables[iVar] = L2.Eta();
    }
    else if(fVariables[iVar] == "lep2_phi"){
      fHistoVector[iVar].Fill(L2.Phi(), histoweight);
      fTreeVariables[iVar] = L2.Phi();
    }
    
        
  }
}

