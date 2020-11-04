from optparse import OptionParser
from manager import manage_configuration_file



parser = OptionParser()

parser.add_option('--create', dest='create', action='store_true', default=False)

(options, args) = parser.parse_args()

if options.create:
    manage_configuration_file(standalone='create')