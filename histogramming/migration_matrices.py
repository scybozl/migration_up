from ROOT import gROOT, TH1, TEfficiency, TTree, TChain

class observable:

	typ	= 'float'
	name	= ''
	nbins   = 0
        xmin    = 0
        xmax    = 0
        latex   = ''

        def __init__(self, typ, name, nbins, xmin, xmax, latex):

	    self.typ	 = typ
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

	obs	= None
	migr	= None

	def __init__(self, observable):

	    self.obs  = observable
	    self.migr = TH2F( 'tMatrix_' + obs.name, 'A_{ij} ' + obs.name,
			 obs.nbins, obs.xmin, obs.xmax,
			 obs.nbins, obs.xmin, obs.xmax )

class efficiency:

        obs     = None
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TH1F( 'tEff_' + obs.name, '#epsilon_{epsilon} ' + obs.name,
			 obs.nbins, obs.xmin, obs.xmax )

class efficiency_binomial:

        obs     = None
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TEfficiency( 'tEff_' + obs.name, '#epsilon_{epsilon} ' + obs.name,
				 obs.nbins, obs.xmin, obs.xmax )

class fake_rates:

        obs     = None
        facc    = None

        def __init__(self, observable):

            self.obs  = observable
            self.facc = TH1F( 'tFacc_' + obs.name, 'f_{acc} ' + obs.name,
                         obs.nbins, obs.xmin, obs.xmax )

class fake_rates_binomial:

        obs     = None
        eff     = None

        def __init__(self, observable):

            self.obs  = observable
            self.eff  = TEfficiency( 'tFacc_' + obs.name, 'f_{acc} ' + obs.name, 
                                 obs.nbins, obs.xmin, obs.xmax )

class reco_hist:

        obs       = None
        reco_hist = None

        def __init__(self, observable):

            self.obs	    = observable
            self.reco_hist  = TH1F( 'tReco_' + obs.name, obs.name + '^{reco}',
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

	def __init__(self, identifier, input_file, observables):

	    self.identifier  = identifier
	    self.input_file  = input_file
	    self.observables = observables
	    self.reco_tree_chain  = TChain('nominal')
	    self.part_tree_chain  = TChain('particleLevel')

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

	    self.reco_tree_struct = nominal_t()
	    self.part_tree_struct = particleLevel_t()

	    self.reco_tree_chain.SetBranchAddress( 'runNumber', AddressOf(self.reco_tree_struct,'runNumber') )
	    self.reco_tree_chain.SetBranchAddress( 'eventNumber', AddressOf(self.reco_tree_struct,'eventNumber') )
	    for obs in self.observables:
		self.reco_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(self.reco_tree_struct, obs.name + '_reco') )
		self.part_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(self.reco_tree_struct, obs.name + '_part') )

	    ## TODO : add vector obs

"""	def populate_up:

	    reco_hists = []

	    output_dir = 'histograms_' + identifier
	    os.system( 'mkdir ' + output_dir )

	    global reco_only
	    reco_hist_file = TFile( output_dir + '/reco_level.root', 'NEW' )

	    for i in range( self.reco_tree_chain.GetEntries() ):
		if ((i_1) % 1000) == 0: print 'Processing event number ' + str(i+1) + '...'
		self.reco_tree_chain.GetEntry(i)

		for j, obs in enumerate( self.observables ):
		    y = obs.name + '_reco'
		    reco_hists.append( 

"""
