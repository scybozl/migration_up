#ifndef HistoCreator_H_
#define HistoCreator_H_

#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TopMass_13TeV_Plotting/EventExtras.h"
#include "TopMass_13TeV_Plotting/Enums.h"
#include "TopMass_13TeV_Plotting/ConfigClass.h"

#include "TChain.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TLorentzVector.h"

#include <utility>
#include <vector>
#include <string>

using namespace std;

class HistoCreator{

 public:

  HistoCreator(std::string, std::string, std::shared_ptr<ConfigClass>, std::string);
  virtual ~HistoCreator();

  void FillCPDistributions();

  void FillCutflowChallenge(EventExtras* iEntryExtrasInfo);
  void FillCoreHistos(EventExtras* iEntryExtrasInfo);
  void FillSmallJetsAllHistos(EventExtras* iEntryExtrasInfo,std::shared_ptr<ConfigClass> Config);
  void FillDileptonHistos(EventExtras* iEntryExtrasInfo,std::shared_ptr<ConfigClass> Config);
  void FillLepJetsHistos(EventExtras* iEntryExtrasInfo);
  void FillKLFitterHistos(EventExtras* iEntryExtrasInfo);
  void FillWeights();
  void SetScaleFactorType(std::string type){fSFType = type;};

  bool InitializeHistograms(std::string InputFileName, std::string InputFileDir);

  float CalculateLumiWeight();
 
  float GetSystWeights(std::string);


 private:

  std::vector<std::string> m_ttbarHFweights;

  std::shared_ptr<ConfigClass> gConfig;
  
  FlatTreeReader *fFlatTree;
  FlatTreeReader *fTruthTree;

  std::pair<float, int> fSampleInfo;

  float m_BTagCut,m_TopMass,m_Eff,m_Rejection;
  bool  m_Integrate,m_TopMassFix;
 
  std::vector<TH1D>        fHistoVector;
  std::vector<std::string> fHistoName;
  std::vector<std::string> fVariables;
  std::vector<std::string> fWeights;
  std::vector<double>      fTreeVariables;
  std::vector<double>      fTreeWeights;
  std::vector<Float_t>     fVar;
  std::vector<TH2D>        fCutflowHistoVector;
  std::vector<std::string> fCutflowName;
  TH2D fNtupleCutflowHisto_e;
  TH2D fNtupleCutflowHisto_mu;

  std::vector<std::string> fSetList;

  // Total Number of events read in
  int fTotalEventsRead;

  //
  int fEventSel;

  string fInputFile;
  string fOutputFile;
  string fOutputTreeFile;
  string fLeptonType;
  string fChannel;
  string fSampleType;
  string fTreeName;
  string fSampleList;
  string fAnalysisType;

  int   fDSID;
  float fLumi;
  float fTotalEventsMC;

  float fSampleXSection;
  
  float missingEtCut;
  float triangularCut;

  bool  fSplitHF;

  string fTTbarHF;

  string fUser;

  string fSFType;

  bool doTruth;

  BINS fBTagBin;
  BINS fJetBin;
  BINS fLargeJetBin;
  BINS fTopTagBin; 


};

#endif
