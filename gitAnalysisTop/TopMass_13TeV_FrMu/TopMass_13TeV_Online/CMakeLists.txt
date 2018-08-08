# Auto-generated on: 2017-11-24 15:14:15.262411

# Declare the name of this package:
atlas_subdir( TopMass_13TeV_Online None )

# This package depends on other packages:
atlas_depends_on_subdirs( PUBLIC
                          TopObjectSelectionTools
                          TopEventSelectionTools
                          TopEvent
                          TopConfiguration
                          TopAnalysis
                          JetJvtEfficiency
                          AsgTools )

# This package uses ROOT:
find_package( ROOT REQUIRED COMPONENTS Core Gpad Tree Hist RIO MathCore Graf )

# Generate a CINT dictionary source file:
atlas_add_root_dictionary( TopMass_13TeV_Online _cintDictSource
                           ROOT_HEADERS Root/LinkDef.h
                           EXTERNAL_PACKAGES ROOT )

# Build a library that other components can link against:
atlas_add_library( TopMass_13TeV_Online Root/*.cxx Root/*.h Root/*.icc
                   TopMass_13TeV_Online/*.h TopMass_13TeV_Online/*.icc TopMass_13TeV_Online/*/*.h
                   TopMass_13TeV_Online/*/*.icc ${_cintDictSource} 
                   PUBLIC_HEADERS TopMass_13TeV_Online
                   LINK_LIBRARIES TopObjectSelectionTools
                                  TopEventSelectionTools
                                  TopEvent
                                  TopConfiguration
                                  TopAnalysis
                                  JetJvtEfficiencyLib
                                  AsgTools
                                  ${ROOT_LIBRARIES}
                   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} )

# Install data files from the package:
atlas_install_data( DIRECTORY share/* )

