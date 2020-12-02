import json,sys, os
from signals import handler_signal
from exec import run_all_jobs
import exec
from kk import message
from clss import jobs , program , node
from subprocess import Popen , check_output
from collections import defaultdict
import socket
from config import HOST, PORT, read, write
from switch import Switch
import sys

def load_file(name_file):
    job = jobs()
    with open(name_file) as json_data_file:
        data = json.load(json_data_file)
        keys = list(data.keys())
        for key in keys:
            job.names.append(key)
        print("load_file",job.names)
        for name in job.names:
            job.list_jobs[name]= node(name, get_setting_program(data[name], name))
    print("___", job.names)
    return job



def get_setting_program(setting,name):
    pr = program()
    keys=setting.keys()
    pr.name=name
    pr.cmd=setting["cmd"]
    pr.env=setting["env"]
    pr.stdout=setting["stdout"]
    pr.stderr=setting["stderr"]
    pr.umask=setting["umask"]
    pr.workingdir=setting["workingdir"]
    pr.autostart=setting["autostart"]
    pr.autorestart=setting["autorestart"]
    pr.exitcodes=setting["exitcodes"]
    pr.startretries=setting["startretries"]
    pr.starttime=setting["starttime"]
    pr.stopsignal=setting["stopsignal"]
    pr.stoptime=setting["stoptime"]
    return pr

def trait_data_json(file):
    pass


def get_pid(conn):
    write(conn, F"{os.getpid()}")

def stop_proccess(jobs, name):
    
    pass

def start_proccess(jobs, name):
    
    pass

def send_signal(jobs, sig):

    pass

def status(jobs):
    
    pass

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
    except OSError as e:
        print(e)
        exit(1)

    jobs = load_file(sys.argv[1])
    run_all_jobs(jobs)

    while True:
        server.listen()
        conn, _ = server.accept()
        req = read(conn).split(' ')
        switch = Switch()
        switch.add_case(lambda : req[0] == 'getpid', lambda : get_pid(conn))
        switch.add_case(lambda : req[0] == 'stop', lambda : stop_proccess(jobs, req[1]))
        switch.add_case(lambda : req[0] == 'start', lambda : start_proccess(jobs, req[1]))
        switch.add_case(lambda : req[0] == 'signal', lambda : send_signal(jobs, req[1]))
        switch.add_case(lambda : req[0] == 'status', lambda : status(jobs))
        switch.add_case(lambda : req[0] == 'close', lambda : exit(0))
        switch.switch()
        conn.close()

        #handler_signal()
        #if exec.global_signal > -1:
        #    print("nbr_signalmain=", exec.dic_signal[exec.global_signal])
        #line=input()
        #if line == "exit":
        #    sys.exit()
        #print(line)



if __name__ == "__main__":
    main()

    #print(data.keys())
        #data['run']['cmd']))
