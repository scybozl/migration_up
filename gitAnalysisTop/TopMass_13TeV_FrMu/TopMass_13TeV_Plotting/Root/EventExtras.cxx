#include "TopMass_13TeV_Plotting/EventExtras.h"
#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TLorentzVector.h"
#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <math.h>
#include <stdio.h>

using namespace std;


EventExtras::EventExtras(int EventIndex, FlatTreeReader *FlatTree, std::shared_ptr<ConfigClass> Config){

  m_eventIndex=EventIndex;
  m_flattree=FlatTree;
  m_flattree -> fChain -> GetEntry(m_eventIndex);

  min_largejetpt  = Config -> GetMinLargeRJetPt();
  matchingdR      = Config -> GetMatchingDR();
  btagdisc        = Config -> GetBTaggingCut();
  btagdisc_loose  = Config -> GetBTaggingCutLoose();
  loose_b_tagging = Config -> GetUseLooseBTagging();
  
  fAnalysisType = Config -> GetAnalysisType();
  
  if(fAnalysisType == "dilepton")
    leadleppt       = 25;
  else
    leadleppt       = Config -> GetLeadingLeptonPt();

  int nJetCount   = m_flattree -> jet_pt  -> size();

  // count number of small jets
  vector<TLorentzVector> GoodSmallJets;
  GoodSmallJets.clear();
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    TLorentzVector smallJet;
    smallJet.SetPtEtaPhiE(m_flattree -> jet_pt -> at(iJet)/1000.0, m_flattree -> jet_eta -> at(iJet), m_flattree -> jet_phi -> at(iJet), m_flattree -> jet_e -> at(iJet)/1000.0);
    GoodSmallJets.push_back(smallJet);
  }

  // count number of b-tagged jets
  vector<TLorentzVector> GoodSmallBTags;
  GoodSmallBTags.clear();
  int nTagCount = 0;
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    if(m_flattree -> jet_mv2c10 -> at(iJet) > btagdisc){
      GoodSmallBTags.push_back(GoodSmallJets[iJet]);
      nTagCount++;
    }
  }

  // count number of non b-tagged jets
  vector<TLorentzVector> GoodSmallNBTags;
  GoodSmallNBTags.clear();
  int nNTagCount = 0;
  for(int iJet = 0; iJet < nJetCount; ++iJet){
    if(m_flattree -> jet_mv2c10 -> at(iJet) <= btagdisc){
      GoodSmallNBTags.push_back(GoodSmallJets[iJet]);
      nNTagCount++;
    }
  }

  // count number of leptons
  int mu_n = m_flattree->mu_pt->size();
  int el_n = m_flattree->el_pt->size();

  // Define good lepton
  vector<TLorentzVector> GoodLeptons;
  GoodLeptons.clear();
  TLorentzVector goodLepton;
  int ngoodleptons = 0;
  bool isEl    = false;
  bool isMu    = false;
  char isTight = -1;
  float goodLeptonCharge = 0;

  for( int electron = 0; electron < el_n; ++electron){
    TLorentzVector el;
    el.SetPtEtaPhiE(m_flattree->el_pt-> at(electron)/1000., m_flattree->el_eta->at(electron), m_flattree->el_phi->at(electron), m_flattree->el_e-> at(electron)/1000.);

    float charge = m_flattree -> el_charge  -> at(electron);
    //char tight    = m_flattree -> el_isTight -> at(electron);

    if(el.Pt() > leadleppt){
      GoodLeptons.push_back(el);
      goodLepton = el;
      ngoodleptons++;
      isEl = true;

      goodLeptonCharge = charge;
      //isTight          = tight;
    }
  }
  for( int muon = 0; muon < mu_n; ++muon){

    TLorentzVector mu;
    mu.SetPtEtaPhiE(m_flattree->mu_pt-> at(muon)/1000., m_flattree->mu_eta->at(muon), m_flattree->mu_phi->at(muon), m_flattree->mu_e-> at(muon)/1000.);

    //std::cout <<  m_flattree -> mu_charge  -> size() << "\t" << m_flattree -> mu_isTight -> size() << std::endl;

    float charge = m_flattree -> mu_charge  -> at(muon);
    //char  tight  = m_flattree -> mu_isTight -> at(muon);

    if (mu.Pt() > leadleppt){
      GoodLeptons.push_back(mu);
      goodLepton = mu;
      ngoodleptons++;
      isMu = true;

      goodLeptonCharge = charge;
      //isTight          = tight;
    }
  }

  if(ngoodleptons > 1 && fAnalysisType == "lepjets"){ 

    cout << ngoodleptons << endl;

    cout << "WARNING: More than one good lepton in the event!" << endl; exit(0);


  }

  m_nJets_all=nJetCount;
  m_nBTags_all=nTagCount;

  m_GoodSmallJets.clear();
  m_GoodSmallJets=GoodSmallJets;

  m_GoodSmallBTags.clear();
  m_GoodSmallBTags=GoodSmallBTags;
  
  m_GoodSmallNBTags.clear();
  m_GoodSmallNBTags=GoodSmallNBTags;
  
  m_GoodLeptons.clear();
  m_GoodLeptons=GoodLeptons;

  m_mu_n = mu_n;
  m_el_n = el_n;

  m_GoodLepton = goodLepton;
  m_isMu = isMu;
  m_isEl = isEl;
  m_LeptonIsTight    = isTight;
  m_GoodLeptonCharge = goodLeptonCharge;

}

EventExtras::EventExtras()
{

}

EventExtras::~EventExtras()
{

}
