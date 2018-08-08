#include "TopMass_13TeV_Plotting/ConfigClass.h"
#include <algorithm>
#include <iterator>
#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>

using namespace std;

ConfigClass::ConfigClass()                          
{
  
  // we do not define default values here on purpose, because we want to ensure that each user thinks about the settings he needs
  // and does not just use the default that might be meaningless to his analysis

}

void ConfigClass::readSettingsFromConfig(std::string ConfigFileName)
{

  
  ifstream ConfigListFile;
  ConfigListFile.open(ConfigFileName.c_str());

  string fileline;
  string line;

  while (ConfigListFile.good()) {

    getline(ConfigListFile, fileline);
    std::istringstream input_line(fileline);
    
    string name;
    string value;

    input_line >> name;
    input_line >> value;

    if(name == "MinLargeRJetPt")
      m_minLargeRJetPt = TString(value).Atof();
    else if(name == "MatchingDR")
      m_matchingDR = TString(value).Atof();
    else if(name == "BTaggingDisc")
      m_btaggingCut = TString(value).Atof();
    else if(name == "BTaggingDiscLoose")
      m_btaggingCutLoose = TString(value).Atof();
    else if(name == "LeadLeptonPt")
      m_leadingLeptonPt = TString(value).Atof();
    else if(name == "UseLooseBTagging")
      m_useLooseBTagging = TString(value).Atoi();
    else if(name == "UseHF")
      m_useHFSplitting = TString(value).Atoi();
    else if(name == "AnalysisType")
      m_analysisType = TString(value);
    else if(name == "Lumi")
      m_lumiValue = TString(value).Atof();
    else if(name == "VariablesList")
      m_fileVariables = TString(value);
    else if(name == "LeptonChannel")
      m_leptonChannel = TString(value);
    else if(name == "MissingEt")
      m_missingEtCut = TString(value).Atof();
    else if(name == "TriangularCut")
      m_triangularCut = TString(value).Atof();
    else if(name == "LumiLabel")
      m_lumiLabel = TString(value).Atof();
    else if(name == "DataLabel")
      m_dataLabel = TString(value);
    else{
      
      std::cout << "ERROR(ConfigClass)::The configuration setting " << name.c_str() << " is not defined!!! ===> EXIT." << std::endl;
      
      exit(0);
      
    }


  }

}

