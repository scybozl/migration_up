#ifndef ENUMS_H
#define ENUMS_H
 
#include "TLegend.h"
#include <string>
#include <iostream>

enum BINS{ v0incl, v1incl, v2incl, v3incl, v4incl, v5incl, v6incl, v0excl, v1excl, v2excl, v3excl, v4excl, v5excl, v6excl, vnone, nodef};

BINS TranslateBinToEnum(std::string bin);

#endif
