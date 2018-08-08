#ifndef EventExtras_H_
#define EventExtras_H_

#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TopMass_13TeV_Plotting/ConfigClass.h"

#include "TLorentzVector.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>

class EventExtras{

 public:

  EventExtras();
  EventExtras(int EventIndex,FlatTreeReader *FlatTree, std::shared_ptr<ConfigClass> Config);
  virtual ~EventExtras();

  void SetEventIndex(int EventIndex){m_eventIndex=EventIndex;};
  void SetNJetsAll(int NJetsAll){m_nJets_all=NJetsAll;};
  void SetNBTagsAll(int NBTagsAll){m_nBTags_all=NBTagsAll;};
  void SetEntryWeight(float EntryWeight){m_entryWeight=EntryWeight;};
  void SetEntryLumiWeight(float EntryLumiWeight){m_entryLumiWeight=EntryLumiWeight;};
  void SetPassTTBarXSec(bool passselection){m_passTTBarXSec = passselection;};

  int GetEventIndex(){ return m_eventIndex;};

  int GetNJetsAll(){ return m_nJets_all;};
  int GetNBTagsAll(){ return m_nBTags_all;};
  float GetEntryWeight(){ return m_entryWeight;};
  float GetEntryLumiWeight(){ return m_entryLumiWeight;};
  float GetMissingEtCut(){return m_missingEtCut;};
  float GetTriangularCut(){return m_triangularCut;};
  float GetLeptonPtCut(){return leadleppt;};

  std::vector<TLorentzVector> GetGoodSmallJets(){ return m_GoodSmallJets;};
  std::vector<TLorentzVector> GetGoodSmallTags(){ return m_GoodSmallBTags;};
  std::vector<TLorentzVector> GetGoodSmallNBTags(){ return m_GoodSmallNBTags;};
  std::vector<TLorentzVector> GetGoodLeptons(){ return m_GoodLeptons;};
  std::string GetfAnalysisType(){ return fAnalysisType;};

  int GetNMu() {return m_mu_n;};
  int GetNEl() {return m_el_n;};
  bool IsMu() {return m_isMu;};
  bool IsEl() {return m_isEl;};
  bool GetPassTTBarXSec() {return m_passTTBarXSec;};
  TLorentzVector GetGoodLepton() { return m_GoodLepton;} ;
  TLorentzVector GetNeutrino() { return m_nu;} ;
  TLorentzVector GetWBoson()   { return m_Wboson;} ;
  TLorentzVector GetLepTop()   { return m_leptop;} ;
  TLorentzVector GetHadTop()   { return m_hadtop;} ;
  TLorentzVector GetTTBar()    { return m_ttbar;} ;

  int GetGoodLeptonCharge(){return m_GoodLeptonCharge;};
  char GetGoodLeptonIsTight(){return m_LeptonIsTight;};

 private:

  char m_LeptonIsTight;
  int m_GoodLeptonCharge;

  int m_eventIndex;
  int m_nJets_all;
  int m_nBTags_all;
  
  int m_mu_n;
  int m_el_n;
  bool m_isMu;
  bool m_isEl;
  bool m_passTTBarXSec;
  float m_entryWeight;
  float m_entryLumiWeight;
  float m_dR_l_jet;

  FlatTreeReader *m_flattree;
  std::vector<TLorentzVector> m_GoodLJets;
  std::vector<int> m_GoodLJetIndex;
  std::vector<int> m_TopTagLooseJetIndex;
  std::vector<TLorentzVector> m_GoodSmallJets;
  std::vector<TLorentzVector> m_GoodSmallBTags;
  std::vector<TLorentzVector> m_GoodSmallNBTags;
  std::vector<TLorentzVector> m_GoodLeptons;

  TLorentzVector m_GoodLepton;
  TLorentzVector m_nu;
  TLorentzVector m_Wboson;
  TLorentzVector m_leptop;
  TLorentzVector m_hadtop;
  TLorentzVector m_ttbar;

  float min_largejetpt;
  float matchingdR;
  float max_largejetpt = 1500.0;
  float largejetmass   =   50.0;
  float largejeteta    =    2.0;
  float btagdisc;
  float btagdisc_loose;
  float leadleppt;
  float m_missingEtCut;
  float m_triangularCut;
  int loose_b_tagging;
  std::string fAnalysisType;

};

#endif
