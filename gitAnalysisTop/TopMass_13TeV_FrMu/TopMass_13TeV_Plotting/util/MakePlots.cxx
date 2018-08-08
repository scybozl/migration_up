/**
 * Andrea Knue (aknue@cern.ch):
 * 
 * 
 */

#include <iostream>

#include "TopMass_13TeV_Plotting/HistoCreator.h"
#include "TopMass_13TeV_Plotting/StatusLogbook.h"
#include "TopMass_13TeV_Plotting/Enums.h"
#include "TopMass_13TeV_Plotting/ConfigClass.h"

#include "TRandom3.h"
#include "TSystem.h"
#include "TH1F.h"

#include <sys/time.h>
typedef unsigned long long timestamp_t;

static timestamp_t
get_timestamp ()
{
  struct timeval now;
  gettimeofday (&now, NULL);
  return  now.tv_usec + (timestamp_t)now.tv_sec * 1000000;
}


int main(int argc, char *argv[]){


 timestamp_t t0 = get_timestamp();
  

  if(argc < 9){

    WriteErrorStatus("MakePlots", "Number of input variables is wrong!!!");

    return 1;

  }
  else{

    for(int i = 1; i < argc; ++i)
      WriteParameterStatus("MakePlots", argv[i]);

  }

  std::string InputFileList  = argv[1];
  std::string OutputFile     = argv[2];
  std::string OutputTreeFile = argv[3];
  std::string SampleType     = argv[4];
  std::string JetBin         = argv[5];
  std::string BTagBin        = argv[6];
  std::string ConfigFileName = argv[7];
  std::string TreeName       = argv[8];

  std::string ScaleFactor    = "nominal";

  if(argc == 10){
    ScaleFactor = argv[9];
    TreeName    = "nominal";
  }

  std::shared_ptr<ConfigClass> fConfig(new ConfigClass());
  
  fConfig -> readSettingsFromConfig(ConfigFileName.c_str());

  fConfig -> SetJetBin(TranslateBinToEnum(JetBin));
  fConfig -> SetNumberOfBTags(TranslateBinToEnum(BTagBin));
  fConfig -> SetInputFile(InputFileList);
  fConfig -> SetOutputFile(OutputFile);
  fConfig -> SetOutputTreeFile(OutputTreeFile);
  fConfig -> SetSampleType(SampleType);
  
  std::string Channel      = fConfig -> GetChannel();
  std::string AnalysisType = fConfig -> GetAnalysisType();

  std::cout << "Channel = " << Channel.c_str() << std::endl;

  std::cout << "SampleType = " << SampleType.c_str() << std::endl;

  HistoCreator *fNewHisto = new HistoCreator(InputFileList, Channel, fConfig, TreeName);

  string pathToConf       = gSystem->Getenv("AnalysisTop_DIR");

  std::string ConfigFile    = pathToConf+"/data/TopMass_13TeV_Plotting/"+fConfig->GetConfigFileVariables();
  std::string ConfigFileDir = pathToConf+"/data/TopMass_13TeV_Plotting/";

  fNewHisto -> SetScaleFactorType(ScaleFactor);
  fNewHisto -> InitializeHistograms(ConfigFile, ConfigFileDir);

  WriteInfoStatus("MakePlots", "Fill CP Distributions...");

  fNewHisto -> FillCPDistributions();

  delete fNewHisto;

  timestamp_t t1 = get_timestamp();

  double secs = (t1 - t0) / 1000000.0L;

  std::cout << "TIME TO MAKE PLOTS: " << secs << std::endl;

  return 0;

}
