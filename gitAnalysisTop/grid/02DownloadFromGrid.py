#!/usr/bin/env python
import TopExamples.grid

scope          = 'user.aknue'
datasetPattern = '*test_02-03-45a_output.root'
directory      = '/tmp/YOURUSERNAME/DownloadFolder/'

TopExamples.grid.download(scope, datasetPattern, directory)
