
class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def ERROR(msg):
  print colors.FAIL + "ERROR: " + colors.ENDC + msg
  print "Exiting..."
  sys.exit()

def WARNING(msg):
# raw_input returns the empty string for "enter"
  print colors.WARNING + "WARNING: " + colors.ENDC + msg
