#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'n30m1nd'

import httplib
import threading
import requests
from core import arg_parser, cookie_parser


class WRACOST():

    def __init__(self, url, method, verbosity=0, proxy=None ,cookiefile=None, headers=None, forceurl=False):
        #   Set the command line arguments  #
        self.arg_url = url
        self.arg_method = method
        self.arg_verbosity = verbosity
        self.arg_paramdict = {}
        self.arg_proxy = proxy
        self.arg_cookie = None
        self.arg_headers = requests.utils.default_headers()
        self.arg_forceurl = forceurl

        if (headers):
            self.arg_headers.update(headers)

        if (cookiefile):
            file_data = ""
            with open(cookiefile) as cfile:
                file_data = "".join(line.rstrip() for line in cfile)
            self.arg_cookie = cookie_parser.CookieParser().parseOneLineCookie(file_data)

        #   Useless if this class is used by any other files than this  #
        self.lock = threading.Lock()

    def do_request(self, url, method="GET", cookie=None, paramsdict=None, headers_loc=None, forceurl=False):
        try:
            #   Entering critical section   #
            self.semaphore.acquire()
            if forceurl:
                req_return = requests.request(method, url, params=paramsdict, proxies=self.arg_proxy, cookies=cookie, headers=headers_loc)
            else:
                req_return = requests.request(method, url, data=paramsdict, proxies=self.arg_proxy, cookies=cookie, headers=headers_loc)
            #   End of critical section     #

            self.lock.acquire()
            print ("[+]\tRequest sent to: %s") % (req_return.url)
            if (arg_verbosity > 0):
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
        finally:
            try:
                self.lock.release()
            except:
                pass


    def run(self, lock, semaphore, paramdict=None):
        self.lock = lock
        self.semaphore = semaphore
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
    #   End of setting the arguments    #

    #   Init with command line args     #
    wracost = WRACOST(arg_url, arg_method, arg_verbosity, arg_proxy, arg_cookiefile, arg_headers, arg_forceurl)

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
            # Meed a .copy() because each thread needs it's own object
            t = threading.Thread(target=wracost.run, args=(lock, semaphore, paramdict.copy()))
            threads.append(t)
            t.start()

    if (wait_nthreads > 2):
        #   Wait for all threads to get to the critical section #
        # TODO: Find another programatic way, not just random sleeps... #
        __import__("time").sleep(0.2*wait_nthreads)

    for i in range(wait_nthreads):
        semaphore.release()
