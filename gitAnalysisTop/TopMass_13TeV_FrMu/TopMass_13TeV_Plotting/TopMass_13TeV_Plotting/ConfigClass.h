#ifndef CONFIGCLASS_H
#define CONFIGCLASS_H

#include "TopMass_13TeV_Plotting/Enums.h"

#include <memory>
#include <string>
#include <vector>
#include <set>
#include <list>
#include <iostream>

class ConfigClass {

 public:

  ConfigClass();
  virtual ~ConfigClass(){}

  void readSettingsFromConfig(std::string);

  int GetDSID(){return m_DSID;};
  
  float GetLumi(){return m_lumiValue;};
  float GetMinLargeRJetPt(){return m_minLargeRJetPt;};
  float GetMatchingDR(){return m_matchingDR;};
  float GetBTaggingCut(){return m_btaggingCut;};
  float GetBTaggingCutLoose(){return m_btaggingCutLoose;};
  float GetLeadingLeptonPt(){return m_leadingLeptonPt;};
  float GetMissingEtCut(){return m_missingEtCut;};
  float GetTriangularCut(){return m_triangularCut;};
  float GetLumiLabel(){return m_lumiLabel;};
  
  bool  GetUseLooseBTagging(){return m_useLooseBTagging;}; 
  bool  GetUseHFSplitting(){return m_useHFSplitting;};
  
  std::string GetConfigFileVariables(){return m_fileVariables;};
  std::string GetLeptonChannel(){return m_leptonChannel;};
  std::string GetAnalysisType(){return m_analysisType;};
  std::string GetHFType(){return m_hfType;};
  std::string GetInputName(){return m_inputFile;};
  std::string GetOutputName(){return m_outputFile;};
  std::string GetOutputTreeName(){return m_outputTreeFile;};
  std::string GetLeptonType(){return m_leptonType;};
  std::string GetChannel(){return m_leptonChannel;};
  std::string GetSampleType(){return m_sampleType;};
  std::string GetDataLabel(){return m_dataLabel;};

  BINS GetBTagBin(){return m_BTagBin;};
  BINS GetJetBin(){return m_JetBin;};
  BINS GetLargeJetBin(){return m_LargeJetBin;};
  BINS GetTopTagBin(){return m_TopTagBin;};
  BINS GetVetoBTagBin(){return m_VetoBTagBin;};
  BINS GetVetoJetBin(){return m_VetoJetBin;};
  BINS GetVetoLargeJetBin(){return m_VetoLargeJetBin;};
  BINS GetVetoTopTagBin(){return m_VetoTopTagBin;};

  // some of the settings are not defined by the config file but set "by hand"

  void SetHFType(std::string value){m_hfType = value;};
  void SetLargeJetBin(BINS JetBin){m_LargeJetBin = JetBin;};
  void SetTopTagBin(BINS JetBin){m_TopTagBin = JetBin;};
  void SetJetBin(BINS JetBin){m_JetBin = JetBin;};
  void SetNumberOfBTags(BINS nr){m_BTagBin = nr;};
  void SetVetoLargeJetBin(BINS JetBin){m_VetoLargeJetBin = JetBin;};
  void SetVetoTopTagBin(BINS JetBin){m_VetoTopTagBin = JetBin;};
  void SetVetoJetBin(BINS JetBin){m_VetoJetBin = JetBin;};
  void SetVetoNumberOfBTags(BINS nr){m_VetoBTagBin = nr;};
  void SetInputFile(std::string value){m_inputFile = value;};
  void SetSampleType(std::string value){m_sampleType = value;};
  void SetOutputFile(std::string value){m_outputFile = value;};
  void SetOutputTreeFile(std::string value){m_outputTreeFile = value;};
  void SetLeptonType(std::string value){m_leptonType = value;};
  void SetChannel(std::string value){m_channel = value;};
  void SetDSID(int value){m_DSID = value;};

 private:
  
  int m_DSID;

  float m_lumiValue;
  float m_minLargeRJetPt;
  float m_matchingDR;
  float m_btaggingCut;
  float m_btaggingCutLoose;
  float m_leadingLeptonPt;
  float m_missingEtCut;
  float m_triangularCut;
  float m_lumiLabel;

  bool m_useLooseBTagging;
  bool m_useHFSplitting;
  
  std::string m_fileVariables;
  std::string m_leptonChannel;
  std::string m_analysisType;
  std::string m_hfType;
  std::string m_inputFile;
  std::string m_outputFile;
  std::string m_outputTreeFile;
  std::string m_leptonType;
  std::string m_channel;
  std::string m_sampleType;
  std::string m_dataLabel;

  BINS m_BTagBin;
  BINS m_JetBin;
  BINS m_LargeJetBin;
  BINS m_TopTagBin;
  BINS m_VetoBTagBin;
  BINS m_VetoJetBin;
  BINS m_VetoLargeJetBin;
  BINS m_VetoTopTagBin;


};

#endif
