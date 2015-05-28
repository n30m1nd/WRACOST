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

        if (cookiefile):
            file_data = ""
            with open(cookiefile) as cfile:
                file_data = "".join(line.rstrip() for line in cfile)
            self.arg_cookie = cookie_parser.CookieParser().parseOneLineCookie(file_data)

        if restparamsdict:
            self.arg_paramdict = restparamsdict

        #   Useless if this class is used by any other files than this  #
        self.lock = threading.Lock()

    def do_request(self, method=None, url=None, cookie=None):
        if not (method):
            method = self.arg_method
        if not (url):
            url = self.arg_url
        if not(cookie):
            cookie = self.arg_cookie
        try:
            req_sent = ""
            #   Entering critical section   #
            if (method == "POST"):
                self.semaphore.acquire()
                req_sent =requests.post(url, data=self.arg_paramdict, cookies=cookie)
            elif(method == "GET"):
                self.semaphore.acquire()
                req_sent = requests.get(url, cookies=cookie)
            elif(method == 'HEAD'):
                self.semaphore.acquire()
                req_sent = requests.head(url, cookies=cookie)
            else:
                self.lock.acquire()
                exit ("[-] Method not implemented yet...")
                self.lock.release()
            #   End of critical section     #
            self.lock.acquire()
            sys.stdout.write("[+]\tRequest sent ")
            if (arg_verbosity > 0):
                print "to:", arg_url
                print "[+]\t\tmethod:", arg_method
                if (self.arg_method!="GET"):
                    print "[+]\t\tpayload:", self.arg_paramdict
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
        if (paramdict):
            if (self.arg_paramdict):
                self.arg_paramdict.update(paramdict)
            else:
                self.arg_paramdict = paramdict
        self.do_request()

if __name__ == "__main__":
    #   Set the command line arguments  #
    parser = arg_parser.WracostArgs()
    arg_url = parser.args.url
    arg_nthreads = parser.args.threads
    arg_verbosity = parser.args.v
    arg_method = parser.args.method
    arg_params = parser.args.params
    arg_payloads = parser.args.payloads
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
    semaphore = threading.Semaphore(0)
    lock = threading.Lock()
    if (arg_method != 'POST'):
        for i in range(arg_nthreads):
            t = threading.Thread(target=wracost.run, args=(lock, semaphore, ))
            threads.append(t)
            t.start()
    else:
        for paramdict in parser.get_params_dict():
            t = threading.Thread(target=wracost.run, args=(lock, semaphore, paramdict))
            threads.append(t)
            t.start()


    if (arg_nthreads > 2):
        #   Wait for all threads to get to the critical section #
        __import__("time").sleep(0.2*arg_nthreads)

    for i in range(arg_nthreads):
        semaphore.release()
