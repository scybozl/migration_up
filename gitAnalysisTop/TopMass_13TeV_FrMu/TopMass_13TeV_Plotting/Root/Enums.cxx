#include "TopMass_13TeV_Plotting/Enums.h"
#include "TLegend.h"
#include <string>
#include <iostream>


BINS TranslateBinToEnum(std::string bin){

  if(bin == "0incl")
    return v0incl;
  if(bin == "1incl")
    return v1incl;
  if(bin == "2incl")
    return v2incl;
  if(bin == "3incl")
    return v3incl;
  if(bin == "4incl")
    return v4incl;
  if(bin == "5incl")
    return v5incl;
  if(bin == "6incl")
    return v6incl;
  if(bin == "0excl")
    return v0excl;
  if(bin == "1excl")
    return v1excl;
  if(bin == "2excl")
    return v2excl;
  if(bin == "3excl")
    return v3excl;
  if(bin == "4excl")
    return v4excl;
  if(bin == "5excl")
    return v5excl;
  if(bin == "6excl")
    return v6excl;
  if(bin == "none")
    return vnone;

  std::cout << "ENUM: This Bin Type " << bin.c_str()  << " does not exist!!! ===> EXIT." << std::endl;
  
  return nodef;

}
