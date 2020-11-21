

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
    parser.add_option('-C', '--command', dest='cmd', help='command to launch', metavar='COMMAND')
    parser.add_option('-N', '--nprocess', default=None, dest='nprocess', help='number of process', metavar='NUMBER')
    parser.add_option('-S', '--autostart', default=None, dest='autostart', help='start at launch', metavar='yes/no')
    parser.add_option('-O', '--stdout', default=None, dest='stdout', help='standard output redirect file', metavar='FILE')
    parser.add_option('-E', '--stderr', default=None, dest='stderr', help='standard error redirect file', metavar='FILE')
    parser.add_option('-U', '--umask', default=None, dest='umask', help='umask to set before launching the program', metavar='NUMBER')
    parser.add_option('--name', dest='name', help='name of command', metavar='NAME')
    parser.add_option('--restart', default=None, dest='restart', help='should Restarted', metavar='always/never/unexpcted_exit')
    parser.add_option('--exitcodes', default=None, dest='exitcodes', help='return code represent expected exit', metavar='NUMBER,...')
    parser.add_option('--starttime', default=None, dest='starttime', help='time to consider successfully started in seconds', metavar='NUMBER_SECONDS')
    parser.add_option('--stoptime', default=None, dest='stoptime', help='time to consider successfully stopped in seconds', metavar='NUMBER_SECONDS')
    parser.add_option('--startretries', default=None, dest='startretries', help='restart attempts before aborted', metavar='NUMBER')
    parser.add_option('--stopsignal', default=None, dest='stopsignal', help='signal to stop program', metavar='SIGNAME,...')
    parser.add_option('--env', default=None, dest='env', help='environment variables', metavar='KEY=VAL,...')
    parser.add_option('--workingdir', default=None, dest='workingdir', help='working directory', metavar='STRING')
    
    (options, _) = parser.parse_args()
    (file, mustShow, configuration) = clean_options(options)

    switch = Switch()
    switch.add_case(lambda : mustShow, lambda : surround_exit(show_file, file))
    switch.add_case(lambda : path.exists(file), lambda : surround_exit(update_file, file, configuration))
    switch.add_case(lambda : not path.exists(file), lambda : surround_exit(create_file, file, configuration))
    switch.switch()

if __name__ == '__main__':
    manage_configuration_file()

