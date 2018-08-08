#ifndef FANCYPLOTS_H_
#define FANCYPLOTS_H_

#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>
#include <set>
#include <iomanip>
#include <vector>
#include "TH1D.h"

void MakePieChart(std::string, std::string, std::vector<float>, bool);
void MakeHiggsDecayPieChart(TH1D, std::string, std::string, std::string);

void PlotSignalOverBkg(std::string, float, float);

#endif
