
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

void HistoCreator::FillKLFitterHistos(EventExtras* iEntryExtrasInfo)
{
  
  float histoweight = iEntryExtrasInfo->GetEntryWeight();
  TLorentzVector goodLepton = iEntryExtrasInfo->GetGoodLepton();

  std::vector<TLorentzVector> bTaggedJets = iEntryExtrasInfo -> GetGoodSmallTags();

  TLorentzVector blep;
  TLorentzVector bhad;
  TLorentzVector lq1;
  TLorentzVector lq2;
  TLorentzVector lep;
  TLorentzVector nu;
  TLorentzVector Wlep;
  TLorentzVector Whad;

  TLorentzVector blep_original;;
  TLorentzVector bhad_original;;
  TLorentzVector lq1_original;
  TLorentzVector lq2_original;
  TLorentzVector Whad_original;
  TLorentzVector lb_original;


  if(fFlatTree -> klfitter_model_blep_pt  -> size() > 0){

    blep.SetPtEtaPhiE(fFlatTree -> klfitter_model_blep_pt  -> at(0), 
		      fFlatTree -> klfitter_model_blep_eta -> at(0), 
		      fFlatTree -> klfitter_model_blep_phi -> at(0), 
		      fFlatTree -> klfitter_model_blep_E   -> at(0));
    bhad.SetPtEtaPhiE(fFlatTree -> klfitter_model_bhad_pt  -> at(0), 
		      fFlatTree -> klfitter_model_bhad_eta -> at(0), 
		      fFlatTree -> klfitter_model_bhad_phi -> at(0), 
		      fFlatTree -> klfitter_model_bhad_E   -> at(0));
    lq1.SetPtEtaPhiE(fFlatTree -> klfitter_model_lq1_pt  -> at(0), 
		     fFlatTree -> klfitter_model_lq1_eta -> at(0), 
		     fFlatTree -> klfitter_model_lq1_phi -> at(0), 
		     fFlatTree -> klfitter_model_lq1_E   -> at(0));
    lq2.SetPtEtaPhiE(fFlatTree -> klfitter_model_lq2_pt  -> at(0), 
		     fFlatTree -> klfitter_model_lq2_eta -> at(0), 
		     fFlatTree -> klfitter_model_lq2_phi -> at(0), 
		     fFlatTree -> klfitter_model_lq2_E   -> at(0));
    lep.SetPtEtaPhiE(fFlatTree -> klfitter_model_lep_pt  -> at(0), 
		     fFlatTree -> klfitter_model_lep_eta -> at(0), 
		     fFlatTree -> klfitter_model_lep_phi -> at(0), 
		     fFlatTree -> klfitter_model_lep_E   -> at(0));
    nu.SetPtEtaPhiE(fFlatTree -> klfitter_model_nu_pt  -> at(0), 
		    fFlatTree -> klfitter_model_nu_eta -> at(0), 
		    fFlatTree -> klfitter_model_nu_phi -> at(0), 
		    fFlatTree -> klfitter_model_nu_E   -> at(0));
    
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


    Wlep = nu+lep;
    Whad = lq1+lq2;

    Whad_original = lq1_original + lq2_original;
    lb_original = goodLepton + blep_original;
    
    // get first all b-tagged jets, check if 1 or 2 are available, then calculate Rbq
    double Rbq = 0.0;
    
    if(bTaggedJets.size() == 1){
      
      Rbq = bTaggedJets[0].Pt()/((lq1_original.Pt()+lq2_original.Pt())*0.5);
      
    }
    else if (bTaggedJets.size() >= 2){
      
      Rbq = (bTaggedJets[0].Pt() + bTaggedJets[1].Pt())/(lq1_original.Pt()+lq2_original.Pt());
      
    }

    int   nr_param   = (fFlatTree -> klfitter_parameters -> at(0)).size();
    float mtop_param = (fFlatTree -> klfitter_parameters -> at(0))[nr_param-1];    

    for(unsigned int iVar = 0; iVar < fVar.size(); ++iVar){    

      if(fVariables[iVar] == "klf_topLep_pt")    
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topLep_pt,  histoweight);
      if(fVariables[iVar] == "klf_topLep_eta")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topLep_eta, histoweight);
      if(fVariables[iVar] == "klf_topLep_phi")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topLep_phi, histoweight);
      if(fVariables[iVar] == "klf_topLep_E")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topLep_E,   histoweight);
      if(fVariables[iVar] == "klf_topLep_m"){
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topLep_m,   histoweight);
	fTreeVariables[iVar] = fFlatTree -> klfitter_bestPerm_topLep_m;
      }
      if(fVariables[iVar] == "klf_topHad_pt")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topHad_pt,  histoweight);
      if(fVariables[iVar] == "klf_topHad_eta")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topHad_eta, histoweight);
      if(fVariables[iVar] == "klf_topHad_phi")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topHad_phi, histoweight);
      if(fVariables[iVar] == "klf_topHad_E")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topHad_E,   histoweight);
      if(fVariables[iVar] == "klf_topHad_m"){
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_topHad_m,   histoweight);
	fTreeVariables[iVar] = fFlatTree -> klfitter_bestPerm_topHad_m;
      }
      if(fVariables[iVar] == "klf_ttbar_pt")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_ttbar_pt,   histoweight);
      if(fVariables[iVar] == "klf_ttbar_eta")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_ttbar_eta,  histoweight);
      if(fVariables[iVar] == "klf_ttbar_phi")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_ttbar_phi,  histoweight);
      if(fVariables[iVar] == "klf_ttbar_E")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_ttbar_E,    histoweight);
      if(fVariables[iVar] == "klf_ttbar_m")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_bestPerm_ttbar_m,    histoweight);
      if(fVariables[iVar] == "klf_Wlep_pt")
	fHistoVector[iVar].Fill(Wlep.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_Wlep_eta")
	fHistoVector[iVar].Fill(Wlep.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_Wlep_phi")
	fHistoVector[iVar].Fill(Wlep.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_Wlep_m")
	fHistoVector[iVar].Fill(Wlep.M(),     histoweight);
      if(fVariables[iVar] == "klf_Whad_pt")
	fHistoVector[iVar].Fill(Whad.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_Whad_eta")
	fHistoVector[iVar].Fill(Whad.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_Whad_phi")
	fHistoVector[iVar].Fill(Whad.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_Whad_m"){
	fHistoVector[iVar].Fill(Whad.M(),     histoweight);
	fTreeVariables[iVar] = Whad.M();
      }
      if(fVariables[iVar] == "klf_blep_pt")
	fHistoVector[iVar].Fill(blep.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_blep_eta")
	fHistoVector[iVar].Fill(blep.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_blep_phi")
	fHistoVector[iVar].Fill(blep.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_blep_m")
	fHistoVector[iVar].Fill(blep.M(),     histoweight);
      if(fVariables[iVar] == "klf_bhad_pt")
	fHistoVector[iVar].Fill(bhad.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_bhad_eta")
	fHistoVector[iVar].Fill(bhad.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_bhad_phi")
	fHistoVector[iVar].Fill(bhad.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_bhad_m")
	fHistoVector[iVar].Fill(bhad.M(),     histoweight);
      if(fVariables[iVar] == "klf_lq1_pt")
	fHistoVector[iVar].Fill(lq1.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_lq1_eta")
	fHistoVector[iVar].Fill(lq1.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_lq1_phi")
	fHistoVector[iVar].Fill(lq1.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_lq1_m")
	fHistoVector[iVar].Fill(lq1.M(),     histoweight);
      if(fVariables[iVar] == "klf_lq2_pt")
	fHistoVector[iVar].Fill(lq2.Pt(),    histoweight);
      if(fVariables[iVar] == "klf_lq2_eta")
	fHistoVector[iVar].Fill(lq2.Eta(),   histoweight);
      if(fVariables[iVar] == "klf_lq2_phi")
	fHistoVector[iVar].Fill(lq2.Phi(),   histoweight);
      if(fVariables[iVar] == "klf_lq2_m")
	fHistoVector[iVar].Fill(lq2.M(),     histoweight);
      if(fVariables[iVar] == "klf_LL")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_logLikelihood -> at(0),    histoweight);
      if(fVariables[iVar] == "klf_eventProbability")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_eventProbability -> at(0), histoweight);
      if(fVariables[iVar] == "klf_minuitDidNotConverge")
	fHistoVector[iVar].Fill(fFlatTree -> klfitter_minuitDidNotConverge -> at(0), histoweight);
      if(fVariables[iVar] == "klf_mtop_param")
	fHistoVector[iVar].Fill(mtop_param, histoweight);
      

      //Observables using original 4-vectors
      if(fVariables[iVar] == "klf_original_Whad_m"){
	fHistoVector[iVar].Fill(Whad_original.M(),     histoweight);
	fTreeVariables[iVar] = Whad_original.M();
      }
      if(fVariables[iVar] == "klf_original_Rbq_reco"){
	fHistoVector[iVar].Fill(Rbq, histoweight); 
	fTreeVariables[iVar] = Rbq;
      }
      if(fVariables[iVar] == "klf_original_mlb_reco"){
	fHistoVector[iVar].Fill(lb_original.M(), histoweight); 
	fTreeVariables[iVar] = lb_original.M();
      }

      if(fVariables[iVar] == "klf_window_mw_reco"){
	fHistoVector[iVar].Fill(Whad_original.M(),     histoweight);
        fTreeVariables[iVar] = Whad_original.M();
      }
      
      if(fVariables[iVar] == "klf_window_rbq_reco"){
	fHistoVector[iVar].Fill(Rbq, histoweight);
        fTreeVariables[iVar] = Rbq;
      }
      
      if(fVariables[iVar] == "klf_window_mtop_reco" ){
	fHistoVector[iVar].Fill(mtop_param, histoweight);
	fTreeVariables[iVar] = mtop_param;
      }
      
      
      
    }
    
  
 
  }

}


