from ROOT import gROOT, AddressOf, TH1F, TH2F, TEfficiency, TTree, TChain, TTreeIndex, TFile
from objects import *

class sample:

	identifier = None
	error_treatment = None

	reco_tree_chain  = None
	part_tree_chain  = None
	reco_level_struct = None
	part_level_struct = None

	input_file    = ''
	observables   = []

	migr_matrices 	= []

	efficiencies	= []
	fake_rates	= []
	efficiencies_bi = []
	fake_rates_bi   = []

	reco_histograms = []
	part_histograms = []


	def __init__(self, identifier, input_file, observables, error):

	    self.identifier  = identifier
	    self.error_treatment = error
	    self.input_file  = input_file
	    self.observables = observables
	    self.reco_tree_chain  = TChain('nominal')
	    self.part_tree_chain  = TChain('particleLevel')

	def init_objects(self):

	    for obs in self.observables:
		self.migr_matrices.append( migration_matrix(obs) ) 
		self.efficiencies.append( efficiency(obs) )
		self.fake_rates.append( fake_rates(obs) )

		self.reco_histograms.append( reco_hist(obs) )
		self.part_histograms.append( part_hist(obs) )

	    if self.error_treatment == 'binomial':
		for obs in self.observables:
		    efficencies_bi.append( efficiency_binomial(obs) )
		    fake_rates_bi.append( fake_rates_binomial(obs) )

	def migration_normalize(self):

	    for matrix in self.migr_matrices:
		matrix.normalize()

	    for i, obs in enumerate( self.observables ):

		self.efficiencies[i].hist.Sumw2()
		self.efficiencies[i].hist.Divide( self.part_histograms[i].hist )

		for bin in range( obs.nbins + 2 ):
		    e = self.efficiencies[i].hist.GetBinContent( bin )
		    if self.part_histograms[i].hist.GetBinContent( bin ) > 0 and e > 0 and e < 1:
			self.efficiencies[i].hist.SetBinError( bin, sqrt( e*(1-e)/self.part_histograms[i].hist.GetBinContent( bin )) )

		self.fake_rates[i].hist.Sumw2()
		self.fake_rates[i].hist.Divide( self.reco_histograms[i].hist )

		for bin in range( obs.nbins + 2 ):
		    e = self.fake_rates[i].hist.GetBinContent( bin )
		    if self.reco_histograms[i].hist.GetBinContent( bin ) > 0 and e > 0 and e < 1:
			self.fake_rates[i].hist.SetBinError( bin, sqrt( e*(1-e)/self.reco_histograms[i].hist.GetBinContent( bin )) )


	def migration_write_output(self, identifier):

	    migr_file = TFile( identifier + '/migration_matrix.root', 'NEW' )
	    for matrix in self.migr_matrices:
		matrix.hist.SetDirectory( migr_file )
		matrix.hist.Write()
		matrix.hist.SetDirectory(0)

	    migr_file.Close()

	def migration_draw(self, identifier):

	    for matrix in self.migr_matrices:
		matrix.draw( identifier )

	def efficiencies_write_output(self, identifier):

	    eff_file = TFile( identifier + '/efficiencies.root', 'NEW' )
	    for eff in self.efficiencies:
		eff.hist.SetDirectory( eff_file )
		eff.hist.Write()
		eff.hist.SetDirectory(0)

	    eff_file.Close()

	def efficiencies_draw(self, identifier):

	    for eff in self.efficiencies:
		eff.draw( identifier )

	def fakes_write_output(self, identifier):

	    facc_file = TFile( identifier + '/fake_rates.root', 'NEW' )
	    for facc in self.fake_rates:
		facc.hist.SetDirectory( facc_file )
		facc.hist.Write()
		facc.hist.SetDirectory(0)

	    facc_file.Close()

	def fakes_draw(self, identifier):

	    for facc in self.fake_rates:
		facc.draw( identifier )

	def import_data(self):

	    if self.input_file == '': ERROR('import_data: No input file given')

	    fileh = open(self.input_file)
	    for sample in fileh:
		filename = sample.split('\n')[0]
		print 'Adding ' + filename.split('/')[-1] + ' to the samples list...'
		self.reco_tree_chain.Add(filename)
		self.part_tree_chain.Add(filename)
	    fileh.close()
	    

	def synchronize_trees(self):

	    ## TODO : add vector obs

	    reco_index = TTreeIndex( self.reco_tree_chain, 'runNumber', 'eventNumber' )
	    part_index = TTreeIndex( self.part_tree_chain, 'runNumber', 'eventNumber' )
	    self.reco_tree_chain.SetTreeIndex( reco_index )
	    self.part_tree_chain.SetTreeIndex( part_index )

	    ## The variables holding the values as the populate_.() methods
	    ## loop through the trees are declared in a C struct. This is not
	    ## optimal. Maybe it ought to be replaced by a dynamic class, 
	    ## something along the lines of:

	    ##		list_obs = dict( (k.name, None) for k in self.observables )
	    ##		list_obs.update( {'runNumber': -99, 'eventNumber': -99} )
	    ##		event = type( 'event', (), list_obs)


	    struct1 = 'struct reco_level_struct_t{UInt_t runNumber;ULong64_t eventNumber;'
	    struct2 = 'struct part_level_struct_t{UInt_t runNumber;ULong64_t eventNumber;'

	    for obs in self.observables:
		struct1 += obs.typ + ' ' + obs.name + '_reco;'
		struct2 += obs.typ + ' ' + obs.name + '_part;'

	    struct1 += '}'
	    struct2 += '}'

	    gROOT.ProcessLine(struct1)
	    gROOT.ProcessLine(struct2)

	    from ROOT import reco_level_struct_t, part_level_struct_t

	    self.reco_level_struct = reco_level_struct_t()
	    self.part_level_struct = part_level_struct_t()

	    ## Set the tree branches to the struct observables declared above

	    self.reco_tree_chain.SetBranchAddress( 'runNumber', AddressOf(self.reco_level_struct, 'runNumber') )
	    self.reco_tree_chain.SetBranchAddress( 'eventNumber', AddressOf(self.reco_level_struct, 'eventNumber') )
	    for obs in self.observables:
		self.reco_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(self.reco_level_struct, obs.name + '_reco') )
		self.part_tree_chain.SetBranchAddress( 'tma_' + obs.name, AddressOf(self.part_level_struct, obs.name + '_part') )

	    

	def populate_up(self, identifier):

	    reco_hist_file = TFile( identifier + '/reco_level.root', 'NEW' )

	    ## Loop over all events
	    print '*************************************\n'+\
		  '******* Populating reco level *******\n'+\
		  '*************************************\n'
	    for i in range( self.reco_tree_chain.GetEntries() ):
		if ((i+1) % 1000) == 0: print 'Processing event number ' + str(i+1) + '...'

		self.reco_tree_chain.GetEntry(i)

		for j, obs in enumerate( self.observables ):
		    y = obs.name + '_reco'
		    self.reco_histograms[j].hist.SetDirectory( reco_hist_file )
		    self.reco_histograms[j].hist.Fill( getattr( self.reco_level_struct, y ), self.reco_tree_chain.weight_mc )

		## If the event exists on the particle level, fill out the migration matrices, efficiencies and fakes
		if self.part_tree_chain.GetEntryWithIndex( self.reco_level_struct.runNumber,
							   self.reco_level_struct.eventNumber ) >= 0:

		    for j, obs in enumerate( self.observables ):
			x = obs.name + '_part'
			y = obs.name + '_reco'

			self.migr_matrices[j].hist.Fill( getattr(self.part_level_struct, x), getattr(self.reco_level_struct, y),
					       		 self.part_tree_chain.weight_mc )
			self.efficiencies[j].hist.Fill(  getattr(self.part_level_struct, x), self.part_tree_chain.weight_mc )
			self.fake_rates[j].hist.Fill(    getattr(self.reco_level_struct, y), self.reco_tree_chain.weight_mc )

			if self.error_treatment == 'binomial':
			    self.efficiencies_bi[j].hist.FillWeighted( kTRUE, self.part_tree_chain.weight_mc,
							               getattr( self.part_level_struct, x ) )
			    self.fake_rates_bi[j].hist.FillWeighted(   kTRUE, self.reco_tree_chain.weight_mc,
							               getattr( self.reco_level_struct, y ) )

		## If the event only exists on reco level, still fill out the total histo for TEfficiencies
		else:

		    if self.error_treatment == 'binomial':
			for j, obs in enumerate( self.observables ):
			    y = obs.name + '_reco'
			    self.fake_rates_bi[j].hist.FillWeighted( kFALSE, self.reco_tree_chain.weight_mc,
						                     getattr( self.reco_level_struct, y ) )

	    for j, obs in enumerate( self.observables ):
		self.reco_histograms[j].hist.Write()
		self.reco_histograms[j].hist.SetDirectory(0)

	    reco_hist_file.Close()


	def populate_down(self, identifier):

	    part_hist_file = TFile( identifier + '/part_level.root', 'NEW' )

	    print '*************************************\n'+\
		  '******* Populating part level *******\n'+\
		  '*************************************\n'
	    for i in range( self.part_tree_chain.GetEntries() ):
		if ((i+1) % 1000) == 0: print 'Processing event number ' + str(i+1) + '...'

		self.part_tree_chain.GetEntry(i)

		for j, obs in enumerate( self.observables ):
		    x = obs.name + '_part'
		    self.part_histograms[j].hist.SetDirectory( part_hist_file )
		    self.part_histograms[j].hist.Fill( getattr( self.part_level_struct, x ), self.part_tree_chain.weight_mc )

		## Fill the total histogram if event only on particle-level
		if ( self.reco_tree_chain.GetEntryWithIndex( self.part_level_struct.runNumber,
		     self.part_level_struct.eventNumber ) < 0 ) and self.error_treatment == 'binomial': 

		    for j, obs in enumerate( self.observables ):
			x = obs.name + '_part'
			efficiencies_bi[j].hist.FillWeighted( kFALSE, self.part_tree_chain.weight_mc,
							      getattr( self.part_level_struct, x ) )

	    for j, obs in enumerate( self.observables ):
		self.part_histograms[j].hist.Write()
		self.part_histograms[j].hist.SetDirectory(0)

	    part_hist_file.Close()
