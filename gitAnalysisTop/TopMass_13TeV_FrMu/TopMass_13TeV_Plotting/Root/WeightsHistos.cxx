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

void HistoCreator::FillWeights()
{
  
  for(unsigned iVar = 0; iVar < fVar.size(); ++iVar){

    //    std::cout << fVariables[iVar].c_str() << std::endl;

    //    std::cout << fFlatTree -> weight_bTagSF_77_eigenvars_B_up -> size() << "\t" << fFlatTree -> weight_bTagSF_77_eigenvars_C_up ->size() << "\t" << fFlatTree -> weight_bTagSF_77_eigenvars_Light_up -> size() << std::endl;

    if (fVariables[iVar] == "weight_mc")
      fTreeVariables[iVar] = fFlatTree -> weight_mc;
    if (fVariables[iVar] == "weight_pileup")
      fTreeVariables[iVar] = fFlatTree -> weight_pileup;
    if (fVariables[iVar] == "weight_leptonSF")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF;
    if (fVariables[iVar] == "weight_bTagSF_77")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77;
    if (fVariables[iVar] == "weight_jvt")
      fTreeVariables[iVar] = fFlatTree -> weight_jvt;
    if (fVariables[iVar] == "weight_pileup_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_pileup_UP;
    if (fVariables[iVar] == "weight_pileup_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_pileup_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Trigger_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Trigger_UP;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Trigger_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Trigger_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Reco_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Reco_UP;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Reco_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Reco_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_ID_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_ID_UP;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_ID_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_ID_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Isol_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Isol_UP;
    if (fVariables[iVar] == "weight_leptonSF_EL_SF_Isol_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_EL_SF_Isol_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Trigger_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Trigger_STAT_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Trigger_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Trigger_STAT_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Trigger_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Trigger_SYST_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Trigger_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Trigger_SYST_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_ID_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_ID_STAT_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_ID_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_ID_STAT_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_ID_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_ID_SYST_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_ID_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_ID_SYST_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Isol_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Isol_STAT_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Isol_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Isol_STAT_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Isol_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Isol_SYST_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_Isol_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_Isol_SYST_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_TTVA_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_TTVA_STAT_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_TTVA_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_TTVA_STAT_DOWN;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_TTVA_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_TTVA_SYST_UP;
    if (fVariables[iVar] == "weight_leptonSF_MU_SF_TTVA_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_leptonSF_MU_SF_TTVA_SYST_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Trigger")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Trigger;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Trigger_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Trigger_UP;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Trigger_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Trigger_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Reco")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Reco;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Reco_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Reco_UP;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Reco_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Reco_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_EL_ID")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_ID;
    if (fVariables[iVar] == "weight_indiv_SF_EL_ID_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_ID_UP;
    if (fVariables[iVar] == "weight_indiv_SF_EL_ID_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_ID_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Isol")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Isol;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Isol_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Isol_UP;
    if (fVariables[iVar] == "weight_indiv_SF_EL_Isol_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_EL_Isol_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Trigger")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Trigger;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Trigger_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Trigger_STAT_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Trigger_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Trigger_STAT_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Trigger_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Trigger_SYST_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Trigger_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Trigger_SYST_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_ID")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_ID;
    if (fVariables[iVar] == "weight_indiv_SF_MU_ID_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_ID_STAT_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_ID_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_ID_STAT_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_ID_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_ID_SYST_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_ID_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_ID_SYST_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Isol")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Isol;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Isol_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Isol_STAT_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Isol_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Isol_STAT_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Isol_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Isol_SYST_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_Isol_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_Isol_SYST_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_TTVA")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_TTVA;
    if (fVariables[iVar] == "weight_indiv_SF_MU_TTVA_STAT_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_TTVA_STAT_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_TTVA_STAT_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_TTVA_STAT_DOWN;
    if (fVariables[iVar] == "weight_indiv_SF_MU_TTVA_SYST_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_TTVA_SYST_UP;
    if (fVariables[iVar] == "weight_indiv_SF_MU_TTVA_SYST_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_indiv_SF_MU_TTVA_SYST_DOWN;
    if (fVariables[iVar] == "weight_bTagSF_77_extrapolation_up")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_extrapolation_up;
    if (fVariables[iVar] == "weight_bTagSF_77_extrapolation_down")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_extrapolation_down;
    if (fVariables[iVar] == "weight_bTagSF_77_extrapolation_from_charm_up")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_extrapolation_from_charm_up;
    if (fVariables[iVar] == "weight_bTagSF_77_extrapolation_from_charm_down")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_extrapolation_from_charm_down;
    if (fVariables[iVar] == "weight_jvt_UP")
      fTreeVariables[iVar] = fFlatTree -> weight_jvt_UP;
    if (fVariables[iVar] == "weight_jvt_DOWN")
      fTreeVariables[iVar] = fFlatTree -> weight_jvt_DOWN;

    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(2);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_3")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(3);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_4")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(4);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_up_5")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_up ->at(5);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(2);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_3")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(3);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_4")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(4);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_B_down_5")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_B_down ->at(5);

    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_up_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_up ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_up_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_up ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_up_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_up ->at(2);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_down_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_down ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_down_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_down ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_C_down_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_C_down ->at(2);

    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(2);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_3")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(3);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_4")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(4);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_5")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(5);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_6")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(6);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_7")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(7);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_8")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(8);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_9")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(9);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_10")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(10);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_11")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(11);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_12")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(12);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_13")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(13);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_14")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(14);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_up_15")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_up ->at(15);

    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_0")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(0);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_1")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(1);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_2")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(2);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_3")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(3);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_4")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(4);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_5")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(5);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_6")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(6);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_7")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(7);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_8")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(8);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_9")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(9);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_10")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(10);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_11")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(11);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_12")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(12);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_13")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(13);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_14")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(14);
    if (fVariables[iVar] == "weight_bTagSF_77_eigenvars_Light_down_15")
      fTreeVariables[iVar] = fFlatTree -> weight_bTagSF_77_eigenvars_Light_down ->at(15);


  }
}


