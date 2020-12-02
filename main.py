import json
import sys
import os
from signals import handler_signal
from exec import run_all_jobs
import exec
from kk import message
from clss import jobs, program, node
from subprocess import Popen, check_output
from collections import defaultdict
import socket
from config import HOST, PORT, read, write
from switch import Switch
import sys


def load_file(name_file):
    job = jobs()
    with open(name_file) as json_data_file:
        data = json.load(json_data_file)
        print("load_file", job.names)
        # keys = list(data.keys())
        for key in list(data.keys()):
            job.names.append(key)
        # for name in job.names:
            job.list_process[name] = get_setting_program(data[name], name)
    print("___", job.names)
    return job


# def get_setting_program(setting, name):
#     pr=program()
#     keys=setting.keys()
#     pr.name=name
#     pr.cmd=setting["cmd"]
#     pr.env=setting["env"]
#     pr.stdout=setting["stdout"]
#     pr.stderr=setting["stderr"]
#     pr.umask=setting["umask"]
#     pr.workingdir=setting["workingdir"]
#     pr.autostart=setting["autostart"]
#     pr.autorestart=setting["autorestart"]
#     pr.exitcodes=setting["exitcodes"]
#     pr.startretries=setting["exitcodes"]
#     pr.starttime=setting["starttime"]
#     pr.stopsignal=setting["stopsignal"]
#     pr.stoptime=setting["stoptime"]
#     return pr

data_name = ["cmd", "env", " stdout", "stderr", "umask", "workingdir",
             "autostart", "autorestart", "exitcodes", "starttime", "stopsignal", "stoptime"]


def get_setting_program(setting, name):
    process = program()
    process.name = name
    keys = setting.keys()
    keys = setting.keys()
    for key in keys:
        if key in data_name:
            # // my_calculator.('button_%d' % i) = tkinter.Button(root, text=i)
            #    // process.('%s'% key) = setting[name]
            # //process.create_new_var(key, setting[name])
        print(key)
    return process


def get_pid(conn):
    write(conn, F"{os.getpid()}")


def stop_proccess(jobs, name):
    if name in jobs.names:
        jobs.list_jobs[name].start()  # kill process;
    else:
        return "this programe does not exist"
    return "successfully"


def start_proccess(jobs, name):
    if name in jobs.names:
        jobs.list_jobs[name].start()
    else:
        return "this programe does not exist"
    return "successfully"


def send_signal(jobs, sig):
    for key, value in exec.dic_signal.items():
        if value == sig:
            exec.global_signal = key
            return "successfully"
    return ("this signal does not exist")


def status(jobs):  # string.ljust(7, ' ')
    print("%10s %20s   %30s %20s" % ("PID", "NAME", "COMMAND", "STATUS"))
    for name in jobs.names:
        info = jobs.list_process[name]
        if info.out_cmd is None:
            status_ = "not start"
        elif (info.out_cmd.pull() is None)
        status_ = "run"
        else:
            status_ = str(info.out_cmd.exitcodes)
        print("%10s %20s   %30s %20s" %
              (str(info.out_cmd.pid), str(name), str(info.cmd), str(status_)))


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
        switch.add_case(lambda: req[0] == 'getpid', lambda: get_pid(conn))
        switch.add_case(lambda: req[0] == 'stop',
                        lambda: stop_proccess(jobs, req[1]))
        switch.add_case(lambda: req[0] == 'start',
                        lambda: start_proccess(jobs, req[1]))
        switch.add_case(lambda: req[0] == 'signal',
                        lambda: send_signal(jobs, req[1]))
        switch.add_case(lambda: req[0] == 'status', lambda: status(jobs))
        switch.add_case(lambda: req[0] == 'close', lambda: exit(0))
        switch.switch()
        conn.close()

        # handler_signal()
        # if exec.global_signal > -1:
        #    print("nbr_signalmain=", exec.dic_signal[exec.global_signal])
        # line=input()
        # if line == "exit":
        #    sys.exit()
        # print(line)


if __name__ == "__main__":
    p = get_setting_program({'cmd': "ls", "umask": 44}, "cat")
    print(p.cmd)
    # main()

    # print(data.keys())
    # data['run']['cmd']))