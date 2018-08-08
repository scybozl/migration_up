# Auto-generated on: 2017-11-24 15:14:15.262411

# Declare the name of this package:
atlas_subdir( TopMass_13TeV_Plotting None )

# This package depends on other packages:
atlas_depends_on_subdirs( PUBLIC
                          TopDataPreparation
                          AsgTools )

# This package uses ROOT:
find_package( ROOT REQUIRED COMPONENTS Core Gpad Tree Hist RIO MathCore Graf Matrix Physics  )

# Generate a CINT dictionary source file:
atlas_add_root_dictionary( TopMass_13TeV_Plotting _cintDictSource
                           ROOT_HEADERS Root/LinkDef.h
                           EXTERNAL_PACKAGES ROOT )

# Build a library that other components can link against:
atlas_add_library( TopMass_13TeV_Plotting Root/*.cxx Root/*.h Root/*.icc
                   TopMass_13TeV_Plotting/*.h TopMass_13TeV_Plotting/*.icc TopMass_13TeV_Plotting/*/*.h
                   TopMass_13TeV_Plotting/*/*.icc ${_cintDictSource} 
                   PUBLIC_HEADERS TopMass_13TeV_Plotting
                   LINK_LIBRARIES TopDataPreparation
                                  AsgTools
                                  ${ROOT_LIBRARIES}
                   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} )

# Install data files from the package:
atlas_install_data( DIRECTORY data/* )

atlas_add_executable( MakePlots
		      util/MakePlots.cxx 
		      LINK_LIBRARIES TopMass_13TeV_Plotting
		      TopMass_13TeV_Online
		      ${ROOT_LIBRARIES}
		      )
