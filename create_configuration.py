

# implement configuration file creation

import json
import getopt, sys
from optparse import OptionParser
from os import path


parser = OptionParser(usage='Usage: %prog -c configurationfile [options]')

parser.add_option('-c', '--configurationfile', dest='configurationfile', help='create configuration file | add new configuration', metavar='FILE')
parser.add_option('-s', '--show', default=False, action='store_true', dest='show', help='show configuration file')
parser.add_option('-C', '--command', dest='command', help='command to launch', metavar='COMMAND')
parser.add_option('-N', '--nprocess', default='1', dest='nprocess', help='number of process', metavar='NUMBER')
parser.add_option('-S', '--startup', default='no', dest='startup', help='start at launch', metavar='yes/no')
parser.add_option('-O', '--output', default='1', dest='output', help='standard output redirect file', metavar='FILE')
parser.add_option('-E', '--error', default='2', dest='error', help='standard error redirect file', metavar='FILE')
parser.add_option('-U', '--umask', default=None, dest='umask', help='umask to set before launching the program', metavar='NUMBER')
parser.add_option('--restart', default='never', dest='restart', help='should Restarted', metavar='always/never/unexpcted_exit')
parser.add_option('--returncode', default='0', dest='returncode', help='return code represent expected exit', metavar='NUMBER')
parser.add_option('--starttime', default='1', dest='starttime', help='time to consider successfully started in seconds', metavar='SECONDS')
parser.add_option('--stoptime', default='1', dest='stoptime', help='time to consider successfully stopped in seconds', metavar='SECONDS')
parser.add_option('--attempts', default='0', dest='attempts', help='restart attempts before aborted', metavar='NUMBER')
parser.add_option('--stopsignal', default='2', dest='stopsignal', help='signal to stop program', metavar='NUMBER')
parser.add_option('--environment', default=None, dest='environment', help='environment variables', metavar='STRING')
parser.add_option('--directory', default=None, dest='directory', help='working directory', metavar='STRING')

(options, args) = parser.parse_args()

if not options.configurationfile:
    parser.error('Missing Required parameter: -c configurationfile')

if options.show:
    if path.exists(options.configurationfile):
        with open(options.configurationfile, 'r') as configurationfile:
            try:
                configurations = json.load(configurationfile)
                if not isinstance(configurations, list):
                    raise 'error'
            except:
                print(options.configurationfile + ': not a valid file!')
                exit(2)
            print(json.dumps(configurations, indent=4))
    else:
        print(options.configurationfile + ': file not found!')
    exit(0)

if not options.command:
    parser.error('Missing Required parameter: -C COMMAND')

if not path.exists(options.configurationfile):
    with open(options.configurationfile, 'w') as configurationfile:
        del options.configurationfile
        del options.show
        json.dump([vars(options)], configurationfile, indent=4)
else:
    with open(options.configurationfile, 'r+') as configurationfile:
        try:
            configurations = json.load(configurationfile)
            if not isinstance(configurations, list):
                raise 'error'
        except:
            print(options.configurationfile + ': not a valid file!')
            exit(2)
        configurationfile.seek(0)
        del options.configurationfile
        del options.show
        configurations.append(vars(options))
        json.dump(configurations, configurationfile, indent=4)