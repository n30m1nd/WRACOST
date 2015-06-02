#-*- coding: utf-8 -*-

__author__ = 'n30'

import httplib
from urlparse import urlparse
import threading
import sys
import requests
from core import arg_parser, cookie_parser


class WRACOST():

    def __init__(self, url, method, verbosity=0, cookiefile=None, restparamsdict=None):
        #   Set the command line arguments  #
        self.arg_url = url
        self.arg_method = method
        self.arg_verbosity = verbosity
        self.arg_paramdict = {}
        self.arg_cookie = None

        if (cookiefile):
            file_data = ""
            with open(cookiefile) as cfile:
                file_data = "".join(line.rstrip() for line in cfile)
            self.arg_cookie = cookie_parser.CookieParser().parseOneLineCookie(file_data)

        #   Useless if this class is used by any other files than this  #
        self.lock = threading.Lock()

    def do_request(self, method=None, url=None, cookie=None, paramsdict=None):
        if not (method):
            method = self.arg_method
        if not (url):
            url = self.arg_url
        if not(cookie):
            cookie = self.arg_cookie
        try:
            req_sent = ""
            #   Entering critical section   #
            self.semaphore.acquire()
            req_sent = requests.request(method, url, data=paramsdict, cookies=cookie)
            #   End of critical section     #
            self.lock.acquire()
            sys.stdout.write("[+]\tRequest sent ")
            if (arg_verbosity > 0):
                print "to:", arg_url
                print "[+]\t\tmethod:", arg_method
                print "[+]\t\tpayload:", paramsdict
                print "[+]\tresponse headers: "
                for header_name in req_sent.headers:
                    print "[+]\t\t", header_name, ":", req_sent.headers[header_name]
                print "[+]\tCookie \n[i]\t[output info] { 'key' : 'value' }:"
                print "[+]\t\t", self.arg_cookie
                print
            self.lock.release()

        except httplib.HTTPException as ex:
            self.lock.acquire()
            print "[-] Connection error: ", ex.message
            self.lock.release()
        except Exception as ex:
            self.lock.acquire()
            print "[-] Error: ", str(ex)
            self.lock.release()


    def run(self, lock, semaphore, paramdict=None):
        self.lock = lock
        self.semaphore = semaphore
        self.do_request(paramsdict=paramdict)

if __name__ == "__main__":
    #   Set the command line arguments  #
    parser = arg_parser.WracostArgs()
    arg_url = parser.args.url
    arg_nthreads = parser.args.threads
    arg_verbosity = parser.args.v
    arg_method = parser.args.method
    arg_params = parser.args.params
    arg_getreq = parser.args.getreq
    arg_cookiefile = parser.args.cfile
    #   End of setting the arguments    #

    #   Init                            #
    wracost = WRACOST(arg_url, arg_method, arg_verbosity, arg_cookiefile)

    print "WRACOST v1.1 ( www.github.com/n30m1nd )"
    print
    print "[+] Starting requests..."

    if (arg_verbosity > 0):
            print "[+]\t\tURL: ", arg_url
            print "[+]\t\tThreads: ", arg_nthreads
            print

    threads = []
    wait_nthreads = 0
    semaphore = threading.Semaphore(0)
    lock = threading.Lock()
    if (arg_nthreads):
        for i in range(arg_nthreads):
            wait_nthreads += 1
            t = threading.Thread(target=wracost.run, args=(lock, semaphore, arg_getreq))
            threads.append(t)
            t.start()
    else:
        for paramdict in parser.get_params_dict():
            wait_nthreads += 1
            t = threading.Thread(target=wracost.run, args=(lock, semaphore, paramdict.copy()))
            threads.append(t)
            t.start()


    if (wait_nthreads > 2):
        #   Wait for all threads to get to the critical section #
        __import__("time").sleep(0.2*wait_nthreads)

    for i in range(wait_nthreads):
        semaphore.release()
