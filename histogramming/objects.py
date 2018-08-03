from ROOT import TH1F, TH2F, TEfficiency

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

class efficiency:

        obs     = None
        hist     = None

        def __init__(self, observable):

            self.obs  = observable
            self.hist = TH1F( 'tEff_' + self.obs.name, '#epsilon_{epsilon} ' + self.obs.name,
                         self.obs.nbins, self.obs.xmin, self.obs.xmax )

class efficiency_binomial:

        obs     = None
        hist     = None

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

