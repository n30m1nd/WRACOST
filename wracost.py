#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'n30m1nd'

import httplib
import requests
from core import arg_parser, cookie_parser
import time
from multiprocessing import Process, Lock, Semaphore, Value
import ctypes


class WRACOST():

    def __init__(self, url, method, verbosity=0, proxy=None ,cookiefile=None, headers=None, locked=None, forceurl=False):
        #   Set the command line arguments  #
        self.arg_url = url
        self.arg_method = method
        self.arg_verbosity = verbosity
        self.arg_paramdict = {}
        self.arg_proxy = proxy
        self.arg_cookie = None
        self.arg_headers = requests.utils.default_headers()
        self.arg_headers.update({"User-Agent": "WRACOST/0.9"})
        self.arg_forceurl = forceurl
        self.locked = locked

        if (headers):
            self.arg_headers.update(headers)

        if (cookiefile):
            file_data = ""
            with open(cookiefile) as cfile:
                file_data = "".join(line.rstrip() for line in cfile)
            self.arg_cookie = cookie_parser.CookieParser().parseOneLineCookie(file_data)

        #   Useless if this class is used by any other files than this  #
        self.lock = Lock()

    def do_request(self, url, method="GET", cookie=None, paramsdict=None, headers_loc=None, forceurl=False):
        try:
            #   Entering critical section   #
            # There is no observer pattern implemented on python...
            while self.locked.value:
                pass
            # threadtime = time.time()
            if forceurl:
                req_return = requests.request(method, url, params=paramsdict, proxies=self.arg_proxy, cookies=cookie, headers=headers_loc)
            else:
                req_return = requests.request(method, url, data=paramsdict, proxies=self.arg_proxy, cookies=cookie, headers=headers_loc)
            self.lock.acquire()
            #   End of critical section     #
            print ("[+]\tResponse received from: %s [%d]") % (req_return.url, req_return.status_code)
            if (arg_verbosity > 0):
            #   print "[+]\t\ttime: %f " % (threadtime)
                print "[+]\t\tmethod:", method
                print "[+]\t\tpayload:", paramsdict
                print "[+]\t\theaders:", req_return.request.headers
                print "[+]\tresponse headers: "
                for header_name in req_return.headers:
                    print "[+]\t\t", header_name, ":", req_return.headers[header_name]
                if (self.arg_proxy):
                    print "[+] Using proxy:", self.arg_proxy
                print "[+]\tCookie { 'name' : 'value' }:"
                print "[+]\t\t", self.arg_cookie
                if (arg_verbosity > 1):
                    print "******** SOURCE CODE FROM:", req_return.url, "********"
                    print req_return.text
                    print "****** END OF SOURCE CODE:", req_return.url, "********"
                print
            self.lock.release()

        except httplib.HTTPException as ex:
            self.lock.acquire()
            print "[-] Connection error: ", ex.message
            self.lock.release()
        except requests.exceptions.InvalidHeader as ex:
            self.lock.acquire()
            print "[-] Invalid headers, check trailing spaces: ", ex.message
            self.lock.release()


    def run(self, lock, paramdict=None):
        self.lock = lock
        self.do_request(self.arg_url, method=self.arg_method, cookie=self.arg_cookie, paramsdict=paramdict,
                        headers_loc=self.arg_headers, forceurl=self.arg_forceurl)

if __name__ == "__main__":
    print "WRACOST v0.9 ( www.github.com/n30m1nd )"
    print
    #   Set the command line arguments  #
    parser = arg_parser.WracostArgs()
    arg_url = parser.args.url
    arg_nthreads = parser.args.threads
    arg_verbosity = parser.args.v
    arg_method = parser.args.method
    arg_params = parser.args.params
    arg_getreq = parser.args.getreq
    arg_proxy = parser.args.proxy
    arg_cookiefile = parser.args.cfile
    arg_headers = parser.args.headers
    arg_forceurl = parser.args.forceurl
    arg_auto = parser.args.auto
    #   End of setting the arguments    #

    #   Init with command line args     #
    shared_lock_launch = Value(ctypes.c_bool)
    shared_lock_launch.value = True
    wracost = WRACOST(arg_url, arg_method, arg_verbosity, arg_proxy, arg_cookiefile, arg_headers, shared_lock_launch, arg_forceurl)

    print "[+] Starting requests..."

    if (arg_verbosity > 0):
            print "[+]\t\tURL: ", arg_url
            print "[+]\t\tThreads: ", arg_nthreads
            print

    threads = []
    stdout_lock = Lock()
    if (arg_nthreads):
        for i in range(arg_nthreads):
            t = Process(target=wracost.run, args=(stdout_lock, arg_getreq))
            threads.append(t)
            t.start()
    else:
        paramsdictionary = parser.get_params_dict()
        for singleparam in paramsdictionary:
            # Meed a .copy() because each thread needs it's own object
            t = Process(target=wracost.run, args=(stdout_lock, singleparam.copy()))
            threads.append(t)
            t.start()

    if arg_auto or raw_input("[+] All threads synchronised! Launch attack?(Y/n): ") != 'n':
        with shared_lock_launch.get_lock():
            shared_lock_launch.value = False
            print "[+] Requests launched!"
    else:
        for thread in threads:
            thread.terminate()
