from ROOT import gROOT, TH1, TEfficiency, TTree

class observable:

	typ	= 'float'
	name	= ''
	nbins   = 0
        xmin    = 0
        xmax    = 0
        latex   = ''

        def __init__(self, name, nbins, xmin, xmax, latex):

            self.name    = name
            self.nbins   = nbins
            self.xmin    = xmin
            self.xmax    = xmax
            self.latex   = latex

class vector_observable:

	typ	= 'float'
	name	= ''
	nbins   = 0
        xmin    = 0
        xmax    = 0
        latex   = ''

        def __init__(self, name, nbins, xmin, xmax, latex):

            self.name    = name
            self.nbins   = nbins
            self.xmin    = xmin
            self.xmax    = xmax
            self.latex   = latex


class migration_matrix:

	obs	= observable()
	migr	= None

	def __init__(self, observable):

	    self.obs  = observable
	    self.migr = TH2F( 'tMatrix_' + obs.name, 'A_{ij} ' + obs.name,
			 obs.nbins, obs.xmin, obs.xmax,
			 obs.nbins, obs.xmin, obs.xmax )

class efficiency:

        obs     = observable()
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TH1F( 'tEff_' + obs.name, '#epsilon_{epsilon} ' + obs.name,
			 obs.nbins, obs.xmin, obs.xmax )

class efficiency_binomial:

        obs     = observable()
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TEfficiency( 'tEff_' + obs.name, '#epsilon_{epsilon} ' + obs.name,
				 obs.nbins, obs.xmin, obs.xmax )

class fake_rates:

        self.obs     = observable()
        self.facc    = None

        def __init__(self, observable):

            self.obs  = observable
            self.facc = TH1F( 'tFacc_' + obs.name, 'f_{acc} ' + obs.name,
                         obs.nbins, obs.xmin, obs.xmax )

class fake_rates_binomial:

        obs     = observable()
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TEfficiency( 'tFacc_' + obs.name, 'f_{acc} ' + obs.name, 
                                 obs.nbins, obs.xmin, obs.xmax )


class sample:

	identifier = None

	reco_tree_chain  = None
	part_tree_chian  = None
	reco_tree_struct = None
	part_tree_struct = None

	input_file    = ''
	observables   = []

	migr_matrices 	= []
	efficiencies	= []
	fake_rates	= []

	def __init__(self, input_file, observables):

	    self.input_file  = input_file
	    self.observables = observables
	    reco_tree_chain  = TChain('nominal')
	    part_tree_chain  = TChain('particleLevel')

	def import_data(self):

	    if self.input_file == '': ERROR('import_data: No input file given')

	    fileh = open(self.input_file)
	    for sample in fileh:
		filename = sample.split('\n')[0]
		print 'Adding ' + filename + ' to the samples list...'
		self.reco_tree_chain.Add(filename)
		self.part_tree_chain.Add(filename)
	    fileh.close()
	    

	def synchronize_trees(self):

	    reco_index = TTreeIndex( self.reco_tree_chain, 'runNumber', 'eventNumber' )
	    part_index = TTreeIndex( self.part_tree_chain, 'runNumber', 'eventNumber' )

	    struct1 = 'struct nominal_t{UInt_t runNumber;ULong64_t eventNumber;'
	    struct2 = 'struct particleLevel_t{UInt_t runNumber;ULong64_t eventNumber;'

	    for obs in self.observables:
		struct1 += obs.typ + ' ' + obs.name + '_reco;'
		struct2 += obs.typ + ' ' + obs.name + '_part;'

	    ## TODO : add vector obs

	    struct1 += '}'
	    struct2 += '}'

	    gROOT.ProcessLine(struct1)
	    gROOT.ProcessLine(struct2)

	    nominal = nominal_t()
	    particleLevel = particleLevel_t()

	    reco_tree_chain.SetBranchAddress("runNumber", AddressOf(nominal,'runNumber'))
	    reco_tree_chain.SetBranchAddress("eventNumber", AddressOf(nominal,'eventNumber'))
	    for obs in self.observables:
		reco_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(nominal, obs.name + '_reco') )
		part_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(particleLevel, obs.name + '_part') )

	    ## TODO : add vector obs

	def populate_up:

	    
