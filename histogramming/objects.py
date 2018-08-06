from ROOT import gStyle, TH1F, TH2F, TEfficiency, TCanvas
from math import sqrt

class observable:

        typ     = 'float'
        name    = ''
        nbins   = 0
        xmin    = 0
        xmax    = 0
        latex   = ''

        def __init__(self, typ, name, nbins, xmin, xmax, latex):

            self.typ     = typ
            self.name    = name
            self.nbins   = nbins
            self.xmin    = xmin
            self.xmax    = xmax
            self.latex   = latex

class vector_observable:

        typ     = 'float'
        name    = ''
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

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist = TH2F( 'tMatrix_' + self.obs.name, 'A_{ij} ' + self.obs.name,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax )

	def normalize(self):

	    for xbins in range( self.obs.nbins + 2 ):

		sum = 0
		for ybins in range( self.obs.nbins + 2 ):
		    sum += self.hist.GetBinContent( xbins, ybins )

		for ybins in range( self.obs.nbins + 2):
		    if sum != 0:

		        self.hist.SetBinContent( xbins, ybins, 
				self.hist.GetBinContent( xbins, ybins ) / float(sum) )

			e = self.hist.GetBinContent( xbins, ybins )
			if e > 0 and e < 1:
			    self.hist.SetBinError( xbins, ybins, 
				sqrt( e*(1-e) / float(sum) ) )

	def draw(self, identifier):

	    gStyle.SetOptStat("neou")
	    gStyle.SetPaintTextFormat(".4f")

	    c = TCanvas('c', 'c', 900, 900)
	    c.cd()

	    self.hist.GetXaxis().SetTitle( self.obs.latex + '^{part}' )
	    self.hist.GetYaxis().SetTitle( self.obs.latex + '^{reco}' )
	    self.hist.GetZaxis().SetRangeUser(0,1)
	    self.hist.SetMarkerSize(0.3)
	    self.hist.Draw('COLZ TEXT E')
	    c.SaveAs(identifier + '/Aij_' + self.obs.name + '.pdf')

	    self.hist.Draw('LEGO2Z')
	    c.SaveAs(identifier + '/Aij_' + self.obs.name + '_lego.pdf')

	    c.Close()


class efficiency:

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist = TH1F( 'tEff_' + self.obs.name, '#epsilon_{epsilon} ' + self.obs.name,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax )

	def draw(self, identifier):

	    c = TCanvas('c', 'c', 900, 900)
	    c.cd()

	    self.hist.GetXaxis().SetTitle( self.obs.latex )
	    self.hist.GetYaxis().SetTitle( '#epsilon_{eff} ' + self.obs.latex )
	    self.hist.GetYaxis().SetRangeUser(0,1)
	    self.hist.Draw('*HE')
	    c.SaveAs(identifier + '/efficiency_' + self.obs.name + '.pdf')

	    c.Close()

class efficiency_binomial:

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist  = TEfficiency( 'tEff_' + self.obs.name, '#epsilon_{epsilon} ' + self.obs.name,
                          self.obs.nbins, self.obs.xmin, self.obs.xmax )

class fake_rates:

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist = TH1F( 'tFacc_' + self.obs.name, 'f_{acc} ' + self.obs.name,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax )

	def draw(self, identifier):

	    c = TCanvas('c', 'c', 900, 900)
	    c.cd()

	    self.hist.GetXaxis().SetTitle( self.obs.latex )
	    self.hist.GetYaxis().SetTitle( 'f_{acc} ' + self.obs.latex )
	    self.hist.GetYaxis().SetRangeUser(0,1)
	    self.hist.Draw('*HE')
	    c.SaveAs(identifier + '/fakes_' + self.obs.name + '.pdf')

	    c.Close()

class fake_rates_binomial:

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist = TEfficiency( 'tFacc_' + self.obs.name, 'f_{acc} ' + self.obs.name,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax )

class reco_hist:

        obs       = None
        hist = None

        def __init__(self, observable):

            self.obs    = observable
            self.hist   = TH1F( 'tReco_' + self.obs.name, self.obs.name + '^{reco}',
                           self.obs.nbins, self.obs.xmin, self.obs.xmax )

class part_hist:

        obs     = None
        hist    = None

        def __init__(self, observable):

            self.obs     = observable
            self.hist    = TH1F( 'tPart_' + self.obs.name, self.obs.name + '^{part}',
                            self.obs.nbins, self.obs.xmin, self.obs.xmax )

