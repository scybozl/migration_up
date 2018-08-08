
#include "TopMass_13TeV_Plotting/HistoCreator.h"
#include "TopMass_13TeV_Plotting/StatusLogbook.h"
#include "TopMass_13TeV_Plotting/FlatTreeReader.h"
#include "TopMass_13TeV_Plotting/BKUtilities.h"
#include "TopMass_13TeV_Plotting/HistoUtilities.h"
#include "TopMass_13TeV_Plotting/EventExtras.h"
#include "TopDataPreparation/SampleXsection.h"

#include "TChain.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TH2D.h"

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


HistoCreator::HistoCreator(std::string sampleList, std::string Channel, std::shared_ptr<ConfigClass> Config, std::string TreeName)
{

  gROOT        -> ProcessLine("#include<vector>");
  gInterpreter -> GenerateDictionary("vector<vector<int> >","vector");

  fSampleList = sampleList;
  gConfig     = Config;

  // chain all input trees
  TChain *HelpTree   = ChainFiles(TreeName.c_str(), fSampleList); // flat nominal tree
  TChain *HelpTreeBK = ChainFiles("sumWeights",     fSampleList); // Bookkeeping Tree

  std::vector<std::string> FileList = GetFileList(fSampleList);

  // get here all values from your config file
  fChannel         = gConfig -> GetChannel();
  fAnalysisType    = gConfig -> GetAnalysisType();
  fLumi            = gConfig -> GetLumi();
  fJetBin          = gConfig -> GetJetBin();
  fBTagBin         = gConfig -> GetBTagBin();
  fSampleType      = gConfig -> GetSampleType();
  fOutputFile      = gConfig -> GetOutputName();
  fOutputTreeFile  = gConfig -> GetOutputTreeName();
  fTreeName        = TreeName;

  if(fSampleType != "QCD_Nedaa"){

    // get total number of events for correct normalisation                                                                                                          
    fSampleInfo = CalculateTotalEventNumberHisto(FileList, HelpTreeBK, Channel);

    fDSID          = fSampleInfo.second;
    fTotalEventsMC = fSampleInfo.first;

  }


  gConfig -> SetDSID(fDSID);

  fFlatTree = new FlatTreeReader(HelpTree);

  std::cout << "fDSID == "        << fDSID        << std::endl;
  std::cout << "AnalysisType == " << fAnalysisType << std::endl;
    
}

HistoCreator::~HistoCreator()
{

  delete fFlatTree;

}

bool HistoCreator::InitializeHistograms(std::string InputFileName, std::string InputFileDir)
{
  
  WriteInfoStatus("HistoCreator", "InitializeHistograms...");
  ifstream InputListFile;
  InputListFile.open(InputFileName.c_str());

  int counter = 0;

  string fileline;
  string line;
  
  while (InputListFile.good()) {

    getline(InputListFile, fileline);
    std::istringstream input_fileline(fileline);

    string setname;
    string setindex;
    input_fileline >> setname;
    input_fileline >> setindex;

    int setindex_int = TString(setindex).Atoi();

    
    if(setindex_int == 0 && setname!="CoreHistos") continue;

    std::cout << "Adding Histogram set: " << setname << std::endl;    
    fSetList.push_back(setname);

    string setfilename = InputFileDir+setname+".txt";

    ifstream InputFile;
    InputFile.open(setfilename.c_str());

    while (InputFile.good()) {

      counter++;
      
      getline(InputFile, line);
    
      std::istringstream input_line(line);
      string name;
      string index;
      string bins;
      string lower;
      string upper;
      
      std::vector<double> binEdges;
      
      input_line >> name;
      input_line >> index;
      int   index_int = TString(index).Atoi();
      
      if(index_int == 1){

	TH1D helpHist;
	
       	input_line >> bins;

	// Variable Binning
	if (bins == "v" || bins == "V")
	  { 
	    string tmp;
	    input_line >> tmp;
	    int size = 0;
	    while (tmp != "v" && tmp != "V")
	      {
		binEdges.push_back(TString(tmp).Atof());
		size++;
		input_line >> tmp;
	      }
	    
	    double* edges_array = new double[ size ];
	    for ( int iii = 0; iii < size; ++iii)
	      {
		edges_array[iii] = binEdges[iii];
	      }
	    helpHist = TH1D(name.c_str(), name.c_str(), size-1, edges_array);
	    
	    delete edges_array;
	  }
	
	else
	  {
	    input_line >> lower;
	    input_line >> upper;
	    int   bins_int  = TString(bins).Atoi();
	    float lower_int = TString(lower).Atof();
	    float upper_int = TString(upper).Atof();
	    
	    helpHist = TH1D(name.c_str(), name.c_str(), bins_int, lower_int, upper_int);
	  }
	
	
	if(name.find( "weight_" ) != std::string::npos && fTreeName != "nominal")
          continue;
	
	helpHist.Sumw2();
	
	fHistoVector.push_back(helpHist);
	fHistoName.push_back("hist_"+name);
	fVariables.push_back(name);
	if(name.find( "weight_" ) != std::string::npos && fTreeName == "nominal_Loose" && fSampleType != "QCD_Nedaa") fWeights.push_back(name);
	
	float helpFloat;
	
	fVar.push_back(helpFloat);
	
	
      }
      

    }
  }

  return true;
}


void HistoCreator::FillCPDistributions()
{

  float LumiWeight = 1.0;
  if(fSampleType == "MC" || fSampleType == "MCNorm") 
    LumiWeight = CalculateLumiWeight();

  
  WriteInfoStatus("HistoCreator", "Fill CP distributions...");

  std::string OutputFileTree;  
  int TotalEntries = fFlatTree -> fChain -> GetEntries();
  float FinalWeight = -100.0;

  std::cout << "TotalEntries: " << TotalEntries << std::endl;

  TFile *fOutTreeFile = TFile::Open(fOutputTreeFile.c_str(), "RECREATE");
  TTree t2("t2","a new tree for top mass");

  t2.Branch("FinalWeight", &FinalWeight);
  t2.Branch("LumiWeight", &LumiWeight);
  



  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){
    fTreeVariables.push_back(0.);
  }

  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){
    t2.Branch(fVariables[iVar].c_str(), &fTreeVariables[iVar]);
  }
  
  for(unsigned iVar = 0; iVar < fWeights.size(); ++iVar){                                                                                                                                                                 
    t2.Branch(fWeights[iVar].c_str(),&fTreeWeights[iVar]);                                                                                                                                                                
  } 

  for(unsigned iVar = 0; iVar < fWeights.size(); ++iVar){
    fTreeWeights.push_back(0.);
  }

  // check for duplicates
  std::set<std::pair<int, int> > pairDuplicates; 
  EventExtras *iEntryExtras = 0;

  for(int iEntry = 0; iEntry < TotalEntries; ++iEntry){
    
    fFlatTree -> fChain -> GetEntry(iEntry);

    if((iEntry % 50000) == 0)
      std::cout << "Processing entry: " << iEntry << std::endl;
    
    if(fAnalysisType == "dilepton"){
      if(fChannel == "ee_2015"   && fFlatTree  ->  ee_2015 == 0)
	continue;
      if(fChannel == "ee_2016"   && fFlatTree  ->  ee_2016 == 0)
	continue;
      if(fChannel == "mumu_2015"  && fFlatTree  -> mumu_2015 == 0)
	continue;
      if(fChannel == "mumu_2016"  && fFlatTree  -> mumu_2016 == 0)
	continue;
      if(fChannel == "emu_2015"   && fFlatTree  ->  emu_2015 == 0)
	continue;
      if(fChannel == "emu_2016"   && fFlatTree  ->  emu_2016 == 0)
	continue;  	
      if(fChannel == "ll_2015"   && (fFlatTree  ->  emu_2015 == 0 && fFlatTree  -> mumu_2015 == 0 && fFlatTree  ->  ee_2015 == 0))
	continue;  	
      if(fChannel == "ll_2016"   && (fFlatTree  ->  emu_2016 == 0 && fFlatTree  -> mumu_2016 == 0 && fFlatTree  ->  ee_2016 == 0))
	continue;  	
      if(fChannel == "ll_comb"   && (fFlatTree  ->  emu_2016 == 0 && fFlatTree  -> mumu_2016 == 0 && fFlatTree  ->  ee_2016 == 0 && 
				     fFlatTree  ->  emu_2015 == 0 && fFlatTree  -> mumu_2015 == 0 && fFlatTree  ->  ee_2015 == 0))
	continue;  	
    }
    else{
      if(fChannel == "ejets_2015"   && fFlatTree  ->  ejets_2015 == 0)
	continue;
      if(fChannel == "mujets_2015"  && fFlatTree  -> mujets_2015 == 0)
	continue;
      if(fChannel == "ejets_2016"   && fFlatTree  ->  ejets_2016 == 0)
	continue;
      if(fChannel == "mujets_2016"  && fFlatTree  -> mujets_2016 == 0)
	continue;
      if(fChannel == "emujets_2015" && (fFlatTree ->  ejets_2015 == 0 && fFlatTree -> mujets_2015 == 0))
	continue;
      if(fChannel == "emujets_2016" && (fFlatTree ->  ejets_2016 == 0 && fFlatTree -> mujets_2016 == 0))
	continue;
      
      if(fChannel == "emujets_comb" && (fFlatTree ->  ejets_2016 == 0 && fFlatTree -> mujets_2016 == 0 &&
					fFlatTree ->  ejets_2015 == 0 && fFlatTree -> mujets_2015 == 0))
	continue;

      if(fFlatTree  -> ee_2015  == 1 || fFlatTree  -> mumu_2015  == 1 || fFlatTree  -> emu_2015  == 1)
	continue;
      if(fFlatTree  -> ee_2016  == 1 || fFlatTree  -> mumu_2016  == 1 || fFlatTree  -> emu_2016  == 1)
	continue;
    }


    // Create EventExtras
    if(iEntryExtras) delete iEntryExtras;
    iEntryExtras = new EventExtras(iEntry, fFlatTree, gConfig);

    // if data, check for double counting and take events that already exists out!!!
    if(fSampleType == "Data"){
      if(!pairDuplicates.insert(std::make_pair(fFlatTree->runNumber, fFlatTree->eventNumber)).second){
	std::cout << "WARNING Found duplicated data event in event: " << fFlatTree->eventNumber << "  run: " << fFlatTree->runNumber << " ===> event will be removed!" << std::endl;
	continue;
      }
    }

    // Set event weights
    FinalWeight = 1.0;

    if(fSampleType.find("MC") != std::string::npos && fBTagBin != v0incl)
	FinalWeight = LumiWeight*fFlatTree->weight_mc*fFlatTree->weight_leptonSF*fFlatTree->weight_bTagSF_77*fFlatTree->weight_jvt*fFlatTree->weight_pileup;
    else if(fSampleType.find("MC") != std::string::npos)
      FinalWeight = LumiWeight*fFlatTree->weight_mc*fFlatTree->weight_leptonSF*fFlatTree->weight_jvt*fFlatTree->weight_pileup;
      
    iEntryExtras -> SetEntryWeight(FinalWeight);
    iEntryExtras -> SetEntryLumiWeight(LumiWeight);

    int jets_all = iEntryExtras->GetNJetsAll();
    int tags_all = iEntryExtras->GetNBTagsAll();

    if(fAnalysisType == "lepjets"){
      TLorentzVector Lepton = iEntryExtras -> GetGoodLepton();

      double met = fFlatTree -> met_met/1000.0;
      double dPhi = Lepton.Phi() - fFlatTree -> met_phi;
      if (dPhi > 3.142) dPhi = 6.28 - dPhi;
      if (dPhi < - 3.142) dPhi = -6.28 - dPhi;
     
      double mtw = sqrt(2*Lepton.Pt()*met*(1-cos(dPhi)));
      
      if(met < 20.0)
	continue;
      
      if(met+mtw < 60.0)
	continue;
      
    }

    if(!passJetAndBTagBin(jets_all, tags_all, fJetBin, fBTagBin))
      continue;

    double fakesWeight = 1.0;

    if((fSampleType == "QCD_Nedaa") && (fAnalysisType == "lepjets")){
      
      if(fChannel == "emujets_2015" && fFlatTree -> ejets_2015)
        fakesWeight = fFlatTree -> fakesMM_weight_ejets_2015_test2015config4;
      if(fChannel == "emujets_2015" && fFlatTree -> mujets_2015)
        fakesWeight = fFlatTree -> fakesMM_weight_mujets_2015_test2015config4;
      if(fChannel == "emujets_2016" && fFlatTree -> ejets_2016)
        fakesWeight = fFlatTree -> fakesMM_weight_ejets_2016_test2016config4;
      if(fChannel == "emujets_2016" && fFlatTree -> mujets_2016)
	fakesWeight = fFlatTree -> fakesMM_weight_mujets_2016_test2016config4;

      FinalWeight = fakesWeight;
      
    }
    
    iEntryExtras -> SetEntryWeight(FinalWeight);
    

    if(fAnalysisType != "dilepton"){

      std::vector<TLorentzVector> bTaggedJets = iEntryExtras -> GetGoodSmallTags();
      
      TLorentzVector blep_original;;
      TLorentzVector bhad_original;;
      TLorentzVector lq1_original;
      TLorentzVector lq2_original;
      TLorentzVector Whad_original;
      
      double mtop_param = 0;
      double Rbq = 0;
      double Wmass = 0;
      
      if(fFlatTree -> klfitter_model_blep_pt  -> size() > 0){
	
	int blep_index = fFlatTree -> klfitter_model_blep_jetIndex -> at(0);
	blep_original.SetPtEtaPhiE(fFlatTree -> jet_pt  -> at(blep_index)/1000.0,
				   fFlatTree -> jet_eta -> at(blep_index),
				   fFlatTree -> jet_phi -> at(blep_index),
				   fFlatTree -> jet_e   -> at(blep_index)/1000.0);
	int bhad_index = fFlatTree -> klfitter_model_bhad_jetIndex -> at(0);
	bhad_original.SetPtEtaPhiE(fFlatTree -> jet_pt  -> at(bhad_index)/1000.0,
				   fFlatTree -> jet_eta -> at(bhad_index),
				   fFlatTree -> jet_phi -> at(bhad_index),
				 fFlatTree -> jet_e   -> at(bhad_index)/1000.0);
	int lq1_index = fFlatTree -> klfitter_model_lq1_jetIndex -> at(0);
	lq1_original.SetPtEtaPhiE(fFlatTree -> jet_pt  -> at(lq1_index)/1000.0,
				  fFlatTree -> jet_eta -> at(lq1_index),
				  fFlatTree -> jet_phi -> at(lq1_index),
				  fFlatTree -> jet_e   -> at(lq1_index)/1000.0);
	int lq2_index = fFlatTree -> klfitter_model_lq2_jetIndex -> at(0);
	lq2_original.SetPtEtaPhiE(fFlatTree -> jet_pt  -> at(lq2_index)/1000.0,
				  fFlatTree -> jet_eta -> at(lq2_index),
				  fFlatTree -> jet_phi -> at(lq2_index),
				  fFlatTree -> jet_e   -> at(lq2_index)/1000.0);
	
	
	Whad_original = lq1_original + lq2_original;
	Wmass = Whad_original.M();
	
	
	if(bTaggedJets.size() == 1){
	  
	  Rbq = bTaggedJets[0].Pt()/((lq1_original.Pt()+lq2_original.Pt())*0.5);
	}
	else if (bTaggedJets.size() >= 2){
	  Rbq = (bTaggedJets[0].Pt() + bTaggedJets[1].Pt())/(lq1_original.Pt()+lq2_original.Pt());
	}
	
	int   nr_param = (fFlatTree -> klfitter_parameters -> at(0)).size();
	mtop_param     = (fFlatTree -> klfitter_parameters -> at(0))[nr_param-1];
	
      }
      
      if( Wmass < 55 || Wmass > 110) continue;
      
      if( Rbq < 0.3 || Rbq > 3.0) continue;
      
      if( mtop_param < 125 || mtop_param > 200) continue;

      if( fFlatTree -> klfitter_minuitDidNotConverge -> at(0)) continue;

    }

    for(unsigned int iSet = 0; iSet<fSetList.size(); iSet++){
      
      if(fSetList[iSet] == "CoreHistos")     FillCoreHistos(iEntryExtras);
      if(fSetList[iSet] == "SmallJetsAll")   FillSmallJetsAllHistos(iEntryExtras,gConfig);
      if(fSetList[iSet] == "DileptonHistos") FillDileptonHistos(iEntryExtras,gConfig);
      if(fSetList[iSet] == "LepJetsHistos")  FillLepJetsHistos(iEntryExtras);
      if(fSetList[iSet] == "KLFHistos")      FillKLFitterHistos(iEntryExtras);
      if(fSetList[iSet] == "Weights")        {

	if(fSampleType != "Data" && fSampleType != "QCD_Nedaa" && fSampleType != "QCD")
	  FillWeights();

      }      
    }
    t2.Fill();
    
  }  
  t2.Write();
  
  
  fOutTreeFile -> Close();
  
  std::cout << "Write to file: " << fOutputFile.c_str() << std::endl;  

  TFile *fOutFile = TFile::Open(fOutputFile.c_str(), "RECREATE");

  for(unsigned int iHist = 0; iHist < fHistoVector.size(); ++iHist){   
    fHistoVector[iHist] = AddOverflow(fHistoVector[iHist]);
    fHistoVector[iHist].Write(fHistoName[iHist].c_str());
    if(fVariables[iHist] == "met_met")
      std::cout << std::setprecision(8) << fHistoVector[iHist].Integral() << "\t" << fHistoName[iHist].c_str() << std::endl;    
  }
  for(unsigned int iHist = 0; iHist < fCutflowHistoVector.size(); ++iHist){
    fCutflowHistoVector[iHist].Write();
  }

  if(fNtupleCutflowHisto_e.Integral()==0)  fNtupleCutflowHisto_e  = TH2D("NtupleCutflow_ejets", "NtupleCutflow_ejets",  1, 0, 1, 1, 0, 1);
  if(fNtupleCutflowHisto_mu.Integral()==0) fNtupleCutflowHisto_mu = TH2D("NtupleCutflow_mujets","NtupleCutflow_mujets", 1, 0, 1, 1, 0, 1);

  fNtupleCutflowHisto_e.Write();
  fNtupleCutflowHisto_mu.Write();
  
  fOutFile -> Close();

}


float HistoCreator::CalculateLumiWeight(){
  
  SampleXsection tdp;
  const char* const rc = getenv("AnalysisTop_DIR");
    std::string filename = std::string(rc) + "/data/TopDataPreparation/XSection-MC15-13TeV.data";
  if (!tdp.readFromFile(filename.c_str())) {
    std::cout << "ERROR:TopDataPreparation - could not read file\n";
    std::cout << filename << "\n";
    exit(1);
  }
  
  float xsection  = tdp.getXsection(fDSID); 
  fSampleXSection = xsection;
  
  float lumi = fTotalEventsMC/(xsection*fLumi);
  float SF   = 1/lumi; 
   
    std::cout << "===================================================================================> " << fSampleXSection << "\t" << fTotalEventsMC << "\t" << fLumi << std::endl;

  return SF;

}


