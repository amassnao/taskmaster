from optparse import OptionParser
from manager import manage_configuration_file
import sys
import socket
from switch import Switch
from subprocess import Popen
from config import HOST, PORT, read, write


def send_command(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        return False
    write(client, command)
    res = read(client)
    client.close()
    return res if res else "not implemented"

def start_server(configurationfile):
    pid = send_command("getpid")
    if pid:
        print("server already running with pid :", pid)
    else:
        Popen(F"python3 main.py {configurationfile}", shell=True)
    
def stop_server():
    if not send_command("getpid"):
        print("server not running")
    else:
        send_command("close")
    
def status():
    status = send_command("status")
    if not status:
        print("server not running")
    else:
        print(status)

def stop_process(name):
    stop = send_command(F"stop {name}")
    if not stop:
        print("server not running")
    else:
        print(stop)

def start_process(name):
    stop = send_command(F"start {name}")
    if not stop:
        print("server not running")
    else:
        print(stop)

def help(cmd):
    if cmd != 'help':
        print("unknown command!\nplease use one of the commands listed bellow")
    print("\thelp   :", "show help menu")
    print("\tstart  :", "start proccess")
    print("\tstop   :", "stop proccess")
    print("\tstatus :", "show list of process with status")
    print("\texit   :", "exit from shell")


def shell():
    res = send_command("status")
    if not res:
        print("server not running")
    while res:
        cmd = input("$> ").split()
        switch = Switch()
        switch.add_case(lambda : len(cmd) == 1 and cmd[0] == 'exit', lambda : exit(0))
        switch.add_case(lambda : len(cmd) == 1 and cmd[0] == 'status', status)
        switch.add_case(lambda : len(cmd) == 2 and cmd[0] == 'start', lambda : start_process(cmd[1]))
        switch.add_case(lambda : len(cmd) == 2 and cmd[0] == 'stop', lambda : stop_process(cmd[1]))
        switch.add_case(lambda : len(cmd) == 2 and cmd[0] == 'exit', lambda : exit(0))
        switch.add_case(lambda : len(cmd) == 1, lambda : help(cmd[0]))
        switch.switch()


parser = OptionParser()

parser.add_option('--create', dest='create', action='store_true', help="create configuration file", default=False)
parser.add_option('--startserver', dest='startserver', help='start taskmaster deamon with configuration file', metavar='FILE')
parser.add_option('--stopserver', dest='stopserver', action='store_true', help="stop taskmaster deamon", default=False)
parser.add_option('--status', dest='status', action='store_true', help='show list of process', default=False)
parser.add_option('--stop', dest='stopprocess', default=False, help='stop proccess', metavar='COMMAND')
parser.add_option('--start', dest='startprocess', default=False, help='start proccess', metavar='COMMAND')
parser.add_option('--shell', dest="shell", action='store_true', help='start a stable shell', default=False)


if '--create' in sys.argv:
    (options, args) = parser.parse_args(sys.argv[0:2])
else:
    (options, args) = parser.parse_args()

switch = Switch()

switch.add_case(lambda : options.create, lambda : manage_configuration_file(standalone='create'))
switch.add_case(lambda : options.startserver, lambda : start_server(options.startserver))
switch.add_case(lambda : options.stopserver, stop_server)
switch.add_case(lambda : options.status, status)
switch.add_case(lambda : options.stopprocess, lambda : stop_process(options.stopprocess))
switch.add_case(lambda : options.startprocess, lambda : start_process(options.startprocess))
switch.add_case(lambda : options.shell, shell)

switch.switch()


