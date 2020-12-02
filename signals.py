from signal import *
import sys
import exec
#global global_signal

# global_signal=-1


def receiveSignal(nbr_signal, param):
    exec.global_signal = nbr_signal


def handler_signal():
    signal(SIGHUP, receiveSignal)
    signal(SIGINT, receiveSignal)
    signal(SIGQUIT, receiveSignal)
    signal(SIGILL, receiveSignal)
    signal(SIGTRAP, receiveSignal)
    signal(SIGABRT, receiveSignal)
    signal(SIGBUS, receiveSignal)
    signal(SIGFPE, receiveSignal)
    #signal(SIGKILL, receiveSignal)
    signal(SIGUSR1, receiveSignal)
    signal(SIGSEGV, receiveSignal)
    signal(SIGUSR2, receiveSignal)
    signal(SIGPIPE, receiveSignal)
    signal(SIGALRM, receiveSignal)
    signal(SIGTERM, receiveSignal)
