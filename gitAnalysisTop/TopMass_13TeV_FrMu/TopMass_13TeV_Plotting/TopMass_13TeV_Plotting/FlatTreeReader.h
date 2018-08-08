//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Oct 25 12:16:57 2016 by ROOT version 6.04/16
// from TTree nominal/tree
// found on file: /ptmp/mpp/knand/TopAnalysis_13TeV/Output_2.4.19_NominalOnly/Downloads/user.aknue.410000.PowhegPythiaEvtGen.DAOD_TOPQ1.e3698_s2608_s2183_r7725_r7676_p2669.02-04-19_BTagPri4_output.root/user.aknue.9573647._000010.output.root
//////////////////////////////////////////////////////////

#ifndef FlatTreeReader_h
#define FlatTreeReader_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.                                                                                                                             
  
#include <vector>
#include "TLorentzVector.h"

using namespace std;



class FlatTreeReader {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         fakesMM_weight_ejets_2015_test2015config4;
   Float_t         fakesMM_weight_ejets_2015_test2015config3;
   Float_t         fakesMM_weight_ejets_2015_test2015config2;
   Float_t         fakesMM_weight_ejets_2015_test2015config1;
   Float_t         fakesMM_weight_ejets_2016_test2016config4;
   Float_t         fakesMM_weight_ejets_2016_test2016config3;
   Float_t         fakesMM_weight_ejets_2016_test2016config2;
   Float_t         fakesMM_weight_ejets_2016_test2016config1;
   Float_t         fakesMM_weight_mujets_2015_test2015config4;
   Float_t         fakesMM_weight_mujets_2015_test2015config3;
   Float_t         fakesMM_weight_mujets_2015_test2015config2;
   Float_t         fakesMM_weight_mujets_2015_test2015config1;
   Float_t         fakesMM_weight_mujets_2016_test2016config4;
   Float_t         fakesMM_weight_mujets_2016_test2016config3;
   Float_t         fakesMM_weight_mujets_2016_test2016config2;
   Float_t         fakesMM_weight_mujets_2016_test2016config1;


   Float_t         weight_mc;
   Float_t         weight_pileup;
   Float_t         weight_leptonSF;
   Float_t         weight_bTagSF_77;
   Float_t         weight_jvt;
   Float_t         weight_pileup_UP;
   Float_t         weight_pileup_DOWN;
   Float_t         weight_leptonSF_EL_SF_Trigger_UP;
   Float_t         weight_leptonSF_EL_SF_Trigger_DOWN;
   Float_t         weight_leptonSF_EL_SF_Reco_UP;
   Float_t         weight_leptonSF_EL_SF_Reco_DOWN;
   Float_t         weight_leptonSF_EL_SF_ID_UP;
   Float_t         weight_leptonSF_EL_SF_ID_DOWN;
   Float_t         weight_leptonSF_EL_SF_Isol_UP;
   Float_t         weight_leptonSF_EL_SF_Isol_DOWN;
   Float_t         weight_leptonSF_MU_SF_Trigger_STAT_UP;
   Float_t         weight_leptonSF_MU_SF_Trigger_STAT_DOWN;
   Float_t         weight_leptonSF_MU_SF_Trigger_SYST_UP;
   Float_t         weight_leptonSF_MU_SF_Trigger_SYST_DOWN;
   Float_t         weight_leptonSF_MU_SF_ID_STAT_UP;
   Float_t         weight_leptonSF_MU_SF_ID_STAT_DOWN;
   Float_t         weight_leptonSF_MU_SF_ID_SYST_UP;
   Float_t         weight_leptonSF_MU_SF_ID_SYST_DOWN;
   Float_t         weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP;
   Float_t         weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN;
   Float_t         weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP;
   Float_t         weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN;
   Float_t         weight_leptonSF_MU_SF_Isol_STAT_UP;
   Float_t         weight_leptonSF_MU_SF_Isol_STAT_DOWN;
   Float_t         weight_leptonSF_MU_SF_Isol_SYST_UP;
   Float_t         weight_leptonSF_MU_SF_Isol_SYST_DOWN;
   Float_t         weight_leptonSF_MU_SF_TTVA_STAT_UP;
   Float_t         weight_leptonSF_MU_SF_TTVA_STAT_DOWN;
   Float_t         weight_leptonSF_MU_SF_TTVA_SYST_UP;
   Float_t         weight_leptonSF_MU_SF_TTVA_SYST_DOWN;
   Float_t         weight_indiv_SF_EL_Trigger;
   Float_t         weight_indiv_SF_EL_Trigger_UP;
   Float_t         weight_indiv_SF_EL_Trigger_DOWN;
   Float_t         weight_indiv_SF_EL_Reco;
   Float_t         weight_indiv_SF_EL_Reco_UP;
   Float_t         weight_indiv_SF_EL_Reco_DOWN;
   Float_t         weight_indiv_SF_EL_ID;
   Float_t         weight_indiv_SF_EL_ID_UP;
   Float_t         weight_indiv_SF_EL_ID_DOWN;
   Float_t         weight_indiv_SF_EL_Isol;
   Float_t         weight_indiv_SF_EL_Isol_UP;
   Float_t         weight_indiv_SF_EL_Isol_DOWN;
   Float_t         weight_indiv_SF_MU_Trigger;
   Float_t         weight_indiv_SF_MU_Trigger_STAT_UP;
   Float_t         weight_indiv_SF_MU_Trigger_STAT_DOWN;
   Float_t         weight_indiv_SF_MU_Trigger_SYST_UP;
   Float_t         weight_indiv_SF_MU_Trigger_SYST_DOWN;
   Float_t         weight_indiv_SF_MU_ID;
   Float_t         weight_indiv_SF_MU_ID_STAT_UP;
   Float_t         weight_indiv_SF_MU_ID_STAT_DOWN;
   Float_t         weight_indiv_SF_MU_ID_SYST_UP;
   Float_t         weight_indiv_SF_MU_ID_SYST_DOWN;
   Float_t         weight_indiv_SF_MU_ID_STAT_LOWPT_UP;
   Float_t         weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN;
   Float_t         weight_indiv_SF_MU_ID_SYST_LOWPT_UP;
   Float_t         weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN;
   Float_t         weight_indiv_SF_MU_Isol;
   Float_t         weight_indiv_SF_MU_Isol_STAT_UP;
   Float_t         weight_indiv_SF_MU_Isol_STAT_DOWN;
   Float_t         weight_indiv_SF_MU_Isol_SYST_UP;
   Float_t         weight_indiv_SF_MU_Isol_SYST_DOWN;
   Float_t         weight_indiv_SF_MU_TTVA;
   Float_t         weight_indiv_SF_MU_TTVA_STAT_UP;
   Float_t         weight_indiv_SF_MU_TTVA_STAT_DOWN;
   Float_t         weight_indiv_SF_MU_TTVA_SYST_UP;
   Float_t         weight_indiv_SF_MU_TTVA_SYST_DOWN;
   Float_t         weight_jvt_UP;
   Float_t         weight_jvt_DOWN;
   Float_t         LumiWeight;
   vector<float>   *weight_bTagSF_77_eigenvars_B_up;
   vector<float>   *weight_bTagSF_77_eigenvars_C_up;
   vector<float>   *weight_bTagSF_77_eigenvars_Light_up;
   vector<float>   *weight_bTagSF_77_eigenvars_B_down;
   vector<float>   *weight_bTagSF_77_eigenvars_C_down;
   vector<float>   *weight_bTagSF_77_eigenvars_Light_down;
   Float_t         weight_bTagSF_77_extrapolation_up;
   Float_t         weight_bTagSF_77_extrapolation_down;
   Float_t         weight_bTagSF_77_extrapolation_from_charm_up;
   Float_t         weight_bTagSF_77_extrapolation_from_charm_down;
   ULong64_t       eventNumber;
   UInt_t          runNumber;
   UInt_t          randomRunNumber;
   UInt_t          mcChannelNumber;
   Float_t         mu;
   UInt_t          backgroundFlags;
   vector<float>   *el_pt;
   vector<float>   *el_eta;
   vector<float>   *el_cl_eta;
   vector<float>   *el_phi;
   vector<float>   *el_e;
   vector<float>   *el_charge;
   vector<float>   *el_topoetcone20;
   vector<float>   *el_ptvarcone20;
   vector<float>   *el_d0sig;
   vector<float>   *el_delta_z0_sintheta;
   vector<int>     *el_true_type;
   vector<int>     *el_true_origin;
   vector<int>     *el_true_typebkg;
   vector<int>     *el_true_originbkg;
   vector<float>   *mu_pt;
   vector<float>   *mu_eta;
   vector<float>   *mu_phi;
   vector<float>   *mu_e;
   vector<float>   *mu_charge;
   vector<float>   *mu_topoetcone20;
   vector<float>   *mu_ptvarcone30;
   vector<float>   *mu_d0sig;
   vector<float>   *mu_delta_z0_sintheta;
   vector<int>     *mu_true_type;
   vector<int>     *mu_true_origin;
   vector<float>   *jet_pt;
   vector<float>   *jet_eta;
   vector<float>   *jet_phi;
   vector<float>   *jet_e;
   vector<float>   *jet_mv2c00;
   vector<float>   *jet_mv2c10;
   vector<float>   *jet_mv2c20;
   vector<float>   *jet_ip3dsv1;
   vector<float>   *jet_jvt;
   vector<int>     *jet_truthflav;
   vector<char>    *jet_isbtagged_77;
   Float_t         met_met;
   Float_t         met_phi;
   Short_t         klfitter_selected;
   vector<short>   *klfitter_minuitDidNotConverge;
   vector<short>   *klfitter_fitAbortedDueToNaN;
   vector<short>   *klfitter_atLeastOneFitParameterAtItsLimit;
   vector<short>   *klfitter_invalidTransferFunctionAtConvergence;
   vector<unsigned int> *klfitter_bestPermutation;
   vector<float>   *klfitter_logLikelihood;
   vector<float>   *klfitter_eventProbability;
   vector<vector<double> > *klfitter_parameters;
   vector<vector<double> > *klfitter_parameterErrors;
   vector<float>   *klfitter_model_bhad_pt;
   vector<float>   *klfitter_model_bhad_eta;
   vector<float>   *klfitter_model_bhad_phi;
   vector<float>   *klfitter_model_bhad_E;
   vector<unsigned int> *klfitter_model_bhad_jetIndex;
   vector<float>   *klfitter_model_blep_pt;
   vector<float>   *klfitter_model_blep_eta;
   vector<float>   *klfitter_model_blep_phi;
   vector<float>   *klfitter_model_blep_E;
   vector<unsigned int> *klfitter_model_blep_jetIndex;
   vector<float>   *klfitter_model_lq1_pt;
   vector<float>   *klfitter_model_lq1_eta;
   vector<float>   *klfitter_model_lq1_phi;
   vector<float>   *klfitter_model_lq1_E;
   vector<unsigned int> *klfitter_model_lq1_jetIndex;
   vector<float>   *klfitter_model_lq2_pt;
   vector<float>   *klfitter_model_lq2_eta;
   vector<float>   *klfitter_model_lq2_phi;
   vector<float>   *klfitter_model_lq2_E;
   vector<unsigned int> *klfitter_model_lq2_jetIndex;
   vector<float>   *klfitter_model_lep_pt;
   vector<float>   *klfitter_model_lep_eta;
   vector<float>   *klfitter_model_lep_phi;
   vector<float>   *klfitter_model_lep_E;
   vector<float>   *klfitter_model_nu_pt;
   vector<float>   *klfitter_model_nu_eta;
   vector<float>   *klfitter_model_nu_phi;
   vector<float>   *klfitter_model_nu_E;
   Float_t         klfitter_bestPerm_topLep_pt;
   Float_t         klfitter_bestPerm_topLep_eta;
   Float_t         klfitter_bestPerm_topLep_phi;
   Float_t         klfitter_bestPerm_topLep_E;
   Float_t         klfitter_bestPerm_topLep_m;
   Float_t         klfitter_bestPerm_topHad_pt;
   Float_t         klfitter_bestPerm_topHad_eta;
   Float_t         klfitter_bestPerm_topHad_phi;
   Float_t         klfitter_bestPerm_topHad_E;
   Float_t         klfitter_bestPerm_topHad_m;
   Float_t         klfitter_bestPerm_ttbar_pt;
   Float_t         klfitter_bestPerm_ttbar_eta;
   Float_t         klfitter_bestPerm_ttbar_phi;
   Float_t         klfitter_bestPerm_ttbar_E;
   Float_t         klfitter_bestPerm_ttbar_m;
   Int_t           ejets_2015;
   Int_t           ejets_2016;
   Int_t           mujets_2015;
   Int_t           mujets_2016;
   Int_t           ee_2015;
   Int_t           ee_2016;
   Int_t           mumu_2015;
   Int_t           mumu_2016;
   Int_t           emu_2015;
   Int_t           emu_2016;
   Char_t          HLT_mu20_iloose_L1MU15;
   Char_t          HLT_e60_lhmedium_nod0;
   Char_t          HLT_mu26_ivarmedium;
   Char_t          HLT_e26_lhtight_nod0_ivarloose;
   Char_t          HLT_e140_lhloose_nod0;
   Char_t          HLT_mu50;
   Char_t          HLT_e60_lhmedium;
   Char_t          HLT_e24_lhmedium_L1EM20VH;
   Char_t          HLT_e120_lhloose;
   vector<char>    *el_trigMatch_HLT_e60_lhmedium_nod0;
   vector<char>    *el_trigMatch_HLT_e26_lhtight_nod0_ivarloose;
   vector<char>    *el_trigMatch_HLT_e140_lhloose_nod0;
   vector<char>    *el_trigMatch_HLT_e60_lhmedium;
   vector<char>    *el_trigMatch_HLT_e24_lhmedium_L1EM20VH;
   vector<char>    *el_trigMatch_HLT_e120_lhloose;
   vector<char>    *mu_trigMatch_HLT_mu26_ivarmedium;
   vector<char>    *mu_trigMatch_HLT_mu50;
   vector<char>    *mu_trigMatch_HLT_mu20_iloose_L1MU15;

   // List of branches
   TBranch        *b_fakesMM_weight_ejets_2015_test2015config4;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2015_test2015config3;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2015_test2015config2;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2015_test2015config1;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2016_test2016config4;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2016_test2016config3;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2016_test2016config2;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_ejets_2016_test2016config1;   //!                                                                                                                   
   TBranch        *b_fakesMM_weight_mujets_2015_test2015config4;   //!                                                                                                                  
   TBranch        *b_fakesMM_weight_mujets_2015_test2015config3;   //!                                                                                                                  
   TBranch        *b_fakesMM_weight_mujets_2015_test2015config2;   //!                                                                                                                  
   TBranch        *b_fakesMM_weight_mujets_2015_test2015config1;   //!                                                                                                                  
   TBranch        *b_fakesMM_weight_mujets_2016_test2016config4;   //!                                                                                                                  
   TBranch        *b_fakesMM_weight_mujets_2016_test2016config3;   //!                                                                                                                 
   TBranch        *b_fakesMM_weight_mujets_2016_test2016config2;   //!                                                                                                                
   TBranch        *b_fakesMM_weight_mujets_2016_test2016config1;   //!   

   TBranch        *b_weight_mc;   //!
   TBranch        *b_weight_pileup;   //!
   TBranch        *b_weight_leptonSF;   //!
   TBranch        *b_weight_bTagSF_77;   //!
   TBranch        *b_weight_jvt;   //!
   TBranch        *b_weight_pileup_UP;   //!
   TBranch        *b_weight_pileup_DOWN;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Trigger_UP;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Trigger_DOWN;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Reco_UP;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Reco_DOWN;   //!
   TBranch        *b_weight_leptonSF_EL_SF_ID_UP;   //!
   TBranch        *b_weight_leptonSF_EL_SF_ID_DOWN;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Isol_UP;   //!
   TBranch        *b_weight_leptonSF_EL_SF_Isol_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Trigger_STAT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Trigger_STAT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Trigger_SYST_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Trigger_SYST_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_STAT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_STAT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_SYST_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_SYST_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Isol_STAT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Isol_STAT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Isol_SYST_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_Isol_SYST_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_TTVA_STAT_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_TTVA_STAT_DOWN;   //!
   TBranch        *b_weight_leptonSF_MU_SF_TTVA_SYST_UP;   //!
   TBranch        *b_weight_leptonSF_MU_SF_TTVA_SYST_DOWN;   //!
   TBranch        *b_weight_indiv_SF_EL_Trigger;   //!
   TBranch        *b_weight_indiv_SF_EL_Trigger_UP;   //!
   TBranch        *b_weight_indiv_SF_EL_Trigger_DOWN;   //!
   TBranch        *b_weight_indiv_SF_EL_Reco;   //!
   TBranch        *b_weight_indiv_SF_EL_Reco_UP;   //!
   TBranch        *b_weight_indiv_SF_EL_Reco_DOWN;   //!
   TBranch        *b_weight_indiv_SF_EL_ID;   //!
   TBranch        *b_weight_indiv_SF_EL_ID_UP;   //!
   TBranch        *b_weight_indiv_SF_EL_ID_DOWN;   //!
   TBranch        *b_weight_indiv_SF_EL_Isol;   //!
   TBranch        *b_weight_indiv_SF_EL_Isol_UP;   //!
   TBranch        *b_weight_indiv_SF_EL_Isol_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_Trigger;   //!
   TBranch        *b_weight_indiv_SF_MU_Trigger_STAT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_Trigger_STAT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_Trigger_SYST_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_Trigger_SYST_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_ID;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_STAT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_STAT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_SYST_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_SYST_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_STAT_LOWPT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_SYST_LOWPT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_Isol;   //!
   TBranch        *b_weight_indiv_SF_MU_Isol_STAT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_Isol_STAT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_Isol_SYST_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_Isol_SYST_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_TTVA;   //!
   TBranch        *b_weight_indiv_SF_MU_TTVA_STAT_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_TTVA_STAT_DOWN;   //!
   TBranch        *b_weight_indiv_SF_MU_TTVA_SYST_UP;   //!
   TBranch        *b_weight_indiv_SF_MU_TTVA_SYST_DOWN;   //!
   TBranch        *b_weight_jvt_UP;   //!
   TBranch        *b_weight_jvt_DOWN;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_B_up;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_C_up;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_Light_up;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_B_down;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_C_down;   //!
   TBranch        *b_weight_bTagSF_77_eigenvars_Light_down;   //!
   TBranch        *b_weight_bTagSF_77_extrapolation_up;   //!
   TBranch        *b_weight_bTagSF_77_extrapolation_down;   //!
   TBranch        *b_weight_bTagSF_77_extrapolation_from_charm_up;   //!
   TBranch        *b_weight_bTagSF_77_extrapolation_from_charm_down;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_runNumber;   //!
   TBranch        *b_randomRunNumber;   //!
   TBranch        *b_mcChannelNumber;   //!
   TBranch        *b_mu;   //!
   TBranch        *b_backgroundFlags;   //!
   TBranch        *b_el_pt;   //!
   TBranch        *b_el_eta;   //!
   TBranch        *b_el_cl_eta;   //!
   TBranch        *b_el_phi;   //!
   TBranch        *b_el_e;   //!
   TBranch        *b_el_charge;   //!
   TBranch        *b_el_topoetcone20;   //!
   TBranch        *b_el_ptvarcone20;   //!
   TBranch        *b_el_d0sig;   //!
   TBranch        *b_el_delta_z0_sintheta;   //!
   TBranch        *b_el_true_type;   //!
   TBranch        *b_el_true_origin;   //!
   TBranch        *b_el_true_typebkg;   //!
   TBranch        *b_el_true_originbkg;   //!
   TBranch        *b_mu_pt;   //!
   TBranch        *b_mu_eta;   //!
   TBranch        *b_mu_phi;   //!
   TBranch        *b_mu_e;   //!
   TBranch        *b_mu_charge;   //!
   TBranch        *b_mu_topoetcone20;   //!
   TBranch        *b_mu_ptvarcone30;   //!
   TBranch        *b_mu_d0sig;   //!
   TBranch        *b_mu_delta_z0_sintheta;   //!
   TBranch        *b_mu_true_type;   //!
   TBranch        *b_mu_true_origin;   //!
   TBranch        *b_jet_pt;   //!
   TBranch        *b_jet_eta;   //!
   TBranch        *b_jet_phi;   //!
   TBranch        *b_jet_e;   //!
   TBranch        *b_jet_mv2c00;   //!
   TBranch        *b_jet_mv2c10;   //!
   TBranch        *b_jet_mv2c20;   //!
   TBranch        *b_jet_ip3dsv1;   //!
   TBranch        *b_jet_jvt;   //!
   TBranch        *b_jet_truthflav;   //!
   TBranch        *b_jet_isbtagged_77;   //!
   TBranch        *b_met_met;   //!
   TBranch        *b_met_phi;   //!
   TBranch        *b_klfitter_selected;   //!
   TBranch        *b_klfitter_minuitDidNotConverge;   //!
   TBranch        *b_klfitter_fitAbortedDueToNaN;   //!
   TBranch        *b_klfitter_atLeastOneFitParameterAtItsLimit;   //!
   TBranch        *b_klfitter_invalidTransferFunctionAtConvergence;   //!
   TBranch        *b_klfitter_bestPermutation;   //!
   TBranch        *b_klfitter_logLikelihood;   //!
   TBranch        *b_klfitter_eventProbability;   //!
   TBranch        *b_klfitter_parameters;   //!
   TBranch        *b_klfitter_parameterErrors;   //!
   TBranch        *b_klfitter_model_bhad_pt;   //!
   TBranch        *b_klfitter_model_bhad_eta;   //!
   TBranch        *b_klfitter_model_bhad_phi;   //!
   TBranch        *b_klfitter_model_bhad_E;   //!
   TBranch        *b_klfitter_model_bhad_jetIndex;   //!
   TBranch        *b_klfitter_model_blep_pt;   //!
   TBranch        *b_klfitter_model_blep_eta;   //!
   TBranch        *b_klfitter_model_blep_phi;   //!
   TBranch        *b_klfitter_model_blep_E;   //!
   TBranch        *b_klfitter_model_blep_jetIndex;   //!
   TBranch        *b_klfitter_model_lq1_pt;   //!
   TBranch        *b_klfitter_model_lq1_eta;   //!
   TBranch        *b_klfitter_model_lq1_phi;   //!
   TBranch        *b_klfitter_model_lq1_E;   //!
   TBranch        *b_klfitter_model_lq1_jetIndex;   //!
   TBranch        *b_klfitter_model_lq2_pt;   //!
   TBranch        *b_klfitter_model_lq2_eta;   //!
   TBranch        *b_klfitter_model_lq2_phi;   //!
   TBranch        *b_klfitter_model_lq2_E;   //!
   TBranch        *b_klfitter_model_lq2_jetIndex;   //!
   TBranch        *b_klfitter_model_lep_pt;   //!
   TBranch        *b_klfitter_model_lep_eta;   //!
   TBranch        *b_klfitter_model_lep_phi;   //!
   TBranch        *b_klfitter_model_lep_E;   //!
   TBranch        *b_klfitter_model_nu_pt;   //!
   TBranch        *b_klfitter_model_nu_eta;   //!
   TBranch        *b_klfitter_model_nu_phi;   //!
   TBranch        *b_klfitter_model_nu_E;   //!
   TBranch        *b_klfitter_bestPerm_topLep_pt;   //!
   TBranch        *b_klfitter_bestPerm_topLep_eta;   //!
   TBranch        *b_klfitter_bestPerm_topLep_phi;   //!
   TBranch        *b_klfitter_bestPerm_topLep_E;   //!
   TBranch        *b_klfitter_bestPerm_topLep_m;   //!
   TBranch        *b_klfitter_bestPerm_topHad_pt;   //!
   TBranch        *b_klfitter_bestPerm_topHad_eta;   //!
   TBranch        *b_klfitter_bestPerm_topHad_phi;   //!
   TBranch        *b_klfitter_bestPerm_topHad_E;   //!
   TBranch        *b_klfitter_bestPerm_topHad_m;   //!
   TBranch        *b_klfitter_bestPerm_ttbar_pt;   //!
   TBranch        *b_klfitter_bestPerm_ttbar_eta;   //!
   TBranch        *b_klfitter_bestPerm_ttbar_phi;   //!
   TBranch        *b_klfitter_bestPerm_ttbar_E;   //!
   TBranch        *b_klfitter_bestPerm_ttbar_m;   //!
   TBranch        *b_ejets_2015;   //!
   TBranch        *b_ejets_2016;   //!
   TBranch        *b_mujets_2015;   //!
   TBranch        *b_mujets_2016;   //!
   TBranch        *b_ee_2015;   //!
   TBranch        *b_ee_2016;   //!
   TBranch        *b_mumu_2015;   //!
   TBranch        *b_mumu_2016;   //!
   TBranch        *b_emu_2015;   //!
   TBranch        *b_emu_2016;   //!
   TBranch        *b_HLT_mu20_iloose_L1MU15;   //!
   TBranch        *b_HLT_e60_lhmedium_nod0;   //!
   TBranch        *b_HLT_mu26_ivarmedium;   //!
   TBranch        *b_HLT_e26_lhtight_nod0_ivarloose;   //!
   TBranch        *b_HLT_e140_lhloose_nod0;   //!
   TBranch        *b_HLT_mu50;   //!
   TBranch        *b_HLT_e60_lhmedium;   //!
   TBranch        *b_HLT_e24_lhmedium_L1EM20VH;   //!
   TBranch        *b_HLT_e120_lhloose;   //!
   TBranch        *b_el_trigMatch_HLT_e60_lhmedium_nod0;   //!
   TBranch        *b_el_trigMatch_HLT_e26_lhtight_nod0_ivarloose;   //!
   TBranch        *b_el_trigMatch_HLT_e140_lhloose_nod0;   //!
   TBranch        *b_el_trigMatch_HLT_e60_lhmedium;   //!
   TBranch        *b_el_trigMatch_HLT_e24_lhmedium_L1EM20VH;   //!
   TBranch        *b_el_trigMatch_HLT_e120_lhloose;   //!
   TBranch        *b_mu_trigMatch_HLT_mu26_ivarmedium;   //!
   TBranch        *b_mu_trigMatch_HLT_mu50;   //!
   TBranch        *b_mu_trigMatch_HLT_mu20_iloose_L1MU15;   //!

   FlatTreeReader(TTree *tree=0);
   virtual ~FlatTreeReader();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef FlatTreeReader_cxx
FlatTreeReader::FlatTreeReader(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/ptmp/mpp/knand/TopAnalysis_13TeV/Output_2.4.19_NominalOnly/Downloads/user.aknue.410000.PowhegPythiaEvtGen.DAOD_TOPQ1.e3698_s2608_s2183_r7725_r7676_p2669.02-04-19_BTagPri4_output.root/user.aknue.9573647._000010.output.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/ptmp/mpp/knand/TopAnalysis_13TeV/Output_2.4.19_NominalOnly/Downloads/user.aknue.410000.PowhegPythiaEvtGen.DAOD_TOPQ1.e3698_s2608_s2183_r7725_r7676_p2669.02-04-19_BTagPri4_output.root/user.aknue.9573647._000010.output.root");
      }
      f->GetObject("nominal",tree);

   }
   Init(tree);
}

FlatTreeReader::~FlatTreeReader()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t FlatTreeReader::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t FlatTreeReader::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void FlatTreeReader::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   weight_bTagSF_77_eigenvars_B_up = 0;
   weight_bTagSF_77_eigenvars_C_up = 0;
   weight_bTagSF_77_eigenvars_Light_up = 0;
   weight_bTagSF_77_eigenvars_B_down = 0;
   weight_bTagSF_77_eigenvars_C_down = 0;
   weight_bTagSF_77_eigenvars_Light_down = 0;
   el_pt = 0;
   el_eta = 0;
   el_cl_eta = 0;
   el_phi = 0;
   el_e = 0;
   el_charge = 0;
   el_topoetcone20 = 0;
   el_ptvarcone20 = 0;
   el_d0sig = 0;
   el_delta_z0_sintheta = 0;
   el_true_type = 0;
   el_true_origin = 0;
   el_true_typebkg = 0;
   el_true_originbkg = 0;
   mu_pt = 0;
   mu_eta = 0;
   mu_phi = 0;
   mu_e = 0;
   mu_charge = 0;
   mu_topoetcone20 = 0;
   mu_ptvarcone30 = 0;
   mu_d0sig = 0;
   mu_delta_z0_sintheta = 0;
   mu_true_type = 0;
   mu_true_origin = 0;
   jet_pt = 0;
   jet_eta = 0;
   jet_phi = 0;
   jet_e = 0;
   jet_mv2c00 = 0;
   jet_mv2c10 = 0;
   jet_mv2c20 = 0;
   jet_ip3dsv1 = 0;
   jet_jvt = 0;
   jet_truthflav = 0;
   jet_isbtagged_77 = 0;
   klfitter_minuitDidNotConverge = 0;
   klfitter_fitAbortedDueToNaN = 0;
   klfitter_atLeastOneFitParameterAtItsLimit = 0;
   klfitter_invalidTransferFunctionAtConvergence = 0;
   klfitter_bestPermutation = 0;
   klfitter_logLikelihood = 0;
   klfitter_eventProbability = 0;
   klfitter_parameters = 0;
   klfitter_parameterErrors = 0;
   klfitter_model_bhad_pt = 0;
   klfitter_model_bhad_eta = 0;
   klfitter_model_bhad_phi = 0;
   klfitter_model_bhad_E = 0;
   klfitter_model_bhad_jetIndex = 0;
   klfitter_model_blep_pt = 0;
   klfitter_model_blep_eta = 0;
   klfitter_model_blep_phi = 0;
   klfitter_model_blep_E = 0;
   klfitter_model_blep_jetIndex = 0;
   klfitter_model_lq1_pt = 0;
   klfitter_model_lq1_eta = 0;
   klfitter_model_lq1_phi = 0;
   klfitter_model_lq1_E = 0;
   klfitter_model_lq1_jetIndex = 0;
   klfitter_model_lq2_pt = 0;
   klfitter_model_lq2_eta = 0;
   klfitter_model_lq2_phi = 0;
   klfitter_model_lq2_E = 0;
   klfitter_model_lq2_jetIndex = 0;
   klfitter_model_lep_pt = 0;
   klfitter_model_lep_eta = 0;
   klfitter_model_lep_phi = 0;
   klfitter_model_lep_E = 0;
   klfitter_model_nu_pt = 0;
   klfitter_model_nu_eta = 0;
   klfitter_model_nu_phi = 0;
   klfitter_model_nu_E = 0;
   el_trigMatch_HLT_e60_lhmedium_nod0 = 0;
   el_trigMatch_HLT_e26_lhtight_nod0_ivarloose = 0;
   el_trigMatch_HLT_e140_lhloose_nod0 = 0;
   el_trigMatch_HLT_e60_lhmedium = 0;
   el_trigMatch_HLT_e24_lhmedium_L1EM20VH = 0;
   el_trigMatch_HLT_e120_lhloose = 0;
   mu_trigMatch_HLT_mu26_ivarmedium = 0;
   mu_trigMatch_HLT_mu50 = 0;
   mu_trigMatch_HLT_mu20_iloose_L1MU15 = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);


   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2015_test2015config4")) fChain->SetBranchAddress("fakesMM_weight_ejets_2015_test2015config4", &fakesMM_weight_ejets_2015_test2015config4, &b_fakesMM_weight_ejets_2015_test2015config4);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2015_test2015config3")) fChain->SetBranchAddress("fakesMM_weight_ejets_2015_test2015config3", &fakesMM_weight_ejets_2015_test2015config3, &b_fakesMM_weight_ejets_2015_test2015config3);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2015_test2015config2")) fChain->SetBranchAddress("fakesMM_weight_ejets_2015_test2015config2", &fakesMM_weight_ejets_2015_test2015config2, &b_fakesMM_weight_ejets_2015_test2015config2);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2015_test2015config1")) fChain->SetBranchAddress("fakesMM_weight_ejets_2015_test2015config1", &fakesMM_weight_ejets_2015_test2015config1, &b_fakesMM_weight_ejets_2015_test2015config1);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2016_test2016config4")) fChain->SetBranchAddress("fakesMM_weight_ejets_2016_test2016config4", &fakesMM_weight_ejets_2016_test2016config4, &b_fakesMM_weight_ejets_2016_test2016config4);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2016_test2016config3")) fChain->SetBranchAddress("fakesMM_weight_ejets_2016_test2016config3", &fakesMM_weight_ejets_2016_test2016config3, &b_fakesMM_weight_ejets_2016_test2016config3);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2016_test2016config2")) fChain->SetBranchAddress("fakesMM_weight_ejets_2016_test2016config2", &fakesMM_weight_ejets_2016_test2016config2, &b_fakesMM_weight_ejets_2016_test2016config2);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_ejets_2016_test2016config1")) fChain->SetBranchAddress("fakesMM_weight_ejets_2016_test2016config1", &fakesMM_weight_ejets_2016_test2016config1, &b_fakesMM_weight_ejets_2016_test2016config1);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2015_test2015config4")) fChain->SetBranchAddress("fakesMM_weight_mujets_2015_test2015config4", &fakesMM_weight_mujets_2015_test2015config4, &b_fakesMM_weight_mujets_2015_test2015config4);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2015_test2015config3")) fChain->SetBranchAddress("fakesMM_weight_mujets_2015_test2015config3", &fakesMM_weight_mujets_2015_test2015config3, &b_fakesMM_weight_mujets_2015_test2015config3);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2015_test2015config2")) fChain->SetBranchAddress("fakesMM_weight_mujets_2015_test2015config2", &fakesMM_weight_mujets_2015_test2015config2, &b_fakesMM_weight_mujets_2015_test2015config2);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2015_test2015config1")) fChain->SetBranchAddress("fakesMM_weight_mujets_2015_test2015config1", &fakesMM_weight_mujets_2015_test2015config1, &b_fakesMM_weight_mujets_2015_test2015config1);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2016_test2016config4")) fChain->SetBranchAddress("fakesMM_weight_mujets_2016_test2016config4", &fakesMM_weight_mujets_2016_test2016config4, &b_fakesMM_weight_mujets_2016_test2016config4);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2016_test2016config3")) fChain->SetBranchAddress("fakesMM_weight_mujets_2016_test2016config3", &fakesMM_weight_mujets_2016_test2016config3, &b_fakesMM_weight_mujets_2016_test2016config3);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2016_test2016config2")) fChain->SetBranchAddress("fakesMM_weight_mujets_2016_test2016config2", &fakesMM_weight_mujets_2016_test2016config2, &b_fakesMM_weight_mujets_2016_test2016config2);
   if (fChain->GetListOfBranches()->Contains("fakesMM_weight_mujets_2016_test2016config1")) fChain->SetBranchAddress("fakesMM_weight_mujets_2016_test2016config1", &fakesMM_weight_mujets_2016_test2016config1, &b_fakesMM_weight_mujets_2016_test2016config1);


   if (fChain->GetListOfBranches()->Contains("weight_mc")) fChain->SetBranchAddress("weight_mc", &weight_mc, &b_weight_mc);
   if (fChain->GetListOfBranches()->Contains("weight_pileup")) fChain->SetBranchAddress("weight_pileup", &weight_pileup, &b_weight_pileup);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF")) fChain->SetBranchAddress("weight_leptonSF", &weight_leptonSF, &b_weight_leptonSF);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77")) fChain->SetBranchAddress("weight_bTagSF_77", &weight_bTagSF_77, &b_weight_bTagSF_77);
   if (fChain->GetListOfBranches()->Contains("weight_jvt")) fChain->SetBranchAddress("weight_jvt", &weight_jvt, &b_weight_jvt);
   if (fChain->GetListOfBranches()->Contains("weight_pileup_UP")) fChain->SetBranchAddress("weight_pileup_UP", &weight_pileup_UP, &b_weight_pileup_UP);
   if (fChain->GetListOfBranches()->Contains("weight_pileup_DOWN")) fChain->SetBranchAddress("weight_pileup_DOWN", &weight_pileup_DOWN, &b_weight_pileup_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Trigger_UP")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Trigger_UP", &weight_leptonSF_EL_SF_Trigger_UP, &b_weight_leptonSF_EL_SF_Trigger_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Trigger_DOWN")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Trigger_DOWN", &weight_leptonSF_EL_SF_Trigger_DOWN, &b_weight_leptonSF_EL_SF_Trigger_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Reco_UP")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Reco_UP", &weight_leptonSF_EL_SF_Reco_UP, &b_weight_leptonSF_EL_SF_Reco_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Reco_DOWN")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Reco_DOWN", &weight_leptonSF_EL_SF_Reco_DOWN, &b_weight_leptonSF_EL_SF_Reco_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_ID_UP")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_ID_UP", &weight_leptonSF_EL_SF_ID_UP, &b_weight_leptonSF_EL_SF_ID_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_ID_DOWN")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_ID_DOWN", &weight_leptonSF_EL_SF_ID_DOWN, &b_weight_leptonSF_EL_SF_ID_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Isol_UP")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Isol_UP", &weight_leptonSF_EL_SF_Isol_UP, &b_weight_leptonSF_EL_SF_Isol_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_EL_SF_Isol_DOWN")) fChain->SetBranchAddress("weight_leptonSF_EL_SF_Isol_DOWN", &weight_leptonSF_EL_SF_Isol_DOWN, &b_weight_leptonSF_EL_SF_Isol_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Trigger_STAT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Trigger_STAT_UP", &weight_leptonSF_MU_SF_Trigger_STAT_UP, &b_weight_leptonSF_MU_SF_Trigger_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Trigger_STAT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Trigger_STAT_DOWN", &weight_leptonSF_MU_SF_Trigger_STAT_DOWN, &b_weight_leptonSF_MU_SF_Trigger_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Trigger_SYST_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Trigger_SYST_UP", &weight_leptonSF_MU_SF_Trigger_SYST_UP, &b_weight_leptonSF_MU_SF_Trigger_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Trigger_SYST_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Trigger_SYST_DOWN", &weight_leptonSF_MU_SF_Trigger_SYST_DOWN, &b_weight_leptonSF_MU_SF_Trigger_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_STAT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_STAT_UP", &weight_leptonSF_MU_SF_ID_STAT_UP, &b_weight_leptonSF_MU_SF_ID_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_STAT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_STAT_DOWN", &weight_leptonSF_MU_SF_ID_STAT_DOWN, &b_weight_leptonSF_MU_SF_ID_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_SYST_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_SYST_UP", &weight_leptonSF_MU_SF_ID_SYST_UP, &b_weight_leptonSF_MU_SF_ID_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_SYST_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_SYST_DOWN", &weight_leptonSF_MU_SF_ID_SYST_DOWN, &b_weight_leptonSF_MU_SF_ID_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP", &weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP, &b_weight_leptonSF_MU_SF_ID_STAT_LOWPT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN", &weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN, &b_weight_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP", &weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP, &b_weight_leptonSF_MU_SF_ID_SYST_LOWPT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN", &weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN, &b_weight_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Isol_STAT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Isol_STAT_UP", &weight_leptonSF_MU_SF_Isol_STAT_UP, &b_weight_leptonSF_MU_SF_Isol_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Isol_STAT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Isol_STAT_DOWN", &weight_leptonSF_MU_SF_Isol_STAT_DOWN, &b_weight_leptonSF_MU_SF_Isol_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Isol_SYST_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Isol_SYST_UP", &weight_leptonSF_MU_SF_Isol_SYST_UP, &b_weight_leptonSF_MU_SF_Isol_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_Isol_SYST_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_Isol_SYST_DOWN", &weight_leptonSF_MU_SF_Isol_SYST_DOWN, &b_weight_leptonSF_MU_SF_Isol_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_TTVA_STAT_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_TTVA_STAT_UP", &weight_leptonSF_MU_SF_TTVA_STAT_UP, &b_weight_leptonSF_MU_SF_TTVA_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_TTVA_STAT_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_TTVA_STAT_DOWN", &weight_leptonSF_MU_SF_TTVA_STAT_DOWN, &b_weight_leptonSF_MU_SF_TTVA_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_TTVA_SYST_UP")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_TTVA_SYST_UP", &weight_leptonSF_MU_SF_TTVA_SYST_UP, &b_weight_leptonSF_MU_SF_TTVA_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_leptonSF_MU_SF_TTVA_SYST_DOWN")) fChain->SetBranchAddress("weight_leptonSF_MU_SF_TTVA_SYST_DOWN", &weight_leptonSF_MU_SF_TTVA_SYST_DOWN, &b_weight_leptonSF_MU_SF_TTVA_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Trigger")) fChain->SetBranchAddress("weight_indiv_SF_EL_Trigger", &weight_indiv_SF_EL_Trigger, &b_weight_indiv_SF_EL_Trigger);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Trigger_UP")) fChain->SetBranchAddress("weight_indiv_SF_EL_Trigger_UP", &weight_indiv_SF_EL_Trigger_UP, &b_weight_indiv_SF_EL_Trigger_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Trigger_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_EL_Trigger_DOWN", &weight_indiv_SF_EL_Trigger_DOWN, &b_weight_indiv_SF_EL_Trigger_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Reco")) fChain->SetBranchAddress("weight_indiv_SF_EL_Reco", &weight_indiv_SF_EL_Reco, &b_weight_indiv_SF_EL_Reco);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Reco_UP")) fChain->SetBranchAddress("weight_indiv_SF_EL_Reco_UP", &weight_indiv_SF_EL_Reco_UP, &b_weight_indiv_SF_EL_Reco_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Reco_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_EL_Reco_DOWN", &weight_indiv_SF_EL_Reco_DOWN, &b_weight_indiv_SF_EL_Reco_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_ID")) fChain->SetBranchAddress("weight_indiv_SF_EL_ID", &weight_indiv_SF_EL_ID, &b_weight_indiv_SF_EL_ID);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_ID_UP")) fChain->SetBranchAddress("weight_indiv_SF_EL_ID_UP", &weight_indiv_SF_EL_ID_UP, &b_weight_indiv_SF_EL_ID_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_ID_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_EL_ID_DOWN", &weight_indiv_SF_EL_ID_DOWN, &b_weight_indiv_SF_EL_ID_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Isol")) fChain->SetBranchAddress("weight_indiv_SF_EL_Isol", &weight_indiv_SF_EL_Isol, &b_weight_indiv_SF_EL_Isol);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Isol_UP")) fChain->SetBranchAddress("weight_indiv_SF_EL_Isol_UP", &weight_indiv_SF_EL_Isol_UP, &b_weight_indiv_SF_EL_Isol_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_EL_Isol_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_EL_Isol_DOWN", &weight_indiv_SF_EL_Isol_DOWN, &b_weight_indiv_SF_EL_Isol_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Trigger")) fChain->SetBranchAddress("weight_indiv_SF_MU_Trigger", &weight_indiv_SF_MU_Trigger, &b_weight_indiv_SF_MU_Trigger);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Trigger_STAT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_Trigger_STAT_UP", &weight_indiv_SF_MU_Trigger_STAT_UP, &b_weight_indiv_SF_MU_Trigger_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Trigger_STAT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_Trigger_STAT_DOWN", &weight_indiv_SF_MU_Trigger_STAT_DOWN, &b_weight_indiv_SF_MU_Trigger_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Trigger_SYST_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_Trigger_SYST_UP", &weight_indiv_SF_MU_Trigger_SYST_UP, &b_weight_indiv_SF_MU_Trigger_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Trigger_SYST_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_Trigger_SYST_DOWN", &weight_indiv_SF_MU_Trigger_SYST_DOWN, &b_weight_indiv_SF_MU_Trigger_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID", &weight_indiv_SF_MU_ID, &b_weight_indiv_SF_MU_ID);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_STAT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_STAT_UP", &weight_indiv_SF_MU_ID_STAT_UP, &b_weight_indiv_SF_MU_ID_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_STAT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_STAT_DOWN", &weight_indiv_SF_MU_ID_STAT_DOWN, &b_weight_indiv_SF_MU_ID_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_SYST_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_SYST_UP", &weight_indiv_SF_MU_ID_SYST_UP, &b_weight_indiv_SF_MU_ID_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_SYST_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_SYST_DOWN", &weight_indiv_SF_MU_ID_SYST_DOWN, &b_weight_indiv_SF_MU_ID_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_STAT_LOWPT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_STAT_LOWPT_UP", &weight_indiv_SF_MU_ID_STAT_LOWPT_UP, &b_weight_indiv_SF_MU_ID_STAT_LOWPT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN", &weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN, &b_weight_indiv_SF_MU_ID_STAT_LOWPT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_SYST_LOWPT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_SYST_LOWPT_UP", &weight_indiv_SF_MU_ID_SYST_LOWPT_UP, &b_weight_indiv_SF_MU_ID_SYST_LOWPT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN", &weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN, &b_weight_indiv_SF_MU_ID_SYST_LOWPT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Isol")) fChain->SetBranchAddress("weight_indiv_SF_MU_Isol", &weight_indiv_SF_MU_Isol, &b_weight_indiv_SF_MU_Isol);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Isol_STAT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_Isol_STAT_UP", &weight_indiv_SF_MU_Isol_STAT_UP, &b_weight_indiv_SF_MU_Isol_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Isol_STAT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_Isol_STAT_DOWN", &weight_indiv_SF_MU_Isol_STAT_DOWN, &b_weight_indiv_SF_MU_Isol_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Isol_SYST_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_Isol_SYST_UP", &weight_indiv_SF_MU_Isol_SYST_UP, &b_weight_indiv_SF_MU_Isol_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_Isol_SYST_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_Isol_SYST_DOWN", &weight_indiv_SF_MU_Isol_SYST_DOWN, &b_weight_indiv_SF_MU_Isol_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_TTVA")) fChain->SetBranchAddress("weight_indiv_SF_MU_TTVA", &weight_indiv_SF_MU_TTVA, &b_weight_indiv_SF_MU_TTVA);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_TTVA_STAT_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_TTVA_STAT_UP", &weight_indiv_SF_MU_TTVA_STAT_UP, &b_weight_indiv_SF_MU_TTVA_STAT_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_TTVA_STAT_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_TTVA_STAT_DOWN", &weight_indiv_SF_MU_TTVA_STAT_DOWN, &b_weight_indiv_SF_MU_TTVA_STAT_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_TTVA_SYST_UP")) fChain->SetBranchAddress("weight_indiv_SF_MU_TTVA_SYST_UP", &weight_indiv_SF_MU_TTVA_SYST_UP, &b_weight_indiv_SF_MU_TTVA_SYST_UP);
   if (fChain->GetListOfBranches()->Contains("weight_indiv_SF_MU_TTVA_SYST_DOWN")) fChain->SetBranchAddress("weight_indiv_SF_MU_TTVA_SYST_DOWN", &weight_indiv_SF_MU_TTVA_SYST_DOWN, &b_weight_indiv_SF_MU_TTVA_SYST_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_jvt_UP")) fChain->SetBranchAddress("weight_jvt_UP", &weight_jvt_UP, &b_weight_jvt_UP);
   if (fChain->GetListOfBranches()->Contains("weight_jvt_DOWN")) fChain->SetBranchAddress("weight_jvt_DOWN", &weight_jvt_DOWN, &b_weight_jvt_DOWN);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_B_up")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_B_up", &weight_bTagSF_77_eigenvars_B_up, &b_weight_bTagSF_77_eigenvars_B_up);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_C_up")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_C_up", &weight_bTagSF_77_eigenvars_C_up, &b_weight_bTagSF_77_eigenvars_C_up);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_Light_up")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_Light_up", &weight_bTagSF_77_eigenvars_Light_up, &b_weight_bTagSF_77_eigenvars_Light_up);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_B_down")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_B_down", &weight_bTagSF_77_eigenvars_B_down, &b_weight_bTagSF_77_eigenvars_B_down);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_C_down")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_C_down", &weight_bTagSF_77_eigenvars_C_down, &b_weight_bTagSF_77_eigenvars_C_down);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_eigenvars_Light_down")) fChain->SetBranchAddress("weight_bTagSF_77_eigenvars_Light_down", &weight_bTagSF_77_eigenvars_Light_down, &b_weight_bTagSF_77_eigenvars_Light_down);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_extrapolation_up")) fChain->SetBranchAddress("weight_bTagSF_77_extrapolation_up", &weight_bTagSF_77_extrapolation_up, &b_weight_bTagSF_77_extrapolation_up);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_extrapolation_down")) fChain->SetBranchAddress("weight_bTagSF_77_extrapolation_down", &weight_bTagSF_77_extrapolation_down, &b_weight_bTagSF_77_extrapolation_down);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_extrapolation_from_charm_up")) fChain->SetBranchAddress("weight_bTagSF_77_extrapolation_from_charm_up", &weight_bTagSF_77_extrapolation_from_charm_up, &b_weight_bTagSF_77_extrapolation_from_charm_up);
   if (fChain->GetListOfBranches()->Contains("weight_bTagSF_77_extrapolation_from_charm_down")) fChain->SetBranchAddress("weight_bTagSF_77_extrapolation_from_charm_down", &weight_bTagSF_77_extrapolation_from_charm_down, &b_weight_bTagSF_77_extrapolation_from_charm_down);
   if (fChain->GetListOfBranches()->Contains("eventNumber")) fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   if (fChain->GetListOfBranches()->Contains("runNumber")) fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   if (fChain->GetListOfBranches()->Contains("randomRunNumber")) fChain->SetBranchAddress("randomRunNumber", &randomRunNumber, &b_randomRunNumber);
   if (fChain->GetListOfBranches()->Contains("mcChannelNumber")) fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
   if (fChain->GetListOfBranches()->Contains("mu")) fChain->SetBranchAddress("mu", &mu, &b_mu);
   if (fChain->GetListOfBranches()->Contains("backgroundFlags")) fChain->SetBranchAddress("backgroundFlags", &backgroundFlags, &b_backgroundFlags);
   if (fChain->GetListOfBranches()->Contains("el_pt")) fChain->SetBranchAddress("el_pt", &el_pt, &b_el_pt);
   if (fChain->GetListOfBranches()->Contains("el_eta")) fChain->SetBranchAddress("el_eta", &el_eta, &b_el_eta);
   if (fChain->GetListOfBranches()->Contains("el_cl_eta")) fChain->SetBranchAddress("el_cl_eta", &el_cl_eta, &b_el_cl_eta);
   if (fChain->GetListOfBranches()->Contains("el_phi")) fChain->SetBranchAddress("el_phi", &el_phi, &b_el_phi);
   if (fChain->GetListOfBranches()->Contains("el_e")) fChain->SetBranchAddress("el_e", &el_e, &b_el_e);
   if (fChain->GetListOfBranches()->Contains("el_charge")) fChain->SetBranchAddress("el_charge", &el_charge, &b_el_charge);
   if (fChain->GetListOfBranches()->Contains("el_topoetcone20")) fChain->SetBranchAddress("el_topoetcone20", &el_topoetcone20, &b_el_topoetcone20);
   if (fChain->GetListOfBranches()->Contains("el_ptvarcone20")) fChain->SetBranchAddress("el_ptvarcone20", &el_ptvarcone20, &b_el_ptvarcone20);
   if (fChain->GetListOfBranches()->Contains("el_d0sig")) fChain->SetBranchAddress("el_d0sig", &el_d0sig, &b_el_d0sig);
   if (fChain->GetListOfBranches()->Contains("el_delta_z0_sintheta")) fChain->SetBranchAddress("el_delta_z0_sintheta", &el_delta_z0_sintheta, &b_el_delta_z0_sintheta);
   if (fChain->GetListOfBranches()->Contains("el_true_type")) fChain->SetBranchAddress("el_true_type", &el_true_type, &b_el_true_type);
   if (fChain->GetListOfBranches()->Contains("el_true_origin")) fChain->SetBranchAddress("el_true_origin", &el_true_origin, &b_el_true_origin);
   if (fChain->GetListOfBranches()->Contains("el_true_typebkg")) fChain->SetBranchAddress("el_true_typebkg", &el_true_typebkg, &b_el_true_typebkg);
   if (fChain->GetListOfBranches()->Contains("el_true_originbkg")) fChain->SetBranchAddress("el_true_originbkg", &el_true_originbkg, &b_el_true_originbkg);
   if (fChain->GetListOfBranches()->Contains("mu_pt")) fChain->SetBranchAddress("mu_pt", &mu_pt, &b_mu_pt);
   if (fChain->GetListOfBranches()->Contains("mu_eta")) fChain->SetBranchAddress("mu_eta", &mu_eta, &b_mu_eta);
   if (fChain->GetListOfBranches()->Contains("mu_phi")) fChain->SetBranchAddress("mu_phi", &mu_phi, &b_mu_phi);
   if (fChain->GetListOfBranches()->Contains("mu_e")) fChain->SetBranchAddress("mu_e", &mu_e, &b_mu_e);
   if (fChain->GetListOfBranches()->Contains("mu_charge")) fChain->SetBranchAddress("mu_charge", &mu_charge, &b_mu_charge);
   if (fChain->GetListOfBranches()->Contains("mu_topoetcone20")) fChain->SetBranchAddress("mu_topoetcone20", &mu_topoetcone20, &b_mu_topoetcone20);
   if (fChain->GetListOfBranches()->Contains("mu_ptvarcone30")) fChain->SetBranchAddress("mu_ptvarcone30", &mu_ptvarcone30, &b_mu_ptvarcone30);
   if (fChain->GetListOfBranches()->Contains("mu_d0sig")) fChain->SetBranchAddress("mu_d0sig", &mu_d0sig, &b_mu_d0sig);
   if (fChain->GetListOfBranches()->Contains("mu_delta_z0_sintheta")) fChain->SetBranchAddress("mu_delta_z0_sintheta", &mu_delta_z0_sintheta, &b_mu_delta_z0_sintheta);
   if (fChain->GetListOfBranches()->Contains("mu_true_type")) fChain->SetBranchAddress("mu_true_type", &mu_true_type, &b_mu_true_type);
   if (fChain->GetListOfBranches()->Contains("mu_true_origin")) fChain->SetBranchAddress("mu_true_origin", &mu_true_origin, &b_mu_true_origin);
   if (fChain->GetListOfBranches()->Contains("jet_pt")) fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   if (fChain->GetListOfBranches()->Contains("jet_eta")) fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   if (fChain->GetListOfBranches()->Contains("jet_phi")) fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   if (fChain->GetListOfBranches()->Contains("jet_e")) fChain->SetBranchAddress("jet_e", &jet_e, &b_jet_e);
   if (fChain->GetListOfBranches()->Contains("jet_mv2c00")) fChain->SetBranchAddress("jet_mv2c00", &jet_mv2c00, &b_jet_mv2c00);
   if (fChain->GetListOfBranches()->Contains("jet_mv2c10")) fChain->SetBranchAddress("jet_mv2c10", &jet_mv2c10, &b_jet_mv2c10);
   if (fChain->GetListOfBranches()->Contains("jet_mv2c20")) fChain->SetBranchAddress("jet_mv2c20", &jet_mv2c20, &b_jet_mv2c20);
   if (fChain->GetListOfBranches()->Contains("jet_ip3dsv1")) fChain->SetBranchAddress("jet_ip3dsv1", &jet_ip3dsv1, &b_jet_ip3dsv1);
   if (fChain->GetListOfBranches()->Contains("jet_jvt")) fChain->SetBranchAddress("jet_jvt", &jet_jvt, &b_jet_jvt);
   if (fChain->GetListOfBranches()->Contains("jet_truthflav")) fChain->SetBranchAddress("jet_truthflav", &jet_truthflav, &b_jet_truthflav);
   if (fChain->GetListOfBranches()->Contains("jet_isbtagged_77")) fChain->SetBranchAddress("jet_isbtagged_77", &jet_isbtagged_77, &b_jet_isbtagged_77);
   if (fChain->GetListOfBranches()->Contains("met_met")) fChain->SetBranchAddress("met_met", &met_met, &b_met_met);
   if (fChain->GetListOfBranches()->Contains("met_phi")) fChain->SetBranchAddress("met_phi", &met_phi, &b_met_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_selected")) fChain->SetBranchAddress("klfitter_selected", &klfitter_selected, &b_klfitter_selected);
   if (fChain->GetListOfBranches()->Contains("klfitter_minuitDidNotConverge")) fChain->SetBranchAddress("klfitter_minuitDidNotConverge", &klfitter_minuitDidNotConverge, &b_klfitter_minuitDidNotConverge);
   if (fChain->GetListOfBranches()->Contains("klfitter_fitAbortedDueToNaN")) fChain->SetBranchAddress("klfitter_fitAbortedDueToNaN", &klfitter_fitAbortedDueToNaN, &b_klfitter_fitAbortedDueToNaN);
   if (fChain->GetListOfBranches()->Contains("klfitter_atLeastOneFitParameterAtItsLimit")) fChain->SetBranchAddress("klfitter_atLeastOneFitParameterAtItsLimit", &klfitter_atLeastOneFitParameterAtItsLimit, &b_klfitter_atLeastOneFitParameterAtItsLimit);
   if (fChain->GetListOfBranches()->Contains("klfitter_invalidTransferFunctionAtConvergence")) fChain->SetBranchAddress("klfitter_invalidTransferFunctionAtConvergence", &klfitter_invalidTransferFunctionAtConvergence, &b_klfitter_invalidTransferFunctionAtConvergence);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPermutation")) fChain->SetBranchAddress("klfitter_bestPermutation", &klfitter_bestPermutation, &b_klfitter_bestPermutation);
   if (fChain->GetListOfBranches()->Contains("klfitter_logLikelihood")) fChain->SetBranchAddress("klfitter_logLikelihood", &klfitter_logLikelihood, &b_klfitter_logLikelihood);
   if (fChain->GetListOfBranches()->Contains("klfitter_eventProbability")) fChain->SetBranchAddress("klfitter_eventProbability", &klfitter_eventProbability, &b_klfitter_eventProbability);
   if (fChain->GetListOfBranches()->Contains("klfitter_parameters")) fChain->SetBranchAddress("klfitter_parameters", &klfitter_parameters, &b_klfitter_parameters);
   if (fChain->GetListOfBranches()->Contains("klfitter_parameterErrors")) fChain->SetBranchAddress("klfitter_parameterErrors", &klfitter_parameterErrors, &b_klfitter_parameterErrors);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_bhad_pt")) fChain->SetBranchAddress("klfitter_model_bhad_pt", &klfitter_model_bhad_pt, &b_klfitter_model_bhad_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_bhad_eta")) fChain->SetBranchAddress("klfitter_model_bhad_eta", &klfitter_model_bhad_eta, &b_klfitter_model_bhad_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_bhad_phi")) fChain->SetBranchAddress("klfitter_model_bhad_phi", &klfitter_model_bhad_phi, &b_klfitter_model_bhad_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_bhad_E")) fChain->SetBranchAddress("klfitter_model_bhad_E", &klfitter_model_bhad_E, &b_klfitter_model_bhad_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_bhad_jetIndex")) fChain->SetBranchAddress("klfitter_model_bhad_jetIndex", &klfitter_model_bhad_jetIndex, &b_klfitter_model_bhad_jetIndex);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_blep_pt")) fChain->SetBranchAddress("klfitter_model_blep_pt", &klfitter_model_blep_pt, &b_klfitter_model_blep_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_blep_eta")) fChain->SetBranchAddress("klfitter_model_blep_eta", &klfitter_model_blep_eta, &b_klfitter_model_blep_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_blep_phi")) fChain->SetBranchAddress("klfitter_model_blep_phi", &klfitter_model_blep_phi, &b_klfitter_model_blep_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_blep_E")) fChain->SetBranchAddress("klfitter_model_blep_E", &klfitter_model_blep_E, &b_klfitter_model_blep_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_blep_jetIndex")) fChain->SetBranchAddress("klfitter_model_blep_jetIndex", &klfitter_model_blep_jetIndex, &b_klfitter_model_blep_jetIndex);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq1_pt")) fChain->SetBranchAddress("klfitter_model_lq1_pt", &klfitter_model_lq1_pt, &b_klfitter_model_lq1_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq1_eta")) fChain->SetBranchAddress("klfitter_model_lq1_eta", &klfitter_model_lq1_eta, &b_klfitter_model_lq1_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq1_phi")) fChain->SetBranchAddress("klfitter_model_lq1_phi", &klfitter_model_lq1_phi, &b_klfitter_model_lq1_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq1_E")) fChain->SetBranchAddress("klfitter_model_lq1_E", &klfitter_model_lq1_E, &b_klfitter_model_lq1_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq1_jetIndex")) fChain->SetBranchAddress("klfitter_model_lq1_jetIndex", &klfitter_model_lq1_jetIndex, &b_klfitter_model_lq1_jetIndex);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq2_pt")) fChain->SetBranchAddress("klfitter_model_lq2_pt", &klfitter_model_lq2_pt, &b_klfitter_model_lq2_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq2_eta")) fChain->SetBranchAddress("klfitter_model_lq2_eta", &klfitter_model_lq2_eta, &b_klfitter_model_lq2_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq2_phi")) fChain->SetBranchAddress("klfitter_model_lq2_phi", &klfitter_model_lq2_phi, &b_klfitter_model_lq2_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq2_E")) fChain->SetBranchAddress("klfitter_model_lq2_E", &klfitter_model_lq2_E, &b_klfitter_model_lq2_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lq2_jetIndex")) fChain->SetBranchAddress("klfitter_model_lq2_jetIndex", &klfitter_model_lq2_jetIndex, &b_klfitter_model_lq2_jetIndex);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lep_pt")) fChain->SetBranchAddress("klfitter_model_lep_pt", &klfitter_model_lep_pt, &b_klfitter_model_lep_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lep_eta")) fChain->SetBranchAddress("klfitter_model_lep_eta", &klfitter_model_lep_eta, &b_klfitter_model_lep_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lep_phi")) fChain->SetBranchAddress("klfitter_model_lep_phi", &klfitter_model_lep_phi, &b_klfitter_model_lep_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_lep_E")) fChain->SetBranchAddress("klfitter_model_lep_E", &klfitter_model_lep_E, &b_klfitter_model_lep_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_nu_pt")) fChain->SetBranchAddress("klfitter_model_nu_pt", &klfitter_model_nu_pt, &b_klfitter_model_nu_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_nu_eta")) fChain->SetBranchAddress("klfitter_model_nu_eta", &klfitter_model_nu_eta, &b_klfitter_model_nu_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_nu_phi")) fChain->SetBranchAddress("klfitter_model_nu_phi", &klfitter_model_nu_phi, &b_klfitter_model_nu_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_model_nu_E")) fChain->SetBranchAddress("klfitter_model_nu_E", &klfitter_model_nu_E, &b_klfitter_model_nu_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topLep_pt")) fChain->SetBranchAddress("klfitter_bestPerm_topLep_pt", &klfitter_bestPerm_topLep_pt, &b_klfitter_bestPerm_topLep_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topLep_eta")) fChain->SetBranchAddress("klfitter_bestPerm_topLep_eta", &klfitter_bestPerm_topLep_eta, &b_klfitter_bestPerm_topLep_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topLep_phi")) fChain->SetBranchAddress("klfitter_bestPerm_topLep_phi", &klfitter_bestPerm_topLep_phi, &b_klfitter_bestPerm_topLep_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topLep_E")) fChain->SetBranchAddress("klfitter_bestPerm_topLep_E", &klfitter_bestPerm_topLep_E, &b_klfitter_bestPerm_topLep_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topLep_m")) fChain->SetBranchAddress("klfitter_bestPerm_topLep_m", &klfitter_bestPerm_topLep_m, &b_klfitter_bestPerm_topLep_m);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topHad_pt")) fChain->SetBranchAddress("klfitter_bestPerm_topHad_pt", &klfitter_bestPerm_topHad_pt, &b_klfitter_bestPerm_topHad_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topHad_eta")) fChain->SetBranchAddress("klfitter_bestPerm_topHad_eta", &klfitter_bestPerm_topHad_eta, &b_klfitter_bestPerm_topHad_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topHad_phi")) fChain->SetBranchAddress("klfitter_bestPerm_topHad_phi", &klfitter_bestPerm_topHad_phi, &b_klfitter_bestPerm_topHad_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topHad_E")) fChain->SetBranchAddress("klfitter_bestPerm_topHad_E", &klfitter_bestPerm_topHad_E, &b_klfitter_bestPerm_topHad_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_topHad_m")) fChain->SetBranchAddress("klfitter_bestPerm_topHad_m", &klfitter_bestPerm_topHad_m, &b_klfitter_bestPerm_topHad_m);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_ttbar_pt")) fChain->SetBranchAddress("klfitter_bestPerm_ttbar_pt", &klfitter_bestPerm_ttbar_pt, &b_klfitter_bestPerm_ttbar_pt);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_ttbar_eta")) fChain->SetBranchAddress("klfitter_bestPerm_ttbar_eta", &klfitter_bestPerm_ttbar_eta, &b_klfitter_bestPerm_ttbar_eta);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_ttbar_phi")) fChain->SetBranchAddress("klfitter_bestPerm_ttbar_phi", &klfitter_bestPerm_ttbar_phi, &b_klfitter_bestPerm_ttbar_phi);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_ttbar_E")) fChain->SetBranchAddress("klfitter_bestPerm_ttbar_E", &klfitter_bestPerm_ttbar_E, &b_klfitter_bestPerm_ttbar_E);
   if (fChain->GetListOfBranches()->Contains("klfitter_bestPerm_ttbar_m")) fChain->SetBranchAddress("klfitter_bestPerm_ttbar_m", &klfitter_bestPerm_ttbar_m, &b_klfitter_bestPerm_ttbar_m);
   if (fChain->GetListOfBranches()->Contains("ejets_2015")) fChain->SetBranchAddress("ejets_2015", &ejets_2015, &b_ejets_2015);
   if (fChain->GetListOfBranches()->Contains("ejets_2016")) fChain->SetBranchAddress("ejets_2016", &ejets_2016, &b_ejets_2016);
   if (fChain->GetListOfBranches()->Contains("mujets_2015")) fChain->SetBranchAddress("mujets_2015", &mujets_2015, &b_mujets_2015);
   if (fChain->GetListOfBranches()->Contains("mujets_2016")) fChain->SetBranchAddress("mujets_2016", &mujets_2016, &b_mujets_2016);
   if (fChain->GetListOfBranches()->Contains("ee_2015")) fChain->SetBranchAddress("ee_2015", &ee_2015, &b_ee_2015);
   if (fChain->GetListOfBranches()->Contains("ee_2016")) fChain->SetBranchAddress("ee_2016", &ee_2016, &b_ee_2016);
   if (fChain->GetListOfBranches()->Contains("mumu_2015")) fChain->SetBranchAddress("mumu_2015", &mumu_2015, &b_mumu_2015);
   if (fChain->GetListOfBranches()->Contains("mumu_2016")) fChain->SetBranchAddress("mumu_2016", &mumu_2016, &b_mumu_2016);
   if (fChain->GetListOfBranches()->Contains("emu_2015")) fChain->SetBranchAddress("emu_2015", &emu_2015, &b_emu_2015);
   if (fChain->GetListOfBranches()->Contains("emu_2016")) fChain->SetBranchAddress("emu_2016", &emu_2016, &b_emu_2016);
   if (fChain->GetListOfBranches()->Contains("HLT_mu20_iloose_L1MU15")) fChain->SetBranchAddress("HLT_mu20_iloose_L1MU15", &HLT_mu20_iloose_L1MU15, &b_HLT_mu20_iloose_L1MU15);
   if (fChain->GetListOfBranches()->Contains("HLT_e60_lhmedium_nod0")) fChain->SetBranchAddress("HLT_e60_lhmedium_nod0", &HLT_e60_lhmedium_nod0, &b_HLT_e60_lhmedium_nod0);
   if (fChain->GetListOfBranches()->Contains("HLT_mu26_ivarmedium")) fChain->SetBranchAddress("HLT_mu26_ivarmedium", &HLT_mu26_ivarmedium, &b_HLT_mu26_ivarmedium);
   if (fChain->GetListOfBranches()->Contains("HLT_e26_lhtight_nod0_ivarloose")) fChain->SetBranchAddress("HLT_e26_lhtight_nod0_ivarloose", &HLT_e26_lhtight_nod0_ivarloose, &b_HLT_e26_lhtight_nod0_ivarloose);
   if (fChain->GetListOfBranches()->Contains("HLT_e140_lhloose_nod0")) fChain->SetBranchAddress("HLT_e140_lhloose_nod0", &HLT_e140_lhloose_nod0, &b_HLT_e140_lhloose_nod0);
   if (fChain->GetListOfBranches()->Contains("HLT_mu50")) fChain->SetBranchAddress("HLT_mu50", &HLT_mu50, &b_HLT_mu50);
   if (fChain->GetListOfBranches()->Contains("HLT_e60_lhmedium")) fChain->SetBranchAddress("HLT_e60_lhmedium", &HLT_e60_lhmedium, &b_HLT_e60_lhmedium);
   if (fChain->GetListOfBranches()->Contains("HLT_e24_lhmedium_L1EM20VH")) fChain->SetBranchAddress("HLT_e24_lhmedium_L1EM20VH", &HLT_e24_lhmedium_L1EM20VH, &b_HLT_e24_lhmedium_L1EM20VH);
   if (fChain->GetListOfBranches()->Contains("HLT_e120_lhloose")) fChain->SetBranchAddress("HLT_e120_lhloose", &HLT_e120_lhloose, &b_HLT_e120_lhloose);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e60_lhmedium_nod0")) fChain->SetBranchAddress("el_trigMatch_HLT_e60_lhmedium_nod0", &el_trigMatch_HLT_e60_lhmedium_nod0, &b_el_trigMatch_HLT_e60_lhmedium_nod0);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e26_lhtight_nod0_ivarloose")) fChain->SetBranchAddress("el_trigMatch_HLT_e26_lhtight_nod0_ivarloose", &el_trigMatch_HLT_e26_lhtight_nod0_ivarloose, &b_el_trigMatch_HLT_e26_lhtight_nod0_ivarloose);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e140_lhloose_nod0")) fChain->SetBranchAddress("el_trigMatch_HLT_e140_lhloose_nod0", &el_trigMatch_HLT_e140_lhloose_nod0, &b_el_trigMatch_HLT_e140_lhloose_nod0);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e60_lhmedium")) fChain->SetBranchAddress("el_trigMatch_HLT_e60_lhmedium", &el_trigMatch_HLT_e60_lhmedium, &b_el_trigMatch_HLT_e60_lhmedium);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e24_lhmedium_L1EM20VH")) fChain->SetBranchAddress("el_trigMatch_HLT_e24_lhmedium_L1EM20VH", &el_trigMatch_HLT_e24_lhmedium_L1EM20VH, &b_el_trigMatch_HLT_e24_lhmedium_L1EM20VH);
   if (fChain->GetListOfBranches()->Contains("el_trigMatch_HLT_e120_lhloose")) fChain->SetBranchAddress("el_trigMatch_HLT_e120_lhloose", &el_trigMatch_HLT_e120_lhloose, &b_el_trigMatch_HLT_e120_lhloose);
   if (fChain->GetListOfBranches()->Contains("mu_trigMatch_HLT_mu26_ivarmedium")) fChain->SetBranchAddress("mu_trigMatch_HLT_mu26_ivarmedium", &mu_trigMatch_HLT_mu26_ivarmedium, &b_mu_trigMatch_HLT_mu26_ivarmedium);
   if (fChain->GetListOfBranches()->Contains("mu_trigMatch_HLT_mu50")) fChain->SetBranchAddress("mu_trigMatch_HLT_mu50", &mu_trigMatch_HLT_mu50, &b_mu_trigMatch_HLT_mu50);
   if (fChain->GetListOfBranches()->Contains("mu_trigMatch_HLT_mu20_iloose_L1MU15")) fChain->SetBranchAddress("mu_trigMatch_HLT_mu20_iloose_L1MU15", &mu_trigMatch_HLT_mu20_iloose_L1MU15, &b_mu_trigMatch_HLT_mu20_iloose_L1MU15);
   Notify();
}

Bool_t FlatTreeReader::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void FlatTreeReader::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t FlatTreeReader::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef FlatTreeReader_cxx
