

# implement configuration file creation

import json
import getopt, sys
from optparse import OptionParser
from os import path
from manage_file import show_file, create_file, update_file
from check import is_key_exists
from tool import clean_options, surround_exit
from switch import Switch

def manage_configuration_file(standalone=None):
    parser = OptionParser(usage=F'Usage: %prog {standalone if standalone else ""} -c configurationfile [options]')

    if standalone:
        parser.add_option(F'--{standalone}', dest='standalone', action='store_true')
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
    (options, _) = parser.parse_args()
    (file, mustShow, configuration) = clean_options(options)

    switch = Switch()
    switch.add_case(lambda : mustShow, lambda : surround_exit(show_file, file))
    switch.add_case(lambda : path.exists(file), lambda : surround_exit(update_file, file, configuration))
    switch.add_case(lambda : not path.exists(file), lambda : surround_exit(create_file, file, configuration))
    switch.switch()

if __name__ == '__main__':
    manage_configuration_file()