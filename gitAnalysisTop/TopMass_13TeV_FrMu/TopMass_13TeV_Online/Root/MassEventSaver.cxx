/*
  Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
*/

#include "TopMass_13TeV_Online/MassEventSaver.h"
#include "TopMass_13TeV_Online/NeutrinoWeighter.h"
#include "TopEvent/Event.h"
#include "TopEventSelectionTools/TreeManager.h"
#include "TopParticleLevel/ParticleLevelEvent.h"
#include "TopConfiguration/TopConfig.h"

#include <TRandom3.h>


namespace top{
  ///-- Construcutor --///
  MassEventSaver::MassEventSaver() :
    pseudotop(true),
    m_tma_pseudotop0_mtop_param(0.),
    m_tma_pseudotop1_mtop_param(0.),
    m_tma_pseudotop2_mtop_param(0.),
    m_tma_pseudotop3_mtop_param(0.),
    m_tma_pseudotop_mw(0.),
    m_tma_pseudotop_rbq(0.),
    m_tma_nbjets(0.),
    m_tma_njets(0.),
    m_tma_etdr(0.),
    m_tma_met(0.),
    m_tma_met_ex(0.),
    m_tma_met_ey(0.),
    m_tma_met_phi(0.),
    m_tma_mlb_minavg(0.),
    m_tma_mlb_minavglow(0.),
    m_tma_mlb_minavghigh(0.),
    m_tma_mlb_minmax(0.),
    m_tma_mlb_minmaxlow(0.),
    m_tma_mlb_minmaxavg(0.),
    m_tma_pTlb_1(0.),
    m_tma_pTlb_2(0.),
    m_tma_dRlb_1(0.),
    m_tma_dRlb_2(0.),
    m_tma_mll(0.),
    m_tma_pTll(0.),
    m_tma_dRll(0.),
    m_tma_mbb(0.),
    m_tma_pTbb(0.),
    m_tma_dRbb(0.),
    m_tma_Rbq_avgLJ(0.),
    m_tma_Rbq_leadLJ(0.),
    m_tma_top_pt(0.),
    m_tma_top_eta(0.),
    m_tma_top_phi(0.),
    m_tma_top_m(0.),
    m_tma_top_e(0.),
    m_tma_top_y(0.),
    m_tma_tbar_pt(0.),
    m_tma_tbar_eta(0.),
    m_tma_tbar_phi(0.),
    m_tma_tbar_m(0.),
    m_tma_tbar_e(0.),
    m_tma_tbar_y(0.),
    m_tma_av_top_pt (0.),
    m_tma_av_top_eta(0.),
    m_tma_av_top_phi(0.),
    m_tma_av_top_m(0.),
    m_tma_av_top_e(0.),
    m_tma_av_top_y(0.),
    m_tma_ttbar_pt(0.),
    m_tma_ttbar_eta(0.),
    m_tma_ttbar_phi(0.),
    m_tma_ttbar_m(0.),
    m_tma_ttbar_e(0.),
    m_tma_ttbar_y(0.),
    m_tma_ttbar_pout(0.),
    m_tma_nu_pt(0.),
    m_tma_nu_eta(0.),
    m_tma_nu_phi(0.),
    m_tma_nu_m(0.),
    m_tma_nu_e(0.),
    m_tma_nu_y(0.),
    m_tma_nubar_pt(0.),
    m_tma_nubar_eta(0.),
    m_tma_nubar_phi(0.),
    m_tma_nubar_m(0.),
    m_tma_nubar_e(0.),
    m_tma_nubar_y(0.),

    m_tma_particle_pseudotop0_mtop_param(0.),
    m_tma_particle_pseudotop1_mtop_param(0.),
    m_tma_particle_pseudotop2_mtop_param(0.),
    m_tma_particle_pseudotop3_mtop_param(0.),
    m_tma_particle_pseudotop_mw(0.),
    m_tma_particle_pseudotop_rbq(0.),
    m_tma_particle_nbjets(0.),
    m_tma_particle_njets(0.),
    m_tma_particle_etdr(0.),
    m_tma_particle_met(0.),
    m_tma_particle_met_ex(0.),
    m_tma_particle_met_ey(0.),
    m_tma_particle_met_phi(0.),
    m_tma_particle_mlb_minavg(0.),
    m_tma_particle_mlb_minavglow(0.),
    m_tma_particle_mlb_minavghigh(0.),
    m_tma_particle_mlb_minmax(0.),
    m_tma_particle_mlb_minmaxlow(0.),
    m_tma_particle_mlb_minmaxavg(0.),
    m_tma_particle_pTlb_1(0.),
    m_tma_particle_pTlb_2(0.),
    m_tma_particle_dRlb_1(0.),
    m_tma_particle_dRlb_2(0.),
    m_tma_particle_mll(0.),
    m_tma_particle_pTll(0.),
    m_tma_particle_dRll(0.),
    m_tma_particle_mbb(0.),
    m_tma_particle_pTbb(0.),
    m_tma_particle_dRbb(0.),
    m_tma_particle_top_pt(0.),
    m_tma_particle_top_eta(0.),
    m_tma_particle_top_phi(0.),
    m_tma_particle_top_m(0.),
    m_tma_particle_top_e(0.),
    m_tma_particle_top_y(0.),
    m_tma_particle_tbar_pt(0.),
    m_tma_particle_tbar_eta(0.),
    m_tma_particle_tbar_phi(0.),
    m_tma_particle_tbar_m(0.),
    m_tma_particle_tbar_e(0.),
    m_tma_particle_tbar_y(0.),
    m_tma_particle_av_top_pt (0.),
    m_tma_particle_av_top_eta(0.),
    m_tma_particle_av_top_phi(0.),
    m_tma_particle_av_top_m(0.),
    m_tma_particle_av_top_e(0.),
    m_tma_particle_av_top_y(0.),
    m_tma_particle_ttbar_pt(0.),
    m_tma_particle_ttbar_eta(0.),
    m_tma_particle_ttbar_phi(0.),
    m_tma_particle_ttbar_m(0.),
    m_tma_particle_ttbar_e(0.),
    m_tma_particle_ttbar_y(0.),
    m_tma_particle_ttbar_pout(0.),
    m_tma_particle_nu_pt(0.),
    m_tma_particle_nu_eta(0.),
    m_tma_particle_nu_phi(0.),
    m_tma_particle_nu_m(0.),
    m_tma_particle_nu_e(0.),
    m_tma_particle_nu_y(0.),
    m_tma_particle_nubar_pt(0.),
    m_tma_particle_nubar_eta(0.),
    m_tma_particle_nubar_phi(0.),
    m_tma_particle_nubar_m(0.),
    m_tma_particle_nubar_e(0.),
    m_tma_particle_nubar_y(0.)
  {
  }
  
  ///-- initialize - done once at the start of a job before the loop over events --///
  void MassEventSaver::initialize(std::shared_ptr<top::TopConfig> config, TFile* file, const std::vector<std::string>& extraBranches)
{
    ///-- Let the base class do all the hard work --///
    ///-- It will setup TTrees for each systematic with a standard set of variables --///
    top::EventSaverFlatNtuple::initialize(config, file, extraBranches);
    
    ///-- Loop over the systematic TTrees and add the custom variables --///
    for (auto systematicTree : treeManagers()) {

      // "tma" stands here for "top mass analysis"
      systematicTree->makeOutputVariable(m_tma_klfitter_mtop_param, "tma_klfitter_mtop_param");
      systematicTree->makeOutputVariable(m_tma_original_mw,         "tma_original_mw");
      systematicTree->makeOutputVariable(m_tma_original_rbq,        "tma_original_rbq");
      systematicTree->makeOutputVariable(m_tma_pseudotop0_mtop_param, "tma_pseudotop0_mtop_param");
      systematicTree->makeOutputVariable(m_tma_pseudotop1_mtop_param, "tma_pseudotop1_mtop_param");
      systematicTree->makeOutputVariable(m_tma_pseudotop2_mtop_param, "tma_pseudotop2_mtop_param");
      systematicTree->makeOutputVariable(m_tma_pseudotop3_mtop_param, "tma_pseudotop3_mtop_param");
      systematicTree->makeOutputVariable(m_tma_pseudotop_mw,         "tma_pseudotop_mw");
      systematicTree->makeOutputVariable(m_tma_pseudotop_rbq,        "tma_pseudotop_rbq");
      systematicTree->makeOutputVariable(m_tma_bjet_pt,             "tma_bjet_pt");
      systematicTree->makeOutputVariable(m_tma_bjet_eta,            "tma_bjet_eta");
      systematicTree->makeOutputVariable(m_tma_bjet_phi,            "tma_bjet_phi");
      systematicTree->makeOutputVariable(m_tma_bjet_e,              "tma_bjet_e");
      systematicTree->makeOutputVariable(m_tma_nbjets,              "tma_nbjets");


      // plots for dilepton channel: reco-level                                                                                                                                                                        
      systematicTree->makeOutputVariable(m_tma_etdr,           "tma_etdr");
      systematicTree->makeOutputVariable(m_tma_met,            "tma_met");
      systematicTree->makeOutputVariable(m_tma_met_ex,         "tma_met_ex");
      systematicTree->makeOutputVariable(m_tma_met_ey,         "tma_met_ey");
      systematicTree->makeOutputVariable(m_tma_met_phi,        "tma_met_phi");
      systematicTree->makeOutputVariable(m_tma_njets,          "tma_njets");
      systematicTree->makeOutputVariable(m_tma_jet_pt,         "tma_jet_pt");
      systematicTree->makeOutputVariable(m_tma_jet_eta,        "tma_jet_eta");
      systematicTree->makeOutputVariable(m_tma_jet_phi,        "tma_jet_phi");
      systematicTree->makeOutputVariable(m_tma_jet_e,          "tma_jet_e");
      systematicTree->makeOutputVariable(m_tma_mlb_minavg,     "tma_mlb_minavg");
      systematicTree->makeOutputVariable(m_tma_mlb_minavglow,  "tma_mlb_minavglow");
      systematicTree->makeOutputVariable(m_tma_mlb_minavghigh, "tma_mlb_minavghigh");
      systematicTree->makeOutputVariable(m_tma_mlb_minmax,     "tma_mlb_minmax");
      systematicTree->makeOutputVariable(m_tma_mlb_minmaxlow,  "tma_mlb_minmaxlow");
      systematicTree->makeOutputVariable(m_tma_mlb_minmaxavg,  "tma_mlb_minmaxavg");
      systematicTree->makeOutputVariable(m_tma_pTlb_1,         "tma_pTlb_1");
      systematicTree->makeOutputVariable(m_tma_pTlb_2,         "tma_pTlb_2");
      systematicTree->makeOutputVariable(m_tma_dRlb_1,         "tma_dRlb_1");
      systematicTree->makeOutputVariable(m_tma_dRlb_2,         "tma_dRlb_2");
      systematicTree->makeOutputVariable(m_tma_mll,            "tma_mll");
      systematicTree->makeOutputVariable(m_tma_pTll,           "tma_pTll");
      systematicTree->makeOutputVariable(m_tma_dRll,           "tma_dRll");
      systematicTree->makeOutputVariable(m_tma_mbb,            "tma_mbb");
      systematicTree->makeOutputVariable(m_tma_pTbb,           "tma_pTbb"); 
      systematicTree->makeOutputVariable(m_tma_dRbb,           "tma_dRbb");
      systematicTree->makeOutputVariable(m_tma_Rbq_avgLJ,      "tma_Rbq_avgLJ");
      systematicTree->makeOutputVariable(m_tma_Rbq_leadLJ,     "tma_Rbq_leadLJ");

      // top reco level

      systematicTree->makeOutputVariable(m_weight_max,                        "m_weight_max");

      systematicTree->makeOutputVariable(m_tma_top_pt,                        "tma_top_pt");
      systematicTree->makeOutputVariable(m_tma_top_eta,                       "tma_top_eta");
      systematicTree->makeOutputVariable(m_tma_top_phi,                       "tma_top_phi");
      systematicTree->makeOutputVariable(m_tma_top_e,                         "tma_top_e");
      systematicTree->makeOutputVariable(m_tma_top_m,                         "tma_top_m");
      systematicTree->makeOutputVariable(m_tma_top_y,                         "tma_top_y");

      systematicTree->makeOutputVariable(m_tma_tbar_pt,                       "tma_tbar_pt");
      systematicTree->makeOutputVariable(m_tma_tbar_eta,                      "tma_tbar_eta");
      systematicTree->makeOutputVariable(m_tma_tbar_phi,                      "tma_tbar_phi");
      systematicTree->makeOutputVariable(m_tma_tbar_e,                        "tma_tbar_e");
      systematicTree->makeOutputVariable(m_tma_tbar_m,                        "tma_tbar_m");
      systematicTree->makeOutputVariable(m_tma_tbar_y,                        "tma_tbar_y");

      systematicTree->makeOutputVariable(m_tma_av_top_pt,                        "tma_av_top_pt");
      systematicTree->makeOutputVariable(m_tma_av_top_eta,                       "tma_av_top_eta");
      systematicTree->makeOutputVariable(m_tma_av_top_phi,                       "tma_av_top_phi");
      systematicTree->makeOutputVariable(m_tma_av_top_e,                         "tma_av_top_e");
      systematicTree->makeOutputVariable(m_tma_av_top_m,                         "tma_av_top_m");
      systematicTree->makeOutputVariable(m_tma_av_top_y,                         "tma_av_top_y");

      systematicTree->makeOutputVariable(m_tma_ttbar_pt,                      "tma_ttbar_pt");
      systematicTree->makeOutputVariable(m_tma_ttbar_eta,                     "tma_ttbar_eta");
      systematicTree->makeOutputVariable(m_tma_ttbar_phi,                     "tma_ttbar_phi");
      systematicTree->makeOutputVariable(m_tma_ttbar_e,                       "tma_ttbar_e");
      systematicTree->makeOutputVariable(m_tma_ttbar_m,                       "tma_ttbar_m");
      systematicTree->makeOutputVariable(m_tma_ttbar_y,                       "tma_ttbar_y");
      systematicTree->makeOutputVariable(m_tma_ttbar_pout,                    "tma_ttbar_pout");

      systematicTree->makeOutputVariable(m_tma_nu_pt,                         "tma_nu_pt");
      systematicTree->makeOutputVariable(m_tma_nu_eta,                        "tma_nu_eta");
      systematicTree->makeOutputVariable(m_tma_nu_phi,                        "tma_nu_phi");
      systematicTree->makeOutputVariable(m_tma_nu_e,                          "tma_nu_e");
      systematicTree->makeOutputVariable(m_tma_nu_m,                          "tma_nu_m");
      systematicTree->makeOutputVariable(m_tma_nu_y,                          "tma_nu_y");

      systematicTree->makeOutputVariable(m_tma_nubar_pt,                      "tma_nubar_pt");
      systematicTree->makeOutputVariable(m_tma_nubar_eta,                     "tma_nubar_eta");
      systematicTree->makeOutputVariable(m_tma_nubar_phi,                     "tma_nubar_phi");
      systematicTree->makeOutputVariable(m_tma_nubar_e,                       "tma_nubar_e");
      systematicTree->makeOutputVariable(m_tma_nubar_m,                       "tma_nubar_m");
      systematicTree->makeOutputVariable(m_tma_nubar_y,                       "tma_nubar_y");

      systematicTree->makeOutputVariable(m_tma_Wp_pt,                         "tma_Wp_pt");
      systematicTree->makeOutputVariable(m_tma_Wp_eta,                        "tma_Wp_eta");
      systematicTree->makeOutputVariable(m_tma_Wp_phi,                        "tma_Wp_phi");
      systematicTree->makeOutputVariable(m_tma_Wp_e,                          "tma_Wp_e");
      systematicTree->makeOutputVariable(m_tma_Wp_m,                          "tma_Wp_m");
      systematicTree->makeOutputVariable(m_tma_Wp_y,                          "tma_Wp_y");

      systematicTree->makeOutputVariable(m_tma_Wm_pt,                         "tma_Wm_pt");
      systematicTree->makeOutputVariable(m_tma_Wm_eta,                        "tma_Wm_eta");
      systematicTree->makeOutputVariable(m_tma_Wm_phi,                        "tma_Wm_phi");
      systematicTree->makeOutputVariable(m_tma_Wm_e,                          "tma_Wm_e");
      systematicTree->makeOutputVariable(m_tma_Wm_m,                          "tma_Wm_m");
      systematicTree->makeOutputVariable(m_tma_Wm_y,                          "tma_Wm_y");

    }

  if ( topConfig()->doTopParticleLevel() ){

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop0_mtop_param, "tma_pseudotop0_mtop_param");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop1_mtop_param, "tma_pseudotop1_mtop_param");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop2_mtop_param, "tma_pseudotop2_mtop_param");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop3_mtop_param, "tma_pseudotop3_mtop_param");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop_mw,         "tma_pseudotop_mw");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pseudotop_rbq,        "tma_pseudotop_rbq");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_etdr,                 "tma_etdr");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_met,                  "tma_met");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_met_ex,               "tma_met_ex");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_met_ey,               "tma_met_ey");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_met_phi,              "tma_met_phi");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nbjets,               "tma_nbjets");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_bjet_pt,              "tma_bjet_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_bjet_eta,             "tma_bjet_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_bjet_phi,             "tma_bjet_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_bjet_e,               "tma_bjet_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_njets,                "tma_njets");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_jet_pt,               "tma_jet_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_jet_eta,              "tma_jet_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_jet_phi,              "tma_jet_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_jet_e,                "tma_jet_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minavg,           "tma_mlb_minavg");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minavglow,        "tma_mlb_minavglow");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minavghigh,       "tma_mlb_minavghigh");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minmax,           "tma_mlb_minmax");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minmaxlow,        "tma_mlb_minmaxlow");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mlb_minmaxavg,        "tma_mlb_minmaxavg");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pTlb_1,               "tma_pTlb_1");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pTlb_2,               "tma_pTlb_2");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_dRlb_1,               "tma_dRlb_1");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_dRlb_2,               "tma_dRlb_2");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mll,                  "tma_mll");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pTll,                 "tma_pTll");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_dRll,                 "tma_dRll");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_mbb,                  "tma_mbb");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_pTbb,                 "tma_pTbb");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_dRbb,                 "tma_dRbb");


      // Pseudo-top

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_pt,               "tma_top_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_eta,              "tma_top_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_phi,              "tma_top_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_e,                "tma_top_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_m,                "tma_top_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_top_y,                "tma_top_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_pt,              "tma_tbar_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_eta,             "tma_tbar_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_phi,             "tma_tbar_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_e,               "tma_tbar_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_m,               "tma_tbar_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_tbar_y,               "tma_tbar_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_pt,            "tma_av_top_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_eta,           "tma_av_top_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_phi,           "tma_av_top_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_e,             "tma_av_top_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_m,             "tma_av_top_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_av_top_y,             "tma_av_top_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_pt,             "tma_ttbar_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_eta,            "tma_ttbar_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_phi,            "tma_ttbar_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_e,              "tma_ttbar_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_m,              "tma_ttbar_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_y,              "tma_ttbar_y");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_ttbar_pout,           "tma_ttbar_pout");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_n,                 "tma_nu_n");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_pt,                "tma_nu_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_eta,               "tma_nu_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_phi,               "tma_nu_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_e,                 "tma_nu_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_m,                 "tma_nu_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nu_y,                 "tma_nu_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_pt,             "tma_nubar_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_eta,            "tma_nubar_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_phi,            "tma_nubar_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_e,              "tma_nubar_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_m,              "tma_nubar_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_nubar_y,              "tma_nubar_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_pt,                "tma_Wp_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_eta,               "tma_Wp_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_phi,               "tma_Wp_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_e,                 "tma_Wp_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_m,                 "tma_Wp_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wp_y,                 "tma_Wp_y");

      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_pt,                "tma_Wm_pt");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_eta,               "tma_Wm_eta");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_phi,               "tma_Wm_phi");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_e,                 "tma_Wm_e");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_m,                 "tma_Wm_m");
      particleLevelTreeManager()->makeOutputVariable(m_tma_particle_Wm_y,                 "tma_Wm_y");


  }
}
  
  ///-- saveEvent - run for every systematic and every event --///
  void MassEventSaver::saveEvent(const top::Event& event) 
  {
    // calculate here now the flat variables neccessary for the top mass analysis, want to avoid to recalculate them every time offline!
    m_tma_nbjets = 0; 
    m_tma_njets = 0; 

    m_tma_mlb_minavg = 0.;

    m_tma_bjet_pt.clear();
    m_tma_bjet_eta.clear();
    m_tma_bjet_phi.clear();
    m_tma_bjet_e.clear();

    m_tma_jet_pt.clear();
    m_tma_jet_eta.clear();
    m_tma_jet_phi.clear();
    m_tma_jet_e.clear();

    // get vector of b-tagged jets
    for (const auto* const jetPtr : event.m_jets) {
      
      //if(jetPtr->isAvailable<char>("isbtagged_FixedCutBEff_77"))

      m_tma_njets++;

      const xAOD::BTagging* btag(nullptr);
      btag = jetPtr->btagging();	
      double mvx = -999;
      if (btag) btag->MVx_discriminant("MV2c10", mvx);

      if(mvx > 0.64)
	m_tma_nbjets++;
      
    }

    m_tma_bjet_pt.resize(m_tma_nbjets);
    m_tma_bjet_eta.resize(m_tma_nbjets);
    m_tma_bjet_phi.resize(m_tma_nbjets);
    m_tma_bjet_e.resize(m_tma_nbjets);

    m_tma_jet_pt.resize(m_tma_njets);
    m_tma_jet_eta.resize(m_tma_njets);
    m_tma_jet_phi.resize(m_tma_njets);
    m_tma_jet_e.resize(m_tma_njets);

    int i = 0;
    int j = 0;

    std::vector<TLorentzVector> bJets;
    std::vector<TLorentzVector> LJets;
    std::vector<double> LJets_mvx;
    for (const auto* const jetPtr : event.m_jets) {

      m_tma_jet_pt[j]	= jetPtr->pt();
      m_tma_jet_eta[j]	= jetPtr->eta();
      m_tma_jet_phi[j]	= jetPtr->phi();
      m_tma_jet_e[j]	= jetPtr->e();

      ++j;

      const xAOD::BTagging* btag(nullptr);
      btag = jetPtr->btagging();
      double mvx = -999;
      if(btag) btag->MVx_discriminant("MV2c10", mvx);
      if(mvx > 0.64){
	  
	m_tma_bjet_pt[i]  = jetPtr->pt();
	m_tma_bjet_eta[i] = jetPtr->eta();
	m_tma_bjet_phi[i] = jetPtr->phi();
	m_tma_bjet_e[i]   = jetPtr->e();
	   
	TLorentzVector help;
	help.SetPtEtaPhiE(jetPtr->pt(), jetPtr->eta(), jetPtr->phi(), jetPtr->e());
 
	bJets.push_back(help);

	++i;
      
      }
      else{
	
	TLorentzVector help;
	help.SetPtEtaPhiE(jetPtr->pt(), jetPtr->eta(), jetPtr->phi(), jetPtr->e());
 
	LJets.push_back(help);	
	LJets_mvx.push_back(mvx);	
	
      }

    }

    TLorentzVector blep_original;;
    TLorentzVector bhad_original;;
    TLorentzVector lq1_original;
    TLorentzVector lq2_original;
    TLorentzVector Whad_original;

    int nPermutations  = 0; 
    bool validKLFitter = false;

    if (event.m_KLFitterResults != nullptr) {
      
      validKLFitter = true;
      nPermutations = event.m_KLFitterResults->size();
      
    }

    m_tma_klfitter_mtop_param.resize(nPermutations);
    m_tma_original_mw.resize(nPermutations);
    m_tma_original_rbq.resize(nPermutations);

    int iPerm = 0;

    if (validKLFitter) {

      for (const auto* const klPtr : *event.m_KLFitterResults) {


	int blep_index = klPtr->model_blep_jetIndex();
	int bhad_index = klPtr->model_bhad_jetIndex();
	int lq1_index  = klPtr->model_lq1_jetIndex();
	int lq2_index  = klPtr->model_lq2_jetIndex();

	blep_original.SetPtEtaPhiE(event.m_jets.at(blep_index) -> pt()/1000.0,
				   event.m_jets.at(blep_index) -> eta(),
				   event.m_jets.at(blep_index) -> phi(),
				   event.m_jets.at(blep_index) -> e()/1000.0);

	bhad_original.SetPtEtaPhiE(event.m_jets.at(bhad_index) -> pt()/1000.0,
				   event.m_jets.at(bhad_index) -> eta(),
                                   event.m_jets.at(bhad_index) -> phi(),
				   event.m_jets.at(bhad_index) -> e()/1000.0);

	lq1_original.SetPtEtaPhiE(event.m_jets.at(lq1_index) -> pt()/1000.0,
				   event.m_jets.at(lq1_index) -> eta(),
                                   event.m_jets.at(lq1_index) -> phi(),
				   event.m_jets.at(lq1_index) -> e()/1000.0);

	lq2_original.SetPtEtaPhiE(event.m_jets.at(lq2_index) -> pt()/1000.0,
				   event.m_jets.at(lq2_index) -> eta(),
                                   event.m_jets.at(lq2_index) -> phi(),
				   event.m_jets.at(lq2_index) -> e()/1000.0);

	
	Whad_original = lq1_original + lq2_original;

	m_tma_original_mw[iPerm] = Whad_original.M();
	
	if(m_tma_nbjets == 1){
	  m_tma_original_rbq[iPerm] = m_tma_bjet_pt[0]/1000.0/((lq1_original.Pt()+lq2_original.Pt())*0.5);
	}
	else if(m_tma_nbjets >= 2){
	  m_tma_original_rbq[iPerm] = (m_tma_bjet_pt[0] + m_tma_bjet_pt[1])/1000.0/(lq1_original.Pt()+lq2_original.Pt());
	}

	int nr_param = klPtr->parameters().size();
	m_tma_klfitter_mtop_param[iPerm] = klPtr->parameters().at(nr_param-1);
	
	// std::cout << m_tma_original_mw[iPerm] << "\t" << m_tma_original_rbq[iPerm] << "\t" << m_tma_klfitter_mtop_param[iPerm] << std::endl;  
		
	++iPerm;
	
      }
      
    }

    std::vector<TLorentzVector> goodLeptons;
    std::vector<TLorentzVector> goodElectrons;
    std::vector<TLorentzVector> goodMuons;

    TLorentzVector lep_pos, lep_neg, top, tbar, ttbar, nu, nubar;
    bool lep_pos_set = false;
    bool lep_neg_set = false;

    for (const auto* const elPtr : event.m_electrons) {

      TLorentzVector help;
      help.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());

      if (elPtr->charge() > 0) {
	lep_pos.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());
	lep_pos_set = true; }

      else if (elPtr->charge() < 0) {
	lep_neg.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());
	lep_neg_set = true; }

      goodLeptons.push_back(help);
      goodElectrons.push_back(help);

    }
    for (const auto* const muPtr : event.m_muons) {

      TLorentzVector help;
      help.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());

      if (muPtr->charge() > 0) {
	lep_pos.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());
	lep_pos_set = true; }

      else if (muPtr->charge() < 0) {
	lep_neg.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());
	lep_neg_set = true; }

      goodLeptons.push_back(help);
      goodMuons.push_back(help);

    }

    m_tma_met	    = event.m_met->met();
    m_tma_met_ex    = event.m_met->mpx();
    m_tma_met_ey    = event.m_met->mpy();
    m_tma_met_phi   = event.m_met->phi();

    if (goodLeptons.size() == 1 && LJets.size() >= 2) {

       if (m_tma_nbjets >= 2){
         TLorentzVector lep = goodLeptons.at(0);
         TLorentzVector pb_lep, pb_had;
         if (bJets[0].DeltaR(lep) < bJets[1].DeltaR(lep)){
           pb_lep = bJets[0];
           pb_had = bJets[1];
         }
         else {
           pb_lep = bJets[1];
           pb_had = bJets[0];
         }

	 // Pseudo-top definitions

         TLorentzVector miss, t_lep, t_had;
         t_had = pb_had + LJets[0] + LJets[1];
         m_tma_pseudotop_mw = (LJets[0] + LJets[1]).M();
         m_tma_pseudotop_rbq = (pb_lep.Pt() + pb_had.Pt())/(LJets[0].Pt() + LJets[1].Pt());

         Double_t mW = 80.309;
         Double_t lE = lep.E();
         Double_t lX = lep.Px();
         Double_t lY = lep.Py();
         Double_t lZ = lep.Pz();

         Double_t nuE = event.m_met->met();
         Double_t nuX = event.m_met->mpx();
         Double_t nuY = event.m_met->mpy();

         Double_t wPz2 = pow(lE + nuE,2) - pow(lX + nuX,2) - pow(lY + nuY,2) - pow(mW,2);
         Double_t nuZ = 0.;

	 // Pseudo-top def. 0 (default)
         if (wPz2 >= 0.) nuZ = abs(sqrt(wPz2) - lZ) <= abs(-sqrt(wPz2) - lZ) ? (sqrt(wPz2) - lZ) : (-sqrt(wPz2) - lZ);
         else nuZ = -lZ;

         miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
         t_lep = pb_lep + lep + miss;
         m_tma_pseudotop0_mtop_param = 0.5*(t_lep.M() + t_had.M());

	 if ( pseudotop == true ) {

	   // Pseudo-top def. 1

	   if (wPz2 >= 0.) nuZ = abs(sqrt(wPz2) - lZ) >= abs(-sqrt(wPz2) - lZ) ? (sqrt(wPz2) - lZ) : (-sqrt(wPz2) - lZ);
           else nuZ = -lZ;

           miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           t_lep = pb_lep + lep + miss;
           m_tma_pseudotop1_mtop_param = 0.5*(t_lep.M() + t_had.M());

	   // Pseudo-top def. 2

	   Double_t nuZ_1 = sqrt(wPz2) - lZ;
	   Double_t nuZ_2 = -sqrt(wPz2) - lZ;
	   TLorentzVector miss_1, miss_2;
	   miss_1.SetPxPyPzE(nuX, nuY, nuZ_1, nuE);
	   miss_2.SetPxPyPzE(nuX, nuY, nuZ_2, nuE);
	   TLorentzVector tlep_1 = pb_lep + lep + miss_1;
	   TLorentzVector tlep_2 = pb_lep + lep + miss_2;

	   nuZ = abs(tlep_1.M() - t_had.M()) <= abs(tlep_2.M() - t_had.M()) ? nuZ_1 : nuZ_2;

           miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           t_lep = pb_lep + lep + miss;
           m_tma_pseudotop2_mtop_param = 0.5*(t_lep.M() + t_had.M());

	   // Pseudo-top def. 3

	   Double_t bE = pb_lep.E();
	   Double_t bX = pb_lep.Px();
	   Double_t bY = pb_lep.Py();
	   Double_t bZ = pb_lep.Pz();

	   Double_t tPz2 = pow(bZ,2) - pow(pb_lep.M(),2) - pow(t_had.M(),2)
		+ pow(lE + nuE,2) - pow(lX + nuX,2) - pow(lY + nuY,2)
		+ 2*( (lE + nuE)*bE - (lX + nuX)*bX - (lY + nuY)*bY );
	   if (tPz2 >= 0.) nuZ = abs(sqrt(tPz2) - (lZ + bZ)) <= abs(-sqrt(tPz2) - (lZ + bZ)) ? (sqrt(tPz2) - (lZ + bZ)) : (-sqrt(tPz2) - (lZ + bZ));
	   else nuZ = - (lZ + bZ);

           miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           t_lep = pb_lep + lep + miss;
           m_tma_pseudotop3_mtop_param = 0.5*(t_lep.M() + t_had.M());
	 //std::cout << pb_lep.Pt() << "\n" << pb_had.Pt() << "\n" << LJets[0].Pt() << "\n" << LJets[1].Pt() << "\n\n";
	 }
       }
       else if (m_tma_nbjets == 1){
         m_tma_pseudotop_rbq = bJets[0].Pt()/((LJets[0].Pt() + LJets[1].Pt())*0.5);
       }

    }


    if(m_tma_nbjets >= 2){ 

      // Sort b-tagged jets by pT (*BP* or by MV2)  
      TLorentzVector b1;
      TLorentzVector b2;
      if(bJets[0].Pt() >= bJets[1].Pt()){
	b1 = bJets[0];
	b2 = bJets[1];
      }
      else{
	b1 = bJets[1];
	b2 = bJets[0];
	std::cout << "Non-first jet max" << std::endl;
      }
      
      m_tma_mbb  = (b1 + b2).M();
      m_tma_pTbb = (b1 + b2).Pt();
      m_tma_dRbb = b1.DeltaR(b2);

      // for dilepton channel only
      if(goodLeptons.size() == 2){

	// Top reconstruction
	// Neutrino weighting, like in TopDileptonAnalysis

	if(lep_pos_set && lep_neg_set){

	  TLorentzVector b, bbar;
	  double deltaR_lep_pos_jet_1 = lep_pos.DeltaR(b1);
	  double deltaR_lep_neg_jet_2 = lep_neg.DeltaR(b2);
	  double distance_a = fabs(deltaR_lep_pos_jet_1 + deltaR_lep_neg_jet_2);

	  double deltaR_lep_pos_jet_2 = lep_pos.DeltaR(b2);
	  double deltaR_lep_neg_jet_1 = lep_neg.DeltaR(b1);
	  double distance_b = fabs(deltaR_lep_pos_jet_2 + deltaR_lep_neg_jet_1);

	  if( distance_a < distance_b){
	    b    = b1;
	    bbar = b2; }
	  else if (distance_b < distance_a){
	    b    = b2;
	    bbar = b1; }
	  else {
	    std::cout << "WARNING: Could not determine lepton-b pairings" <<  std::endl;
	    lep_pos.Print();
	    lep_neg.Print();
	    b2.Print();
	    b2.Print();
	    b    = b1;
	    bbar = b2; }

	  m_weight_max = 0.;
	  double m_weight_max_alt = 0.;

	  NeutrinoWeighter nuW     = NeutrinoWeighter(1, lep_pos.Pt() + lep_pos.Phi());// Ingnore the second argument,it's just a random string
	  NeutrinoWeighter nuW_alt = NeutrinoWeighter(1, lep_pos.Pt() + lep_pos.Eta() + m_tma_nbjets);//2
	  m_weight_max  = nuW.Reconstruct(lep_pos, lep_neg, b, bbar, m_tma_met_ex, m_tma_met_ey, m_tma_met_phi);
	  m_weight_max_alt = nuW_alt.Reconstruct(lep_neg, lep_pos, bbar, b, m_tma_met_ex, m_tma_met_ey, m_tma_met_phi);

	  if( m_weight_max_alt > m_weight_max){
	    nuW = nuW_alt;
	    m_weight_max = m_weight_max_alt; }

	  if(m_weight_max > 0.){

	    top   = nuW.GetTop();
	    tbar  = nuW.GetTbar();
            ttbar = nuW.GetTtbar();
            b     = nuW.GetB();
            bbar  = nuW.GetBbar();
            nu    = nuW.GetNu();
            nubar = nuW.GetNubar();

            TLorentzVector Wp, Wm;
            Wp = lep_pos + nu;
            Wm = lep_neg + nubar;

            m_tma_Wp_pt   = Wp.Pt();
            m_tma_Wp_eta  = Wp.Eta();
            m_tma_Wp_phi  = Wp.Phi();
            m_tma_Wp_m    = Wp.M();
            m_tma_Wp_e    = Wp.E();
            m_tma_Wp_y    = Wp.Rapidity();

            m_tma_Wm_pt   = Wm.Pt();
            m_tma_Wm_eta  = Wm.Eta();
            m_tma_Wm_phi  = Wm.Phi();
            m_tma_Wm_m    = Wm.M();
            m_tma_Wm_e    = Wm.E();
            m_tma_Wm_y    = Wm.Rapidity();

            m_tma_top_pt    = top.Pt();
            m_tma_top_eta   = top.Eta();
            m_tma_top_phi   = top.Phi();
            m_tma_top_m     = top.M();
            m_tma_top_e     = top.E();
            m_tma_top_y     = top.Rapidity();

            m_tma_tbar_pt   = tbar.Pt();
            m_tma_tbar_eta  = tbar.Eta();
            m_tma_tbar_phi  = tbar.Phi();
            m_tma_tbar_m    = tbar.M();
            m_tma_tbar_e    = tbar.E();
            m_tma_tbar_y    = tbar.Rapidity();

            m_tma_av_top_pt    = (m_tma_top_pt  + m_tma_tbar_pt)/2.;
            m_tma_av_top_eta   = (m_tma_top_eta + m_tma_tbar_eta)/2.;
            m_tma_av_top_phi   = (m_tma_top_phi + m_tma_tbar_phi)/2.;
            m_tma_av_top_m     = (m_tma_top_m   + m_tma_tbar_m)/2.;
            m_tma_av_top_e     = (m_tma_top_e   + m_tma_tbar_e)/2.;
            m_tma_av_top_y     = (m_tma_top_y   + m_tma_tbar_y)/2.;

            m_tma_ttbar_pt   = ttbar.Pt();
            m_tma_ttbar_eta  = ttbar.Eta();
            m_tma_ttbar_phi  = ttbar.Phi();
            m_tma_ttbar_m    = ttbar.M();
            m_tma_ttbar_e    = ttbar.E();
            m_tma_ttbar_y    = ttbar.Rapidity();
            m_tma_ttbar_pout = calculatePout( top, tbar );

            m_tma_nu_pt     = nu.Pt();
            m_tma_nu_eta    = nu.Eta();
            m_tma_nu_phi    = nu.Phi();
            m_tma_nu_m      = nu.M();
            m_tma_nu_e      = nu.E();
            m_tma_nu_y      = nu.Rapidity();

            m_tma_nubar_pt  = nubar.Pt();
            m_tma_nubar_eta = nubar.Eta();
            m_tma_nubar_phi = nubar.Phi();
            m_tma_nubar_m   = nubar.M();
            m_tma_nubar_e   = nubar.E();
            m_tma_nubar_y   = nubar.Rapidity();

	  }
//	  else { std::cout << "No top reconstruction" << std::endl; }
	}

	// Sort leptons by pT  
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
	double LBpair_avgMass = -1.0;
	double LBpair1_dR = -1.0;
	double LBpair2_dR = -1.0;
	
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

        m_tma_etdr = (L1.Et()*LBpair1_dR + L2.Et()*LBpair2_dR)/2.;
	m_tma_mlb_minavg     = LBpair_avgMass; 
	
	if(LBpair1.M() < LBpair2.M()){
	  m_tma_mlb_minavglow   = LBpair1.M();
	  m_tma_mlb_minavghigh  = LBpair2.M();
	}
	else{
	  m_tma_mlb_minavglow   = LBpair2.M();
	  m_tma_mlb_minavghigh  = LBpair1.M();
	}
	
	m_tma_pTlb_1 = LBpair1.Pt();
	m_tma_pTlb_2 = LBpair2.Pt();
	
	m_tma_dRlb_1 = LBpair1_dR;
	m_tma_dRlb_2 = LBpair2_dR;
	
	m_tma_mll    = (L1 + L2).M();
	m_tma_pTll   = (L1 + L2).Pt();
	m_tma_dRll   = L1.DeltaR(L2);

	double Rbq_avgLJ  = -1;
	double Rbq_leadLJ = -1;
	if(LJets.size() >= 1){
	  double bJets_sumPt = 0;
	  double LJets_sumPt = 0;
	  for(int i = 0; i < (int)bJets.size(); ++i)
	    bJets_sumPt += bJets.at(i).Pt();
	  for(int i = 0; i < (int)LJets.size(); ++i)
	    LJets_sumPt += LJets.at(i).Pt();
	  
	  Rbq_avgLJ  = (bJets_sumPt/bJets.size())/(LJets_sumPt/LJets.size());
	  Rbq_leadLJ = (bJets_sumPt/bJets.size())/LJets.at(0).Pt();
	}
	m_tma_Rbq_avgLJ  = Rbq_avgLJ;
	m_tma_Rbq_leadLJ = Rbq_leadLJ;


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
	
	if(LBpair1_maxMass.M() < LBpair2_maxMass.M())
	  m_tma_mlb_minmax = LBpair1_maxMass.M();
	else
	  m_tma_mlb_minmax = LBpair2_maxMass.M();
	
	if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	  m_tma_mlb_minmaxlow = LBpair1_minMass.M();
	}
	else{
	  m_tma_mlb_minmaxlow = LBpair2_minMass.M();
	}
	
	if(LBpair1_maxMass.M() < LBpair2_maxMass.M()){
	  m_tma_mlb_minmaxavg = (LBpair1_maxMass.M() + LBpair1_minMass.M())/2;
	}
	else{
	  m_tma_mlb_minmaxavg = (LBpair2_maxMass.M() + LBpair2_minMass.M())/2;
	}
	
	
      }
      
    }
    
    ///-- Let the base class do all the hard work --///
    top::EventSaverFlatNtuple::saveEvent(event);

  } 

void MassEventSaver::saveParticleLevelEvent(const top::ParticleLevelEvent& plEvent){

  if( !topConfig()->doTopParticleLevel() ){
	return;
  }

  std::vector<TLorentzVector> particle_bJets;
  std::vector<TLorentzVector> particle_LJets;
  std::vector<TLorentzVector> particle_goodLeptons;
  TLorentzVector lep_pos, lep_neg, nu, nubar, b, bbar, top, tbar, jet1, jet2;
  bool lep_pos_set = false;
  bool lep_neg_set = false;

  m_tma_particle_nbjets = 0;
  m_tma_particle_njets = 0;

  m_tma_particle_mlb_minavg = 0.;

  m_tma_particle_bjet_pt.clear();
  m_tma_particle_bjet_eta.clear();
  m_tma_particle_bjet_phi.clear();
  m_tma_particle_bjet_e.clear();

  m_tma_particle_jet_pt.clear();
  m_tma_particle_jet_eta.clear();
  m_tma_particle_jet_phi.clear();
  m_tma_particle_jet_e.clear();

  for (const auto & jetPtr : * plEvent.m_jets) {
    m_tma_particle_jet_pt.push_back(jetPtr->pt());
    m_tma_particle_jet_eta.push_back(jetPtr->eta());
    m_tma_particle_jet_phi.push_back(jetPtr->phi());
    m_tma_particle_jet_e.push_back(jetPtr->e());
    ++m_tma_particle_njets;

    if( jetPtr->auxdata<int>( "GhostBHadronsFinalCount" ) > 0){
      m_tma_particle_bjet_pt.push_back(jetPtr->pt());
      m_tma_particle_bjet_eta.push_back(jetPtr->eta());
      m_tma_particle_bjet_phi.push_back(jetPtr->phi());
      m_tma_particle_bjet_e.push_back(jetPtr->e());
      ++m_tma_particle_nbjets;

      TLorentzVector help;
      help.SetPtEtaPhiE(jetPtr->pt(), jetPtr->eta(), jetPtr->phi(), jetPtr->e());

      particle_bJets.push_back(help);
    }
    else {
      TLorentzVector help;
      help.SetPtEtaPhiE(jetPtr->pt(), jetPtr->eta(), jetPtr->phi(), jetPtr->e());

      particle_LJets.push_back(help);	
    }
  }

  m_tma_particle_bjet_pt.resize(m_tma_particle_nbjets);
  m_tma_particle_bjet_eta.resize(m_tma_particle_nbjets);
  m_tma_particle_bjet_phi.resize(m_tma_particle_nbjets);
  m_tma_particle_bjet_e.resize(m_tma_particle_nbjets);

  m_tma_particle_jet_pt.resize(m_tma_particle_njets);
  m_tma_particle_jet_eta.resize(m_tma_particle_njets);
  m_tma_particle_jet_phi.resize(m_tma_particle_njets);
  m_tma_particle_jet_e.resize(m_tma_particle_njets);

/*  TLorentzVector blep_particle_original;
  TLorentzVector bhad_particle_original;
  TLorentzVector lq1_particle_original;
  TLorentzVector lq2_particle_original;
  TLorentzVector Whad_particle_original;

  int nPermutations  = 0;
  bool validKLFitter = false;

  if (plEvent.m_KLFitterResults != nullptr) {

    validKLFitter = true;
    nPermutations = plEvent.m_KLFitterResults->size();

  }

std::cout << "nPermutations : " << nPermutations << std::endl;
std::cout << validKLFitter << std::endl;
    std::cout << "blep_index: " << blep_index << std::endl;
    std::cout << "bhad_index: " << bhad_index << std::endl;
    std::cout << "l1_index: " << lq1_index << std::endl;
    std::cout << "l2_index: " << lq2_index << std::endl;


  m_tma_particle_klfitter_mtop_param.resize(nPermutations);
  m_tma_particle_original_mw.resize(nPermutations);
  m_tma_particle_original_rbq.resize(nPermutations);

  int iPerm = 0;

  if (validKLFitter) {

    for (const auto* const klPtr : *plEvent.m_KLFitterResults) {

    int blep_index = klPtr->model_blep_jetIndex();
    int bhad_index = klPtr->model_bhad_jetIndex();
    int lq1_index  = klPtr->model_lq1_jetIndex();
    int lq2_index  = klPtr->model_lq2_jetIndex();
 
    blep_particle_original.SetPtEtaPhiE((*plEvent.m_jets)[blep_index] -> pt()/1000.0,
                   (*plEvent.m_jets)[blep_index] -> eta(),
                   (*plEvent.m_jets)[blep_index] -> phi(),
                   (*plEvent.m_jets)[blep_index] -> e()/1000.0);
    
    bhad_particle_original.SetPtEtaPhiE((*plEvent.m_jets)[bhad_index] -> pt()/1000.0,
                   (*plEvent.m_jets)[bhad_index] -> eta(),
                   (*plEvent.m_jets)[bhad_index] -> phi(),
                   (*plEvent.m_jets)[bhad_index] -> e()/1000.0);
        
    lq1_particle_original.SetPtEtaPhiE((*plEvent.m_jets)[lq1_index] -> pt()/1000.0,
                   (*plEvent.m_jets)[lq1_index] -> eta(),
                   (*plEvent.m_jets)[lq1_index] -> phi(),
                   (*plEvent.m_jets)[lq1_index] -> e()/1000.0);
        
    lq2_particle_original.SetPtEtaPhiE((*plEvent.m_jets)[lq2_index] -> pt()/1000.0,
                   (*plEvent.m_jets)[lq2_index] -> eta(),
                   (*plEvent.m_jets)[lq2_index] -> phi(),
                   (*plEvent.m_jets)[lq2_index] -> e()/1000.0);
        
    Whad_particle_original = lq1_particle_original + lq2_particle_original;
                                   
    m_tma_particle_original_mw[iPerm] = Whad_particle_original.M(); 

    if(m_tma_particle_nbjets == 1){
      m_tma_particle_original_rbq[iPerm] = m_tma_particle_bjet_pt[0]/1000.0/((lq1_particle_original.Pt()+lq2_particle_original.Pt())*0.5);
    }                              
    else if(m_tma_particle_nbjets >= 2){
      m_tma_particle_original_rbq[iPerm] = (m_tma_particle_bjet_pt[0] + m_tma_particle_bjet_pt[1])/1000.0/(lq1_particle_original.Pt()+lq2_particle_original.Pt());
    }

    int nr_param = klPtr->parameters().size();
    m_tma_particle_klfitter_mtop_param[iPerm] = klPtr->parameters().at(nr_param-1);
    ++iPerm;

    }

  }

*/
  for (const auto & elPtr : * plEvent.m_electrons) {

    if (elPtr->charge() > 0) {
        lep_pos.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());
        lep_pos_set = true; }

    else if (elPtr->charge() < 0) {
        lep_neg.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());
        lep_neg_set = true; }

    TLorentzVector help;
    help.SetPtEtaPhiE(elPtr->pt(), elPtr->eta(), elPtr->phi(), elPtr->e());
    particle_goodLeptons.push_back(help);
  }

  for (const auto & muPtr : * plEvent.m_muons) {

    if (muPtr->charge() > 0) {
        lep_pos.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());
        lep_pos_set = true; }

    else if (muPtr->charge() < 0) {
        lep_neg.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());
        lep_neg_set = true; }

    TLorentzVector help;
    help.SetPtEtaPhiE(muPtr->pt(), muPtr->eta(), muPtr->phi(), muPtr->e());
    particle_goodLeptons.push_back(help);
  }

  m_tma_particle_met 	   = plEvent.m_met->met();
  m_tma_particle_met_ex    = plEvent.m_met->mpx();
  m_tma_particle_met_ey    = plEvent.m_met->mpy();
  m_tma_particle_met_phi   = plEvent.m_met->phi();

  if(m_tma_particle_nbjets >= 2){ 

      // Sort b-tagged jets by pT (*BP* or by MV2)  
      TLorentzVector pb1;
      TLorentzVector pb2;
      if(particle_bJets[0].Pt() >= particle_bJets[1].Pt()){
	pb1 = particle_bJets[0];
	pb2 = particle_bJets[1];
      }
      else{
	pb1 = particle_bJets[1];
	pb2 = particle_bJets[0];
      }
      
      m_tma_particle_mbb  = (pb1 + pb2).M();
      m_tma_particle_pTbb = (pb1 + pb2).Pt();
      m_tma_particle_dRbb = pb1.DeltaR(pb2);

      // for dilepton channel only
      if(particle_goodLeptons.size() == 2){

       if(lep_pos_set && lep_neg_set){

	// Neutrinos

	const xAOD::TruthParticleContainer* neutrinos{nullptr};
	top::check(evtStore()->retrieve(neutrinos, "TruthNeutrinos"), "Failed to retrieve Truth Neutrinos");

	bool nu_set     = false;
        bool nubar_set  = false;
        int number_of_tau_neutrinos = 0;
        if (neutrinos != nullptr) {
           for (const auto& neutrino : *neutrinos) {
                ++m_tma_particle_nu_n;
                if( abs(neutrino->pdgId()) == 16) ++number_of_tau_neutrinos;
                   if(!nu_set || !nubar_set){
                      if( neutrino->pdgId() > 0 && !nu_set){
                         nu.SetPtEtaPhiE(neutrino->pt(), neutrino->eta(), neutrino->phi(), neutrino->e());
                         m_tma_particle_nu_pt   = nu.Pt();
                         m_tma_particle_nu_eta  = nu.Eta();
                         m_tma_particle_nu_phi  = nu.Phi();
                         m_tma_particle_nu_e    = nu.E();
                         m_tma_particle_nu_m    = nu.M();
                         m_tma_particle_nu_y    = nu.Rapidity();
                         nu_set = true; }
                      if( neutrino->pdgId() < 0 && !nubar_set){
                         nubar.SetPtEtaPhiE(neutrino->pt(), neutrino->eta(), neutrino->phi(), neutrino->e());
                         m_tma_particle_nubar_pt  = nubar.Pt();
                         m_tma_particle_nubar_eta = nubar.Eta();
                         m_tma_particle_nubar_phi = nubar.Phi();
                         m_tma_particle_nubar_e   = nubar.E();
                         m_tma_particle_nubar_m   = nubar.M();
                         m_tma_particle_nubar_y   = nubar.Rapidity();

                         nubar_set = true; }
                   }
            }
        }

	/// ----------------------------------------//
	///-- Pseudo Top Reconstruction: dilepton --//
	/// ----------------------------------------//

	if(m_tma_particle_nbjets > 0 && m_tma_particle_njets > 1){

	  if(m_tma_particle_nbjets > 1){
	     jet1.SetPtEtaPhiE(m_tma_particle_bjet_pt[0], m_tma_particle_bjet_eta[0], m_tma_particle_bjet_phi[0], m_tma_particle_bjet_e[0]);
	     jet2.SetPtEtaPhiE(m_tma_particle_bjet_pt[1], m_tma_particle_bjet_eta[1], m_tma_particle_bjet_phi[1], m_tma_particle_bjet_e[1]); }
	  else {
	     jet1.SetPtEtaPhiE(m_tma_particle_bjet_pt[0], m_tma_particle_bjet_eta[0], m_tma_particle_bjet_phi[0], m_tma_particle_bjet_e[0]);
	     if (m_tma_particle_jet_pt[0] != m_tma_particle_bjet_pt[0]){
	        jet2.SetPtEtaPhiE(m_tma_particle_jet_pt[0], m_tma_particle_jet_eta[0], m_tma_particle_jet_phi[0], m_tma_particle_jet_e[0]);}
	     else {
	        jet2.SetPtEtaPhiE(m_tma_particle_jet_pt[1], m_tma_particle_jet_eta[1], m_tma_particle_jet_phi[1], m_tma_particle_jet_e[1]);}
	   }

	
        TLorentzVector Wp, Wm, top_a, tbar_a, top_b, tbar_b;

        Wp = lep_pos + nu;
        Wm = lep_neg + nubar;

        top_a  = Wp + jet1;
        top_b  = Wp + jet2;

        tbar_a = Wm + jet2;
        tbar_b = Wm + jet1;

        double diff_a = fabs(top_a.M() - 172.5) + fabs(tbar_a.M() - 172.5);
        double diff_b = fabs(top_b.M() - 172.5) + fabs(tbar_b.M() - 172.5);
        if(diff_a < diff_b){ // A is the correct combination
          top  = top_a;
          tbar = tbar_a;
        } else if (diff_a > diff_b){ // B is the right combination
          top  = top_b;
          tbar = tbar_b;
        } else {
          top  = top_a;
          tbar = tbar_a;
        }

        TLorentzVector ttbar = top + tbar;

        m_tma_particle_Wp_pt   = Wp.Pt();
        m_tma_particle_Wp_eta  = Wp.Eta();
        m_tma_particle_Wp_phi  = Wp.Phi();
        m_tma_particle_Wp_m    = Wp.M();
        m_tma_particle_Wp_e    = Wp.E();
        m_tma_particle_Wp_y    = Wp.Rapidity();

        m_tma_particle_Wm_pt   = Wm.Pt();
        m_tma_particle_Wm_eta  = Wm.Eta();
        m_tma_particle_Wm_phi  = Wm.Phi();
        m_tma_particle_Wm_m    = Wm.M();
        m_tma_particle_Wm_e    = Wm.E();
        m_tma_particle_Wm_y    = Wm.Rapidity();

        m_tma_particle_top_pt        = top.Pt();
        m_tma_particle_top_eta      = top.Eta();
        m_tma_particle_top_phi      = top.Phi();
        m_tma_particle_top_m          = top.M();
        m_tma_particle_top_e          = top.E();
        m_tma_particle_top_y          = top.Rapidity();

        m_tma_particle_tbar_pt      = tbar.Pt();
        m_tma_particle_tbar_eta     = tbar.Eta();
        m_tma_particle_tbar_phi     = tbar.Phi();
        m_tma_particle_tbar_m        = tbar.M();
        m_tma_particle_tbar_e        = tbar.E();
        m_tma_particle_tbar_y        = tbar.Rapidity();

        m_tma_particle_av_top_pt    = (m_tma_particle_top_pt  + m_tma_particle_tbar_pt)/2.;
        m_tma_particle_av_top_eta   = (m_tma_particle_top_eta + m_tma_particle_tbar_eta)/2.;
        m_tma_particle_av_top_phi   = (m_tma_particle_top_phi + m_tma_particle_tbar_phi)/2.;
        m_tma_particle_av_top_m     = (m_tma_particle_top_m   + m_tma_particle_tbar_m)/2.;
        m_tma_particle_av_top_e     = (m_tma_particle_top_e   + m_tma_particle_tbar_e)/2.;
	m_tma_particle_av_top_y     = (m_tma_particle_top_y   + m_tma_particle_tbar_y)/2.;

        m_tma_particle_ttbar_pt     = ttbar.Pt();
        m_tma_particle_ttbar_eta    = ttbar.Eta();
        m_tma_particle_ttbar_phi    = ttbar.Phi();
        m_tma_particle_ttbar_m      = ttbar.M();
        m_tma_particle_ttbar_e      = ttbar.E();
        m_tma_particle_ttbar_y      = ttbar.Rapidity();
        m_tma_particle_ttbar_pout   = calculatePout( top, tbar );

	}
	}

	// Sort leptons by pT  
	TLorentzVector pL1;
	TLorentzVector pL2;
	if(particle_goodLeptons.at(0).Pt() >= particle_goodLeptons.at(1).Pt()){
	  pL1 = particle_goodLeptons.at(0);
	  pL2 = particle_goodLeptons.at(1);
	}
	else{
	  pL1 = particle_goodLeptons.at(1);
	  pL2 = particle_goodLeptons.at(0);
	}

	//Pairing decision             
	TLorentzVector pL1b1 = pL1 + pb1;
	TLorentzVector pL2b2 = pL2 + pb2;
	TLorentzVector pL1b2 = pL1 + pb2;
	TLorentzVector pL2b1 = pL2 + pb1;
	double pavgMass1 = (pL1b1.M() + pL2b2.M())/2 ;
	double pavgMass2 = (pL1b2.M() + pL2b1.M())/2 ;
	
	TLorentzVector pLBpair1;
	TLorentzVector pLBpair2;
	TLorentzVector pLBpair1_reject;
	TLorentzVector pLBpair2_reject;
	double pLBpair_avgMass = -1.0;
	double pLBpair1_dR = -1.0;
	double pLBpair2_dR = -1.0;
	
	if( pavgMass1 <= pavgMass2 ){
	  pLBpair1 = pL1b1;
	  pLBpair2 = pL2b2;
	  pLBpair1_reject = pL1b2;
	  pLBpair2_reject = pL2b1;
	  pLBpair_avgMass = pavgMass1;
	  pLBpair1_dR = pb1.DeltaR(pL1);
	  pLBpair2_dR = pb2.DeltaR(pL2);
	}
	else{
	  pLBpair1 = pL1b2;
	  pLBpair2 = pL2b1;
	  pLBpair1_reject = pL1b1;
	  pLBpair2_reject = pL2b2;
	  pLBpair_avgMass = pavgMass2;
	  pLBpair1_dR = pb2.DeltaR(pL1);
	  pLBpair2_dR = pb1.DeltaR(pL2);
	}

        m_tma_particle_etdr = (pL1.Et()*pLBpair1_dR + pL2.Et()*pLBpair2_dR)/2.;
	m_tma_particle_mlb_minavg     = pLBpair_avgMass; 
	
	if(pLBpair1.M() < pLBpair2.M()){
	  m_tma_particle_mlb_minavglow   = pLBpair1.M();
	  m_tma_particle_mlb_minavghigh  = pLBpair2.M();
	}
	else{
	  m_tma_particle_mlb_minavglow   = pLBpair2.M();
	  m_tma_particle_mlb_minavghigh  = pLBpair1.M();
	}
	
	m_tma_particle_pTlb_1 = pLBpair1.Pt();
	m_tma_particle_pTlb_2 = pLBpair2.Pt();
	
	m_tma_particle_dRlb_1 = pLBpair1_dR;
	m_tma_particle_dRlb_2 = pLBpair2_dR;
	
	m_tma_particle_mll    = (pL1 + pL2).M();
	m_tma_particle_pTll   = (pL1 + pL2).Pt();
	m_tma_particle_dRll   = pL1.DeltaR(pL2);

     }


  }

  /// ----------------------------------------//
  ///-- Pseudo Top Reconstruction: lepton+j --//
  /// ----------------------------------------//



  if (particle_goodLeptons.size() == 1 && particle_LJets.size() >= 2) {

       if (m_tma_particle_nbjets >= 2){
         TLorentzVector p_lep = particle_goodLeptons.at(0);
         TLorentzVector p_b_lep, p_b_had;
         if (particle_bJets[0].DeltaR(p_lep) < particle_bJets[1].DeltaR(p_lep)){
           p_b_lep = particle_bJets[0];
           p_b_had = particle_bJets[1];
         }
         else {
           p_b_lep = particle_bJets[1];
           p_b_had = particle_bJets[0];
         }
         TLorentzVector p_miss, p_t_lep, p_t_had;
         p_t_had = p_b_had + particle_LJets[0] + particle_LJets[1];
         m_tma_particle_pseudotop_mw = (particle_LJets[0] + particle_LJets[1]).M();
         m_tma_particle_pseudotop_rbq = (p_b_lep.Pt() + p_b_had.Pt())/(particle_LJets[0].Pt() + particle_LJets[1].Pt());

         Double_t mW = 80.309;
         Double_t lE = p_lep.E();
         Double_t lX = p_lep.Px();
         Double_t lY = p_lep.Py();
         Double_t lZ = p_lep.Pz();

         Double_t nuE = plEvent.m_met->met();
         Double_t nuX = plEvent.m_met->mpx();
         Double_t nuY = plEvent.m_met->mpy();

         Double_t wPz2 = pow(lE + nuE,2) - pow(lX + nuX,2) - pow(lY + nuY,2) - pow(mW,2);
         Double_t nuZ = 0.;

	 // Pseudo-top def. 0 (default)

         if (wPz2 >= 0.) nuZ = abs(sqrt(wPz2) - lZ) <= abs(-sqrt(wPz2) - lZ) ? (sqrt(wPz2) - lZ) : (-sqrt(wPz2) - lZ);
         else nuZ = -lZ;

         p_miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
         p_t_lep = p_b_lep + p_lep + p_miss;
         m_tma_particle_pseudotop0_mtop_param = 0.5*(p_t_lep.M() + p_t_had.M());
         
	 if ( pseudotop == true ) {

	   // Pseudo-top def. 1

           if (wPz2 >= 0.) nuZ = abs(sqrt(wPz2) - lZ) >= abs(-sqrt(wPz2) - lZ) ? (sqrt(wPz2) - lZ) : (-sqrt(wPz2) - lZ);
           else nuZ = -lZ;

           p_miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           p_t_lep = p_b_lep + p_lep + p_miss;
           m_tma_particle_pseudotop1_mtop_param = 0.5*(p_t_lep.M() + p_t_had.M());

	   // Pseudo-top def. 2

           Double_t nuZ_1 = sqrt(wPz2) - lZ;
           Double_t nuZ_2 = -sqrt(wPz2) - lZ;
           TLorentzVector miss_1, miss_2;
           miss_1.SetPxPyPzE(nuX, nuY, nuZ_1, nuE);
           miss_2.SetPxPyPzE(nuX, nuY, nuZ_2, nuE);
           TLorentzVector tlep_1 = p_b_lep + p_lep + miss_1;
           TLorentzVector tlep_2 = p_b_lep + p_lep + miss_2;

           nuZ = abs(tlep_1.M() - p_t_had.M()) <= abs(tlep_2.M() - p_t_had.M()) ? nuZ_1 : nuZ_2;

           p_miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           p_t_lep = p_b_lep + p_lep + p_miss;
           m_tma_particle_pseudotop2_mtop_param = 0.5*(p_t_lep.M() + p_t_had.M());

	   // Pseudo-top def. 3

           Double_t bE = p_b_lep.E();
           Double_t bX = p_b_lep.Px();
           Double_t bY = p_b_lep.Py();
           Double_t bZ = p_b_lep.Pz();

           Double_t tPz2 = pow(bZ,2) - pow(p_b_lep.M(),2) - pow(p_t_had.M(),2)
                + pow(lE + nuE,2) - pow(lX + nuX,2) - pow(lY + nuY,2)
                + 2*( (lE + nuE)*bE - (lX + nuX)*bX - (lY + nuY)*bY );
           if (tPz2 >= 0.) nuZ = abs(sqrt(tPz2) - (lZ + bZ)) <= abs(-sqrt(tPz2) - (lZ + bZ)) ? (sqrt(tPz2) - (lZ + bZ)) : (-sqrt(tPz2) - (lZ + bZ));
           else nuZ = - (lZ + bZ);

           p_miss.SetPxPyPzE(nuX, nuY, nuZ, nuE);
           p_t_lep = p_b_lep + p_lep + p_miss;
           m_tma_particle_pseudotop3_mtop_param = 0.5*(p_t_lep.M() + p_t_had.M());
         //std::cout << pb_lep.Pt() << "\n" << pb_had.Pt() << "\n" << LJets[0].Pt() << "\n" << LJets[1].Pt() << "\n\n";
         }
       }

       else if (m_tma_nbjets == 1){
//	 std::cout << "bjet pt : " << particle_bJets[0].Pt() << 
//	 ", ljets :" << particle_bJets[0].Pt()/(particle_LJets[0].Pt() + particle_LJets[1].Pt())/2. << std::endl;
//         m_tma_particle_pseudotop_rbq = particle_bJets[0].Pt()/(particle_LJets[0].Pt() + particle_LJets[1].Pt())/2.;
       }

    }

top::EventSaverFlatNtuple::saveParticleLevelEvent(plEvent);

}

float MassEventSaver::calculatePout(TLorentzVector t, TLorentzVector tbar){

    TVector3 t3(t.X(),t.Y(),t.Z());
    TVector3 tbar3(tbar.X(),tbar.Y(),tbar.Z());
    TVector3 z(0,0,1);
    TVector3 vec_temp=tbar3.Cross(z);

    vec_temp*=1/vec_temp.Mag();
    float pout=t3.Dot(vec_temp);

    return pout;
}

}

