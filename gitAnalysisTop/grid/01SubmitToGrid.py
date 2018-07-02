#!/usr/bin/env python
import TopExamples.grid
import DerivationTags
import Data
import MC15c_TOPQ1

config = TopExamples.grid.Config()
config.code          = 'top-xaod'
config.settingsFile  = 'TopMassOnline_13TeV.txt'

config.gridUsername  = 'lscyboz'
config.suffix        = 'MTOP172p5_bb4l'
config.excludedSites = ''
config.noSubmit      = False
config.mergeType     = 'Default' #'None', 'Default' or 'xAOD'
config.destSE        = '' #This is the default (anywhere), or try e.g. 'UKI-SOUTHGRID-BHAM-HEP_LOCALGROUPDISK'
# by default the requested memory is set to 2GB, if you need to increase this, please disable the line below!!!
# config.memory = '4000' 

###############################################################################

###Command line interface
###If you want a script that ask you what you want to run on interactively,
###and uses lists of primary xAODs to convert them as TOPQ derivations
###Otherwise you can edit the automatic scripts below
#names, derivation, ptag = DerivationTags.InteractiveSubmission()
#samples = TopExamples.grid.Samples(names)
#TopExamples.grid.convertAODtoTOPQ(derivation, ptag, samples)
#TopExamples.grid.submit(config, samples)

###############################################################################

# Data - look in Data.py
# Change if you want TOPQ2/3/4
#names = ['Data15_TOPQ1', 'Data16_TOPQ1']
#samples = TopExamples.grid.Samples(names)
#TopExamples.grid.submit(config, samples)

###############################################################################

###MC Simulation - look in MC15c_TOPQ1.py
###Using list of TOPQ1 25ns MC samples, consistent mixture of p-tags
###Edit these lines if you don't want to run everything!
names = [
     "TOPQ1_ttbar_PowPy8"
#    'TOPQ1_ttbar_PowPy6',
#    'TOPQ1_singleTop_PowPy6',
#    'TOPQ1_ttV',
#    'TOPQ1_Wjets_Sherpa221',
#    'TOPQ1_Zjets_Sherpa221',
#    'TOPQ1_Diboson_Sherpa',
]

samples = TopExamples.grid.Samples(names)
TopExamples.grid.submit(config, samples)

